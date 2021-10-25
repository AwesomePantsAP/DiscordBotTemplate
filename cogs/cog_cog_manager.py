from discord.ext import commands
import importlib
from os import getcwd

class cog_cog_manager(commands.Cog):
    def __init__(self, client, *args):
        self.cogs_classes = {}
        print(f"CogManagerCog >>> Discovering Cogs")
        #iterate through args, accept the cogs that are valid and ignore invalid cogs
        for name in args:
            #see if the file exists and if it has the cog
            try:
                #try to open it
                cog_module = importlib.import_module("cogs." + name)
                #success, try to access the class now
                cog_class = getattr(cog_module, name)
                #success! store the module and class
                self.cogs_classes[name] = cog_class
                print(f"\tCog: {name} >>> [Valid]")

            except ImportError as e:
                #oops, file not found. oh well, ignore the cog
                print(f"\tCog: {name} >>> [Invalid: file not found]")
                print(e)
            except AttributeError as e:
                #oops, cog not found. oh well, ignore the cog
                print(f"\tCog: {name} >>> [Invalid: Cog not present in file]")
                print(e)
        print(f"CogManagerCog >>> Valid Cogs Found: {len(self.cogs_classes)}")

        #add cogs to bot
        self.cog_instances = {}
        for name, cog_class in self.cogs_classes.items():
            print(f"\tCog: {name} >>> Initializing")

            #create instance of cog
            cog_instance = cog_class(client)
            #add cog to bot
            client.add_cog(cog_instance)
            #store instance of cog
            self.cog_instances[name] = cog_instance

    #yields a cog if it is an instance of SetupCog
    def get_cogs_with_setup(self):
        for cog in self.cog_instances.items():
            if isinstance(cog, SetupCog):
                yield cog

    @commands.group(pass_context=True, invoke_without_command=True)
    async def managecogs(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("<@521285684271513601> Implement a help message system already you lazy bitch")

    @managecogs.command()
    async def list(self, ctx):
        await ctx.send()
