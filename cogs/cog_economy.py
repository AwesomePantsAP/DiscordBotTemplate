from discord.ext import commands
from cogs.base_cog import BaseCog

class EconomyCog(BaseCog):
    def __init__(self):
        #get database connection
        pass

    @commands.group(pass_context=True, invoke_without_command=True)
    def economy(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("<@521285684271513601> Implement a help message system already you lazy bitch")

    @economy.command()
    def balance(self, ctx):
        pass

    @economy.command()
    def bal(self, ctx):
        self.balance(ctx)

    @economy.command()
    def baltop(self, ctx, check_users=10):
        pass

    @economy.command()
    def checkbalance(self, ctx, user):
        pass

    @economy.command()
    def pay(self, ctx, user):
        pass
