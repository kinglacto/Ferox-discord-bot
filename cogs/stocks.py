import yfinance as yf
from discord import Embed
from discord.ext import commands

from data import Data


class Stocks(commands.Cog, Data):
    def __init__(self, bot):
        Data.__init__(self)
        self.bot = bot

    @commands.command()
    async def invest(self, ctx):
        self.users = self.retrieve(self.users_path)
        user_id = str(ctx.message.author.id)
        try:
            balance = self.users[user_id]["wallet"]
        except:
            if self.register_user(ctx.message.author, str(ctx.message.author)):
                balance = self.users[user_id]["wallet"]

        msg = list(filter(None, str(ctx.message.content).split(" ")))

        try:
            symbol = msg[2]

            if msg[3].strip().isdigit():
                amnt = int(msg[3])
        except:
            await ctx.reply("That ain't right. Type ``pls help invest`` to know more")
            return None

        try:
            data = yf.download(tickers=symbol, period='2d', interval='60m')
            price = round(data["Open"][3])
        except:
            await ctx.reply("Invalid symbol... or it could just be me glitching")
            return None
    
        invested_amnt = round(price * amnt)

        if invested_amnt > balance:
            await ctx.reply("You don't have the necessary funds for that, Walmart Warren")
        else:
            if symbol.upper() in self.users[user_id]["investments"]:
                self.users[user_id]["investments"][1] += amnt
                self.users[user_id]["investments"][2] += invested_amnt
            else:
                self.users[user_id]["investments"].append([symbol.upper(), amnt, invested_amnt])

            self.users[user_id]["wallet"] -= invested_amnt

            self.update_changes(self.users_path, self.users)

            await ctx.reply(f"You bought {'{:,}'.format(amnt)} share(s) of {symbol} for ${'{:,}'.format(invested_amnt)}")


    @commands.command()
    async def sell(self, ctx):
        self.users = self.retrieve(self.users_path)
        user_id = str(ctx.message.author.id)
        try:
            self.users[user_id]["investments"]
        except:
            self.register_user(ctx.message.author, str(ctx.message.author))

        msg = list(filter(None, str(ctx.message.content).split(" ")))

        try:
            symbol = msg[2].upper()
        
            if msg[3].strip().isdigit():
                amnt = int(msg[3])

        except:
            await ctx.reply("That ain't right. Type ``pls help sell`` to know more")
            return None

        if symbol in self.users[user_id]["investments"]:
            if amnt < self.users[user_id]["investments"][1]:
                try:
                    data = yf.download(tickers=symbol, period='2d', interval='60m')
                    price = round(data["Open"][3])
                except:
                    await ctx.reply("Invalid symbol... or it could just be me glitching")
                    return None

                sold = round(price * amnt)
                self.users[user_id]["investments"][symbol][1] -= amnt
                self.users[user_id]["investments"]["wallet"] += sold

                if self.users[user_id]["investments"][symbol][1] == 0:
                    del self.users[user_id]["investments"][symbol]
                self.update_changes(self.users_path, self.users)

                await ctx.reply(f"You sold {'{:,}'.format(amnt)} share(s) of {symbol} for ${'{:,}'.format(sold)}")
                return None
            else:
                await ctx.reply(f"You don't have those many shares in {symbol}")
            return None
        else:
            await ctx.reply(f"You haven't invested in {symbol}")
            return None


    @commands.command()
    async def price(self, ctx):
        self.users = self.retrieve(self.users_path)
        msg = list(filter(None, str(ctx.message.content).split(" ")))

        try:
            symbol = msg[2]
        except:
            await ctx.reply("That ain't right. Type ``pls help price`` to know more")
            return None
    
        try:
            data = yf.download(tickers=symbol, period='2d', interval='60m')
            price = round(data["Open"][3])
        except:
            await ctx.reply("Invalid symbol... or it could just be me glitching")
            return None

        if len(msg) == 3:
            await ctx.reply(f"{symbol}'s current share price is ${price}")
        else:
            if msg[3].isdigit():
               await ctx.reply(f"{symbol}'s current share price is ${price} \n{msg[3]} shares would cost you ${'{:,}'.format(int(msg[3]) * price)}") 
            else:
                await ctx.reply("Invalid amount")

    @commands.command(aliases=["port"])
    async def portfolio(self, ctx):
        self.users = self.retrieve(self.users_path)
        mentions = ctx.message.mentions
        if len(mentions) == 0:
            user = ctx.message.author.id
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
        for n, i in enumerate(investments):
            doc += f"{n+1}) **{i[0]}** : **{i[1]}** share(s) - **${i[2]}**\n"

        embed = Embed(title=f"{user_name}'s Portfolio:", description=f"{doc}", color=0x008508)
        await ctx.reply(embed=embed)