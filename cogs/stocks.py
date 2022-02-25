import yfinance as yf
from discord import Embed
from discord.ext import commands

from data import Data


class Stocks(commands.Cog, Data):
    def __init__(self, bot):
        Data.__init__(self)
        self.bot = bot

    @commands.command()
    async def invest(self, ctx, symbol=None, num_of_shares="1"):
        self.users = self.retrieve(self.users_path)
        user_id = str(ctx.message.author.id)
        try:
            balance = self.users[user_id]["wallet"]
        except:
            if self.register_user(ctx.message.author, str(ctx.message.author)):
                balance = self.users[user_id]["wallet"]

        if symbol is None:
            await ctx.reply("Invalid symbol. Type ``pls help price`` to know more")
            return None
        else:
            symbol = symbol.upper()
        
        if type(num_of_shares) == int or num_of_shares.isdigit():
            num_of_shares = int(num_of_shares)
            try:
                price = round(yf.download(tickers=symbol, period='2d', interval='60m')["Open"][-1], 2)
            except:
                await ctx.reply("Invalid symbol... or it could just be me glitching")
                return None
        else:
            await ctx.reply("Is that even a number, bruh? Type ``pls help invest`` to know more")
            return None

        invested_amnt = price * num_of_shares

        if invested_amnt > balance:
            await ctx.reply("You don't have the necessary funds for that, Walmart Warren")
        else:
            if symbol in self.users[user_id]["investments"]:
                self.users[user_id]["investments"][symbol]["num"] += num_of_shares
                self.users[user_id]["investments"][symbol]["amnt"] += invested_amnt
            else:
                self.users[user_id]["investments"][symbol] = {
                    "num" : num_of_shares,
                    "amnt" : invested_amnt
                }

            self.users[user_id]["wallet"] -= invested_amnt
            self.update_changes(self.users_path, self.users)

            await ctx.reply(f"You bought {'{:,}'.format(num_of_shares)} share(s) of {symbol} for ${'{:,}'.format(invested_amnt)}")

    @commands.command()
    async def sell(self, ctx, symbol=None, num_of_shares="1"):
        self.users = self.retrieve(self.users_path)
        user_id = str(ctx.message.author.id)
        try:
            self.users[user_id]["investments"]
        except:
            self.register_user(ctx.message.author, str(ctx.message.author))

        if symbol is None:
            await ctx.reply("Invalid symbol. Type ``pls help price`` to know more")
            return None
        else:
            symbol = symbol.upper()

        if type(num_of_shares) == int or num_of_shares.isdigit():
            num_of_shares = int(num_of_shares)
        else:
            await ctx.reply("Is that even a number, bruh? Type ``pls help invest`` to know more")
            return None

        if symbol in self.users[user_id]["investments"]:
            if num_of_shares <= self.users[user_id]["investments"][symbol]["num"]:
                try:
                    price = round(yf.download(tickers=symbol, period='2d', interval='60m')["Open"][-1], 2)
                except:
                    await ctx.reply("Invalid symbol... or it could just be me glitching")
                    return None

                sold_amnt = price * num_of_shares
                self.users[user_id]["investments"][symbol]["num"] -= num_of_shares
                self.users[user_id]["wallet"] += sold_amnt

                if self.users[user_id]["investments"][symbol]["num"] == 0:
                    del self.users[user_id]["investments"][symbol]
                self.update_changes(self.users_path, self.users)

                await ctx.reply(f"You sold {'{:,}'.format(num_of_shares)} share(s) of {symbol} for ${'{:,}'.format(sold_amnt)}")
                return None
            else:
                await ctx.reply(f"You don't have those many shares in {symbol}")
            return None
        else:
            await ctx.reply(f"You haven't invested in {symbol}")
            return None


    @commands.command()
    async def price(self, ctx, symbol=None, num_of_shares="1"):
        if symbol is None:
            await ctx.reply("Invalid symbol. Type ``pls help price`` to know more")
            return None
    
        try:
            price = round(yf.download(tickers=symbol, period='2d', interval='60m')["Open"][-1], 2)
        except:
            await ctx.reply("Invalid symbol... or it could just be me glitching")
            return None

        if type(num_of_shares) == int or num_of_shares.isdigit():
            await ctx.reply(f"{symbol}'s current share price is ${price} \n{num_of_shares} share(s) would cost you ${'{:,}'.format(int(num_of_shares) * price)}") 
        else:
            await ctx.reply("Invalid amount")

    @commands.command(aliases=["port"])
    async def portfolio(self, ctx):
        self.users = self.retrieve(self.users_path)
        mentions = ctx.message.mentions
        if len(mentions) == 0:
            user = ctx.message.author
        else:
            user = mentions[0]
            
        user_id = str(user.id)
        try:
            investments = self.users[user_id]["investments"]
        except:
            name = await self.bot.fetch_user(int(user.id))
            if self.register_user(user, str(name)):
                investments = self.users[user_id]["investments"]

        user_name = ''.join(list(str(self.users[user_id]["user_name"]))[:-5])
        doc = ""
        for index, symbol in enumerate(investments):
            num, amnt = investments[symbol]["num"], investments[symbol]["amnt"]
            doc += f"{index + 1}) **{symbol}** : **{num}** share(s) - **${amnt}**\n"

        embed = Embed(title=f"{user_name}'s Portfolio:", description=f"{doc}", color=0x008508)
        await ctx.reply(embed=embed)