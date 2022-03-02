from datetime import datetime

from discord import Embed
from discord.ext import commands

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.now = datetime.now()

    @commands.command(aliases=["lock"])
    @commands.has_permissions(administrator=True)
    async def lock_channel(self, ctx, reason="Not stated"):
        for role in ctx.guild.roles:
            try:
                await ctx.message.channel.set_permissions(role, send_messages=False)
            except:
                await ctx.send("I don't have the permissions to do that")
                return None

        date_time = self.now.strftime("%H:%M:%S-%d/%m/%Y")
        embed = Embed(title=f"🔒 Channel Locked", description=f"**Locked by:** <@{ctx.message.author.id}> \n**Reason:** {reason} \n**Locked at:** {date_time}")
        await ctx.channel.send(embed=embed)

    @commands.command(aliases=["unlock"])
    @commands.has_permissions(administrator=True)
    async def unlock_channel(self, ctx, reason="Not stated"):
        for role in ctx.guild.roles:
            try:
                await ctx.message.channel.set_permissions(role, send_messages=True)
            except:
                await ctx.send("I don't have the permissions to do that")
                return None

        date_time = self.now.strftime("%H:%M:%S-%d/%m/%Y")
        embed = Embed(title=f"🔓 Channel Unocked", description=f"**Unlocked by:** <@{ctx.message.author.id}> \n**Reason:** {reason} \n**Unlocked at:** {date_time}")
        await ctx.channel.send(embed=embed)

    @commands.command(aliases=["lockdown"])
    @commands.has_permissions(manage_channels=True)
    async def server_lockdown(self, ctx, reason="Not stated"):
        locked_categories = []
        for category in ctx.guild.categories:
            permission_denied = False
            for role in ctx.guild.roles:
                if not permission_denied:
                    try:
                        await category.set_permissions(role, send_messages=False, speak=False)
                        locked_categories.append(category.name) if category.name not in locked_categories else locked_categories
                    except:
                        await ctx.channel.send(f"I don't have the permissions to do that in {category}")
                        permission_denied = True

        date_time = self.now.strftime("%H:%M:%S-%d/%m/%Y")
        embed = Embed(title=f"🔐 Server Lockdown", description=f"**Locked Categories:** {locked_categories} \n**Server locked by:** <@{ctx.message.author.id}> \n**Reason:** {reason} \n**Server locked at:** {date_time}")
        await ctx.channel.send(embed=embed)

    @commands.command(aliases=["lift"])
    @commands.has_permissions(manage_channels=True)
    async def unlock_server(self, ctx, reason="Not stated"):
        unlocked_categories = []
        for category in ctx.guild.categories:
            permission_denied = False
            for role in ctx.guild.roles:
                if not permission_denied:
                    try:
                        await category.set_permissions(role, send_messages=True, speak=True)
                        unlocked_categories.append(category.name) if category.name not in unlocked_categories else unlocked_categories
                    except:
                        await ctx.channel.send(f"I don't have the permissions to do that in {category}")
                        permission_denied = True

        date_time = self.now.strftime("%H:%M:%S-%d/%m/%Y")
        embed = Embed(title=f"🔐 Server Unlocked", description=f"**Unlocked Categories:** {unlocked_categories} \n**Server unlocked by:** <@{ctx.message.author.id}> \n**Reason:** {reason} \n**Server unlocked at:** {date_time}")
        await ctx.channel.send(embed=embed)

    

    