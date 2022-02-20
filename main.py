import os

from dotenv import load_dotenv
from discord import Intents
from discord.ext import commands

from cogs.register import Register
from cogs.help import Help
from cogs.stocks import Stocks
from cogs.currency import Currency   
from cogs.fun import Fun
from cogs.games import Games
from cogs.code import Code

def main():
    load_dotenv()

    intents = Intents.default()
    intents.members = True

    bot = commands.Bot(command_prefix="pls ", help_command=None, intents=intents)
    
    bot.add_cog(Register(bot))
    bot.add_cog(Help(bot))
    bot.add_cog(Stocks(bot))
    bot.add_cog(Currency(bot))
    bot.add_cog(Fun(bot))
    bot.add_cog(Games(bot))
    bot.add_cog(Code(bot))

    bot.run(os.getenv('DISCORD_TOKEN'))

if __name__ == "__main__":
    main()