from discord.ext import commands
from cogs.base_cog import BaseCog
from cogs.cog_cog_manager import DependencyUnmetError

class cog_economy(BaseCog):
    def __init__(self, client):
        db_cog = client.get_cog("cog_database")
        if db_cog is None:
            #raise an exception if it's not present
            raise DependencyUnmetError("Dependency `cog_database` Unmet in `cog_economy!`")

    def setup(self, client):
        #get database cog
        self.db_cog = client.get_cog("cog_database")
        if self.db_cog is None:
            #raise an exception if it's not present
            raise DependencyUnmetError("Dependency `cog_database` Unmet in `cog_economy!`")

    @commands.group(pass_context=True, invoke_without_command=True)
    async def economy(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("<@521285684271513601> Implement a help message system already you lazy bitch")

    @economy.command()
    async def balance(self, ctx):
        pass

    @economy.command()
    async def bal(self, ctx):
        self.balance(ctx)

    @economy.command()
    async def baltop(self, ctx, check_users=10):
        pass

    @economy.command()
    async def checkbalance(self, ctx, user):
        pass

    @economy.command()
    async def pay(self, ctx, user):
        pass
