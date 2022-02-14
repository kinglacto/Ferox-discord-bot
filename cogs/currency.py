from discord import Embed
from cogs.data import Data
from discord.ext import commands

class Currency(commands.Cog, Data):
    def __init__(self, bot):
        Data.__init__(self)
        self.bot = bot

    @commands.command(aliases=["bal"])
    async def balance(self, ctx):
        self.users = self.retrieve("data/users.json")
        mentions = ctx.message.mentions
        if len(mentions) == 0:
            user_id = str(ctx.message.author.id)
        else:
            user_id = str(mentions[0].id)

        try:
            wallet_bal = self.users[user_id]["wallet"]
        except:
            name = await self.bot.fetch_user(int(user_id))
            self.register(user_id, str(name))
            wallet_bal = self.users[user_id]["wallet"]

        bank_bal = self.users[user_id]["bank"]
        bank_space = self.users[user_id]["bank_space"]
        user_name = ''.join(list(self.users[user_id]["user_name"])[:-5])
        percentage = "{:.2f}".format((bank_bal/bank_space) * 100)

        embed = Embed(title=f"{user_name}'s balance",
                              description=f"**Wallet: **${'{:,}'.format(wallet_bal)} \n **Bank: **${'{:,}'.format(bank_bal)} / {'{:,}'.format(bank_space)} ``({percentage}%)``",
                              color=0x212121)
        await ctx.reply(embed=embed)

    @commands.command(aliases=["dep"])
    async def deposit(self, ctx):
        self.users = self.retrieve("data/users.json")
        user_id = str(ctx.message.author.id)
        try:
            bank = self.users[user_id]["bank"]
        except:
            self.register(user_id, str(ctx.message.author))
            bank = self.users[user_id]["bank"]

        bank_space = self.users[user_id]["bank_space"]
        wallet = self.users[user_id]["wallet"]

        msg = list(filter(None, str(ctx.message.content).split(" ")))[2]

        if msg in ("max", "all"):
            if wallet > 0:
                avail = (bank_space - bank)
                if avail > 0:
                    if wallet >= avail:
                        amnt = avail
                    else:
                        amnt = wallet
                    self.users[user_id]["bank"] += amnt
                    self.users[user_id]["wallet"] -= amnt
                    self.update_changes("data/users.json", self.users)
                    await ctx.reply(f"Deposited ${amnt}")
                else:
                    await ctx.reply("Your bank is full")
            else:
                await ctx.reply("You got 0. What on earth are you thinking?")
                
        elif msg.isdigit():
            amnt = int(msg)
            if amnt <= wallet:
                if amnt <= (bank_space - bank):
                    self.users[user_id]["bank"] += amnt
                    self.users[user_id]["wallet"] -= amnt
                    self.update_changes("data/users.json", self.users)
                    await ctx.reply(f"Deposited ${amnt}")
                else:
                    await ctx.reply("You don't have enough bank space")
            else:
                await ctx.reply("You don't have that much money")
        else:
            await ctx.reply("Stop bothering me with these lame messages")


    @commands.command(aliases=["with"])
    async def withdraw(self, ctx):
        self.users = self.retrieve("data/users.json")
        user_id = str(ctx.message.author.id)
        try:
            bank = self.users[user_id]["bank"]
        except:
            self.register(user_id, str(ctx.message.author))
            bank = self.users[user_id]["bank"]

        msg = list(filter(None, str(ctx.message.content).split(" ")))[2]

        if msg in ("max", "all"):
            self.users[user_id]["bank"] -= bank
            self.users[user_id]["wallet"] += bank
            self.update_changes("data/users.json", self.users)
            await ctx.reply(f"Withdrew ${bank}")

        elif msg.isdigit():
            amnt = int(msg)
            if amnt <= bank:
                self.users[user_id]["bank"] -= amnt
                self.users[user_id]["wallet"] += amnt
                self.update_changes("data/users.json", self.users)
                await ctx.reply(f"Withdrew ${amnt}")
            else:
                await ctx.reply("You don't have that much money :0")

        else:
            await ctx.reply("Go away")


    @commands.command(aliases=["share"])
    async def give(self, ctx):
        self.users = self.retrieve("data/users.json")
        user_id = str(ctx.message.author.id)
        try:
            wallet = self.users[user_id]["wallet"]
        except:
            name = await self.bot.fetch_user(int(user_id))
            self.register(user_id, str(name))
            wallet = self.users[user_id]["wallet"]

        mentions = ctx.message.mentions
        if len(mentions) == 0:
            await ctx.reply("I guess you got no friends to share with")
        else:
            mention_id = str(mentions[0].id)
            if mention_id in self.users:
                if mention_id == ctx.message.author.id:
                    await ctx.reply("Pretty lame")

                else:
                    amnt = list(filter(None, str(ctx.message.content).split(" ")))[2]
                    if amnt in ("max", "all"):
                        if wallet > 0:
                            amnt = wallet
                            self.users[user_id]["wallet"] -= amnt
                            self.users[str(mention_id)]["wallet"] += amnt
                            self.update_changes("data/users.json", self.users)
                            await ctx.reply(f"You gave <@{mention_id}> ${amnt}")
                        else:
                            await ctx.reply("You don't have that much money")

                    elif amnt.isdigit():
                        amnt = int(amnt)
                        if amnt <= wallet:
                            self.users[user_id]["wallet"] -= amnt
                            self.users[str(mention_id)]["wallet"] += amnt
                            self.update_changes("data/users.json", self.users)
                            await ctx.reply(f"You gave <@{mention_id}> ${amnt}")
                        else:
                            await ctx.reply("You don't have that much money")
                    
                    else:
                        await ctx.reply("I am sick of these failed messages")