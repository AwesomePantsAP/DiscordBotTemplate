from discord.ext import commands
from enum import Enum

#datatype of a column in a table
class ColumnDatatype(Enum):
    NONE = 0
    PRIMARY_KEY = 1
    UNIQUE = 2
    NOT_NULL = 3

#column in a table
class TableColumn:
    def __init__(self, name, data_type, constraints, without_rowid=False):
        self.name = name
        self.data_type = data_type
        self.constraints = constraints
        self.without_rowid = without_rowid

    def as_sql():
        pass

#describes a table
class Table:
    def __init__(self, name, **kwargs):
        pass

class DatabaseCog(commands.cog):
    #gets the database and checks that all servers have entries in the "servers" table
    def __init__(self, database_path):
        #get the database connection
        #store it

        #set up tables if they don't exist
        pass

    #creates table in database
    def CreateTable(self, table):
        pass
