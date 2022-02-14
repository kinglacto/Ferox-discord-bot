from discord import Embed
from cogs.data import Data
from discord.ext import commands
import yfinance as yf


class Stocks(commands.Cog, Data):
    def __init__(self, bot):
        Data.__init__(self)
        self.bot = bot

    @commands.command()
    async def invest(self, ctx):
        self.users = self.retrieve("data\\users.json")
        user_id = str(ctx.message.author.id)
        try:
            balance = self.users[user_id]["wallet"]
        except:
            self.register(user_id, str(ctx.message.author))
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
            self.users[user_id]["investments"].append([symbol.upper(), amnt, price, invested_amnt, self.now.strftime("%d/%m/%Y")])
            self.users[user_id]["wallet"] -= invested_amnt

            self.update_changes("data\\users.json", self.users)

            await ctx.reply(f"You bought {'{:,}'.format(amnt)} share(s) of {symbol} for ${'{:,}'.format(invested_amnt)}")


    @commands.command()
    async def sell(self, ctx):
        self.users = self.retrieve("data\\users.json")
        user_id = str(ctx.message.author.id)
        try:
            i = self.users[user_id]["investments"]
        except:
            self.register(user_id, str(ctx.message.author))
            i = self.users[user_id]["investments"]

        msg = list(filter(None, str(ctx.message.content).split(" ")))

        try:
            symbol = msg[2]
        
            if msg[3].strip().isdigit():
                amnt = int(msg[3])

            if msg[4].strip().isdigit():
                index = int(msg[4])
        except:
            await ctx.reply("That ain't right. Type ``pls help sell`` to know more")
            return None

        try:
            i = i[index - 1]
            if amnt <= i[1]:
                try:
                    data = yf.download(tickers=symbol, period='2d', interval='60m')
                    price = round(data["Open"][3])
                except:
                    await ctx.reply("Invalid symbol... or it could just be me glitching")
                    return None

                sold = round(price * amnt)
                if i[1] - amnt == 0:
                    del self.users[user_id]["investments"][index - 1]
                else:
                    self.users[user_id]["investments"][index - 1][1] -= amnt
                    self.users[user_id]["wallet"] += sold

                    self.update_changes("data\\users.json", self.users)

                    await ctx.reply(f"You sold {'{:,}'.format(amnt)} share(s) of {symbol} for ${'{:,}'.format(sold)}")
                    return None
            else:
                await ctx.reply(f"You don't have that many share(s)")
                return None
        except:
            await ctx.reply(f"You haven't invested in {symbol}")
            return None


    @commands.command()
    async def price(self, ctx):
        self.users = self.retrieve("data\\users.json")
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
        self.users = self.retrieve("data\\users.json")
        mentions = ctx.message.mentions
        if len(mentions) == 0:
            user_id = str(ctx.message.author.id)
        else:
            user_id = str(mentions[0].id)

        try:
            investments = self.users[str(user_id)]["investments"]
        except:
            name = await self.bot.fetch_user(int(user_id))
            self.register(user_id, str(name))
            investments = self.users[str(user_id)]["investments"]

        user_name = ''.join(list(str(self.users[str(user_id)]["user_name"]))[:-5])
        doc = ""
        for n, i in enumerate(investments):
            doc += f"{n+1}) **{i[0]}** : **{i[1]}** share(s) - ${i[2]} per share /{i[1]} for ${i[3]} {i[4]}\n"

        embed = Embed(title=f"{user_name}'s Portfolio:", description=f"{doc}", color=0x008508)
        await ctx.reply(embed=embed)