import discord
import os
import asyncio
# load our local env so we dont have the token in public
from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio
from discord import TextChannel
from youtube_dl import YoutubeDL

#info about a song
class Song():
    url = ""
    title = ""
    duration = None

    #construct a song
    def __init__(self, _url, _title, _duration=0):
        self.url = _url
        self.title = _title
        self.duration = _duration

#gets the info of a playlist
def get_song_info(song_name):
    #options for youtube dl
    YDL_OPTIONS = {'format': 'bestaudio', 'yesplaylist': 'True', 'quiet' : "True"}

    #search for the video as a link
    songs = []
    with YoutubeDL(YDL_OPTIONS) as ydl:
        info = ydl.extract_info(song_name, download=False)

        #if the result is a song, get and return it
        if "url" in info:
            songs.append(Song(info['url'], info["title"], info["duration"]))
            return songs
        #otherwise if the result is a playlist, get all songs and return them
        elif "entries" in info:
            for entry in info["entries"]:
                songs.append(Song(entry['url'], entry["title"], entry["duration"]))
            return songs

    #get the search result for the song name
    with YoutubeDL(YDL_OPTIONS) as ydl:
        info = ydl.extract_info(f"ytsearch:{song_name}", download=False)

    #get and return the first search result
    first_result = info["entries"][0]
    songs.append(Song(first_result['url'], first_result["title"], first_result["duration"]))
    return songs

#plays the next song in the queue
async def _play_next_song(ctx):
    #we need access to the queue
    global queued_songs

    #ffmpeg options
    FFMPEG_OPTIONS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

    #just stop if there aren't any queued songs
    if len(queued_songs) == 0:
        return

    #get and remove the next song in the queue
    song = queued_songs.pop(0)

    #get the voice client of the bot in the guild
    voice = get(client.voice_clients, guild=ctx.guild)

    #play the next song in the queue
    print(f"Playing song {song.title}")
    voice.play(FFmpegPCMAudio(song.url, **FFMPEG_OPTIONS), after=lambda: asyncio.run(_play_next_song(ctx)))
    await ctx.send(f'Playing song `{song.title}`!')

client = commands.Bot(command_prefix='!')  # prefix our commands with '!'

#queued songs to play
queued_songs = []

@client.event  # check if bot is ready
async def on_ready():
    print('Bot online')

@client.command()
async def queue(ctx):
    #we need access to the queue
    global queued_songs

    #template string for string.format
    queue_entry_template = "\n\t{0}. {1}: Length: {2}"

    #start the message as a css codeblock(for looks only)
    final_message = "```css\nQueue:"
    #iterate through each song in the queue
    for song_i in range(len(queued_songs)):
        #get the current song
        song = queued_songs[song_i]
        #add the formatted template string onto the message
        final_message += queue_entry_template.format(
            song_i,
            song.title,
            song.duration
        )
    #end the code block
    final_message += "\n```"

    #send the message
    await ctx.send(final_message)

# command for bot to join the channel of the user, if the bot has already joined and is in a different channel, it will move to the channel the user is in
@client.command()
async def join(ctx):
    #get the voice channel of the user
    channel = ctx.message.author.voice.channel
    #get our voice client
    voice = get(client.voice_clients, guild=ctx.guild)
    
    #are we already connected to a voice channel
    if voice and voice.is_connected():
        #yes, move to the user's channel
        await voice.move_to(channel)
    else:
        #no, connect to the user's channel
        voice = await channel.connect()

#play a video, either by searching or by url
@client.command()
async def play(ctx):
    #we need access to the queue
    global queued_songs

    #get the name of the song
    song_name = " ".join(ctx.message.content.split(" ")[1:])

    #get the voice client of the bot in the guild
    voice = get(client.voice_clients, guild=ctx.guild)

    #add all the songs(for one song we still get a playlist of one) to the queue
    queued_songs += get_song_info(song_name)

    #only begin playing if we aren't already playing a song
    if not voice.is_playing():
        #we aren't playing a song, start playing the queue
        print(f"\n\t{ctx.message.author.guild.name}::{ctx.message.author.name}#{ctx.message.author.discriminator} \n\t\tPlaying song {song_name}")
        await _play_next_song(ctx)
    else:
        #just stop at queuing the song
        print(f"\n\t{ctx.message.author.guild.name}::{ctx.message.author.name}#{ctx.message.author.discriminator} \n\t\tQueuing song {song_name}")
        await ctx.send(f"Queueing song `{song_name}`...")

# command to resume voice if it is paused
@client.command()
async def resume(ctx):
    #get the client voice
    voice = get(client.voice_clients, guild=ctx.guild)

    #only resume if the voice isn't playing
    if not voice.is_playing():
        #resume
        voice.resume()
        await ctx.send('Resuming! :play_icon:')


# command to pause voice if it is playing
@client.command()
async def pause(ctx):
    #get the voice client
    voice = get(client.voice_clients, guild=ctx.guild)

    #only pause if the voice is playing
    if voice.is_playing():
        #pause
        voice.pause()
        await ctx.send('Paused! :pause_icon:')


# command to stop voice
@client.command()
async def stop(ctx):
    #get the voice client
    voice = get(client.voice_clients, guild=ctx.guild)

    #only stop if the voice is playing
    if voice.is_playing():
        #stop
        voice.stop()
        await ctx.send('Stopped! :stop_sign:')


# command to clear channel messages
@client.command()
async def clear(ctx, amount=5):
    #purge messages with limit limit
    await ctx.channel.purge(limit=amount)
    await ctx.send("Cleared! :broom::wind:")

#get the bot token
token_file = open("token.txt")
token = token_file.read()
print(token)

#start the bot
client.run(token)
