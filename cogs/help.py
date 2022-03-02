from discord import Embed
from discord.ext import commands

from data import Data

class Help(commands.Cog, Data):
    def __init__(self, bot):
        Data.__init__(self)
        self.bot = bot
        self.help_command_embeds = self.retrieve(self.help_commands_path)
        self.help_category_embeds = self.retrieve(self.help_category_path)
        self.command_aliases = {"dep": "deposit", "with":  "withdraw", "share": "give"}
        self.embed_color = 0x008508

        self.category_embeds = {}
        for category_embed in self.help_category_embeds:
            embed = Embed(title=self.help_category_embeds[category_embed]["title"], color=self.embed_color)
            for field in self.help_category_embeds[category_embed]["fields"]:
                embed.add_field(name=field, value=self.help_category_embeds[category_embed]["fields"][field], inline=False)
            embed.set_footer(text=self.help_category_embeds[category_embed]["footer"])
            self.category_embeds[category_embed] = embed
    
    @commands.command(aliases=["help"])
    async def Help(self, ctx):
        msg = list(filter(None, str(ctx.message.content).split(" ")))
        if len(msg) == 2:
            await ctx.reply(embed=self.category_embeds["help"])
        else:
            command = msg[2]
            if command in self.help_command_embeds:
                title = self.help_command_embeds[command]["title"]
                description = self.help_command_embeds[command]["description"]
            elif command in self.command_aliases:
                title = self.help_command_embeds[self.command_aliases[command]]["title"]
                description = self.help_command_embeds[self.command_aliases[command]]["description"]
            else:
                await ctx.reply("Either than ain't a valid command or I got nothing to more to say about it")
                return None

            embed = Embed(title=title, description=description, color=0x008508)
            await ctx.reply(embed=embed)

    @commands.command(aliases=["currency"])
    async def Currency(self, ctx):
        await ctx.reply(embed=self.category_embeds["Currency"])

    @commands.command(aliases=["fun"])
    async def Fun(self, ctx):
        await ctx.reply(embed=self.category_embeds["Fun"])

    @commands.command(aliases=["stocks"])
    async def Stocks(self, ctx):
        await ctx.reply(embed=self.category_embeds["Stocks"])

    @commands.command(aliases=["games"])
    async def Games(self, ctx):
        await ctx.reply(embed=self.category_embeds["Games"])

    @commands.command(aliases=["code"])
    async def Code(self, ctx):
        await ctx.reply(embed=self.category_embeds["Code"])