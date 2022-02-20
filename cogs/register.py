from discord.ext import commands

from data import Data

class Register(commands.Cog, Data):
    def __init__(self, bot):
        Data.__init__(self)
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.users = self.retrieve(self.users_path)
        for member in list(self.bot.get_all_members()):
            if str(member.id) not in self.users:
                self.register_user(member, str(member))

    @commands.Cog.listener()
    async def on_member_join(self, member):
        self.users = self.retrieve(self.users_path)
        if str(member.id) not in self.users:
                self.register_user(member, str(member))