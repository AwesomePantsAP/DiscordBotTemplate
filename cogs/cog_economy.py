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

        #create the table in the database if it doesn't exist
        create_table_query = """CREATE TABLE IF NOT EXISTS balances (
            balance_id INTEGER PRIMARY KEY NOT NULL UNIQUE,
            balance INTEGER,
            uuid VARCHAR(18) NOT NULL,
            guild_id VARCHAR(18) NOT NULL
        )
        """
        self.db_cog.do_query(create_table_query)

    #creates a balance totaling balance for user uuid in guild guild_id
    def create_balance(self, balance, uuid, guild_id):
        create_balance_query = "INSERT INTO balances VALUES (?, ?, ?)"
        self.db_cog.do_query(create_balance_query, (balance, uuid, guild_id))

    #changes balance by ammount
    def change_balance(self, ammount, uuid, guild_id):
        change_balance_query = "UPDATE balances SET balance = balance + ? WHERE uuid=? AND guild_id=?"
        self.db_cog.do_query(change_balance_query, (ammount, uuid, guild_id))

    #sets the balance to balance
    def set_balance(self, balance, uuid, guild_id):
        set_balance_query = "UPDATE balances SET balance = ? WHERE uuid=? AND guild_id=?"
        self.db_cog.do_query(set_balance_query, (balance, uuid, guild_id))

    #gets the balance belonging to uuid in guild_id
    def get_balance(self, uuid, guild_id):
        get_balance_query = "SELECT balance FROM balances WHERE uuid=? AND guild_id=?"
        result = self.db_cog.do_query(get_balance_query, (uuid, guild_id)).fetchone()

        #if it's none, return none
        if isinstance(result, None):
            return None
        #otherwise, it's a tuple; return the first element
        else:
            return result[0]

    #removes a balance entry belonging to uuid in guild_id
    def remove_balance(self, uuid, guild_id):
        remove_balance_query = "DELETE FROM balances WHERE uuid=? AND guild_id=?"
        return self.db_cog.do_query(remove_balance_query, (uuid, guild_id))

    @commands.group(pass_context=True, invoke_without_command=True)
    async def economy(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("<@521285684271513601> Implement a help message system already you lazy bastard")

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
