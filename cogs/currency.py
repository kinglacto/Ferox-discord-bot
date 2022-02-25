from discord import Embed
from discord.ext import commands

from data import Data

class Currency(commands.Cog, Data):
    def __init__(self, bot):
        Data.__init__(self)
        self.bot = bot

    @commands.command(aliases=["bal"])
    async def balance(self, ctx):
        self.users = self.retrieve(self.users_path)

        mentions = ctx.message.mentions
        if len(mentions) == 0:
            user = ctx.message.author
        else:
            user = mentions[0]

        user_id = str(user.id)

        try:
            wallet_bal = self.users[user_id]["wallet"]
        except:
            if self.register_user(user, str(ctx.message.author)):
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
    async def deposit(self, ctx, amount=None):
        self.users = self.retrieve(self.users_path)

        user_id = str(ctx.message.author.id)

        try:
            bank = self.users[user_id]["bank"]
        except:
            if self.register_user(ctx.message.author, str(ctx.message.author)):
                bank = self.users[user_id]["bank"]

        bank_space = self.users[user_id]["bank_space"]
        wallet = self.users[user_id]["wallet"]
        available_space = (bank_space - bank)

        if amount is None:
            await ctx.reply("Enter an amount to deposit")
            return None
        elif amount in ("all", "max"):
            if wallet >= available_space:
                amount = available_space
            else:
                amount = wallet
        elif type(amount) == int or amount.isdigit():
            amount = int(amount)
        else:
            await ctx.reply("No idea what that is")
            return None

        if amount == 0:
            await ctx.reply("I don't even know what to say")
            return None

        if wallet > 0:
            if amount <= wallet:
                if amount <= available_space:
                    self.users[user_id]["bank"] += amount
                    self.users[user_id]["wallet"] -= amount
                    self.update_changes(self.users_path, self.users)
                    await ctx.reply(f"Deposited ${amount}")
                else:
                    await ctx.reply("You don't have enough bank space")
            else:
                await ctx.reply("You don't have that much money")
        else:
            await ctx.reply("You got 0. What on earth are you thinking?")


    @commands.command(aliases=["with"])
    async def withdraw(self, ctx, amount=None):
        self.users = self.retrieve(self.users_path)

        user_id = str(ctx.message.author.id)

        try:
            bank = self.users[user_id]["bank"]
        except:
            if self.register_user(ctx.message.author, str(ctx.message.author)):
                bank = self.users[user_id]["bank"]

        if bank == 0:
            await ctx.reply("You have no money to withdraw")
            return None

        if amount is None:
            await ctx.reply("Enter an amount to withdraw")
            return None
        elif amount in ("all", "max"):
            amount = bank
        elif type(amount) == int or amount.isdigit():
            amount = int(amount)
        else:
            await ctx.reply("Go away, what does that even mean?")
            return None

        if amount == 0:
            await ctx.reply("Is there any point?")
            return None

        if amount <= bank:
            self.users[user_id]["bank"] -= amount
            self.users[user_id]["wallet"] += amount
            self.update_changes(self.users_path, self.users)
            await ctx.reply(f"Withdrew ${amount}")
        else:
            await ctx.reply("You don't have that much money in your bank :0")

    @commands.command(aliases=["share"])
    async def give(self, ctx, amount=None):
        self.users = self.retrieve(self.users_path)

        user = ctx.message.author
        user_id = str(user.id)

        try:
            wallet = self.users[user_id]["wallet"]
        except:
            if self.register_user(user, str(ctx.message.author)):
                wallet = self.users[user_id]["wallet"]

        if wallet == 0:
            await ctx.reply("You got no money to share, sorry")
            return None

        if amount is None:
            await ctx.reply("Enter an amount to withdraw")
            return None
        elif amount in ("all", "max"):
            amount = wallet
        elif type(amount) == int or amount.isdigit():
            amount = int(amount)
        else:
            await ctx.reply("Go away, what does that even mean?")
            return None

        if amount == 0:
            await ctx.reply("Seriously? very philanthrophic of you")
            return None

        mentions = ctx.message.mentions
        if len(mentions) == 0:
            await ctx.reply("I guess you got no friends to share with")
            return None
        else:
            mention = mentions[0]
            mention_id = str(mention.id)

            try:    
                self.users[mention_id]["wallet"]
            except:
                name = await self.bot.fetch_user(int(mention_id))
                self.register_user(mention, str(name))

            if mention_id == ctx.message.author.id:
                await ctx.reply("Pretty lame")
                return None

        if amount <= wallet:
            self.users[user_id]["wallet"] -= amount
            self.users[mention_id]["wallet"] += amount
            self.update_changes(self.users_path, self.users)
            await ctx.reply(f"You gave <@{mention_id}> ${amount}")
        else:
            await ctx.reply("You don't have that much money to share")