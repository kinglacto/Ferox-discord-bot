from discord import Embed
from discord.ext import commands

from data import Data

class Help(commands.Cog, Data):
    def __init__(self, bot):
        Data.__init__(self)
        self.bot = bot
        self.help_embeds = self.retrieve(self.help_path)
        self.command_aliases = {"dep": "deposit", "with":  "withdraw", "share": "give"}
    
    @commands.command()
    async def help(self, ctx):
        msg = list(filter(None, str(ctx.message.content).split(" ")))
        if len(msg) == 2:
            embed = Embed(title="Commands", color=0x008508)
            embed.add_field(name='Currency', value=' - To view all the currency commands', inline=False)
            embed.add_field(name='Fun', value=' - To view all the fun commands', inline=False)
            embed.add_field(name='Stocks', value=' - To view all the stock related commands', inline=False)
            embed.add_field(name='Games', value=' - To view all the games that can be played', inline=False)
            embed.add_field(name='Code', value=' - To view all the programming commands', inline=False)
            embed.set_footer(text=f"pls <NAME> to know more")
            await ctx.reply(embed=embed)
        else:
            command = msg[2]
            if command in self.help_embeds:
                title = self.help_embeds[command]["title"]
                description = self.help_embeds[command]["description"]
            elif command in self.command_aliases:
                title = self.help_embeds[self.command_aliases[command]]["title"]
                description = self.help_embeds[self.command_aliases[command]]["description"]
            else:
                await ctx.reply("Either than ain't a valid command or I got nothing to more to say about it")
                return None

            embed = Embed(title=title, description=description, color=0x008508)
            await ctx.reply(embed=embed)

    @commands.command(aliases=["currency"])
    async def Currency(self, ctx):
        embed = Embed(title="Currency Commands", color=0x008508)
        embed.add_field(name='balance', value=' - To check your balance. Tag someone to check theirs', inline=False)
        embed.add_field(name='deposit', value=' - To deposit money into your bank', inline=False)
        embed.add_field(name='withdraw', value=' - To withdraw money from your bank', inline=False)
        embed.add_field(name='give', value=' - To give money to someone', inline=False)
        embed.set_footer(text=f"pls help <CMD_NAME> to know more")
        await ctx.reply(embed=embed)

    @commands.command(aliases=["fun"])
    async def Fun(self, ctx):
        embed = Embed(title="Fun Commands", color=0x008508)
        embed.add_field(name='meme', value="- To view memes", inline=False)
        embed.add_field(name='gif', value=' - Sends a gif', inline=False)
        embed.add_field(name='roll', value=' - Gamble your money', inline=False)
        embed.add_field(name='meaning', value=" - find a word's meaning", inline=False)
        embed.add_field(name='emojify', value="- emojify your text", inline=False)
        embed.add_field(name='8ball', value="- Ask 8ball a question", inline=False)
        embed.set_footer(text=f"pls help <CMD_NAME> to know more")
        await ctx.reply(embed=embed)

    @commands.command(aliases=["stocks"])
    async def Stocks(self, ctx):
        embed = Embed(title="Stock Commands", color=0x008508)
        embed.add_field(name='invest', value=' - To invest into a stock', inline=False)
        embed.add_field(name='sell', value=' - To sell your shares', inline=False)
        embed.add_field(name='price', value=' - To check the current price of a stock', inline=False)
        embed.add_field(name='portfolio', value=' - To view your portfolio', inline=False)
        embed.set_footer(text=f"pls help <CMD_NAME> to know more")
        await ctx.reply(embed=embed)

    @commands.command(aliases=["games"])
    async def Games(self, ctx):
        embed = Embed(title="Games", color=0x008508)
        embed.add_field(name='connect4', value=' - To play connect4, ping the person (pls c4 @user) or (pls c4) to play with the bot', 
                        inline=False)
        embed.set_footer(text=f"pls help <CMD_NAME> to know more")
        await ctx.reply(embed=embed)

    @commands.command(aliases=["code"])
    async def Code(self, ctx):
        embed = Embed(title="Code", color=0x008508)
        embed.add_field(name='run', value='pls run language-name and code within code blocks in the next line', 
                        inline=False)
        embed.set_footer(text=f"pls help <CMD_NAME> to know more")
        await ctx.reply(embed=embed)