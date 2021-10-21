import discord
import os
# load our local env so we dont have the token in public
from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio
from discord import TextChannel
from youtube_dl import YoutubeDL

client = commands.Bot(command_prefix='q_')  # prefix our commands with '.'

players = {}

#queued songs to play
queued_songs = []

@client.event  # check if bot is ready
async def on_ready():
    print('Bot online')

@client.command()
async def queue(ctx):
    global queued_songs

    queue_entry_template = "\t{0}. {1}: Length: {2}\n"
    final_message = "```\nQueue:"
    for song_i in range(len(queued_songs)):
        song = queued_songs[song_i]
        final_message += queue_entry_template.format(
            song_i,
            song.title,
            song.duration
        )
    final_message += "\n```"
    await ctx.send(final_message)

# command for bot to join the channel of the user, if the bot has already joined and is in a different channel, it will move to the channel the user is in
@client.command()
async def join(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()

class Song():
    url = ""
    title = ""
    duration = None

def get_playlist_info(song_name):
    YDL_OPTIONS = {'format': 'bestaudio', 'yesplaylist': 'True', 'quiet' : "True"}

    songs = []
    #try getting the song as a url and use that if it's a url, otherwise search for it
    with YoutubeDL(YDL_OPTIONS) as ydl:
        info = ydl.extract_info(song_name, download=False)
        if "url" in info:
            song = Song()
            song.url = info['url']
            song.title = info["title"]
            song.duration = info["duration"]
            songs.append(song)
            return songs

    #get the search result for the song name
    with YoutubeDL(YDL_OPTIONS) as ydl:
        info = ydl.extract_info(f"ytsearch:{song_name}", download=False)

    for entry in info["entries"]:
        song = Song()
        song.url = entry['url']
        song.title = entry["title"]
        song.duration = entry["duration"]
        songs.append(song)
    return songs

#plays the next song in the queue
async def _play_next_song(ctx):
    global queued_songs

    FFMPEG_OPTIONS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

    if len(queued_songs) == 0:
        return

    #get and remove the next song in the queue
    song = queued_songs.pop(0)

    #get the voice client of the bot in the guild
    voice = get(client.voice_clients, guild=ctx.guild)

    print(f"Playing song {song.title}")
    voice.play(FFmpegPCMAudio(song.url, **FFMPEG_OPTIONS), after=lambda: asyncio.run(_play_next_song(ctx)))
    voice.is_playing()
    await ctx.send(f'Bot is playing song `{song.title}`')

# command to play sound from a youtube URL
@client.command()
async def play(ctx):
    global queued_songs

    #get the name of the song
    song_name = " ".join(ctx.message.content.split(" ")[1:])

    #get the voice client of the bot in the guild
    voice = get(client.voice_clients, guild=ctx.guild)

    #only begin playing if we aren't already playing a song
    queued_songs += get_playlist_info(song_name)
    if not voice.is_playing():
        print(f"{ctx.message.author.guild.name}::{ctx.message.author.name}#{ctx.message.author.discriminator} Playing song {song_name}")
        await _play_next_song(ctx)
    else:
        #queue the song
        print(f"{ctx.message.author.guild.name}::{ctx.message.author.name}#{ctx.message.author.discriminator} Queuing song {song_name}")
        await ctx.send(f"Queueing song `{song_name}`")

# command to resume voice if it is paused
@client.command()
async def resume(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)

    if not voice.is_playing():
        voice.resume()
        await ctx.send('Bot is resuming')


# command to pause voice if it is playing
@client.command()
async def pause(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice.is_playing():
        voice.pause()
        await ctx.send('Bot has been paused')


# command to stop voice
@client.command()
async def stop(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice.is_playing():
        voice.stop()
        await ctx.send('Stopping...')


# command to clear channel messages
@client.command()
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount)
    await ctx.send("Messages have been cleared")


client.run("NTY1NDk5NjUzMDg1MzMxNDk2.XK3Ulw.2h7jXJp0ljXFtItkm8ZqRXK0w2g")
