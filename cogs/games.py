from discord.ext import commands
from discord.ui import View
from games.connect4 import Connect4

class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot_id = 931128710524985364
    
    @commands.command(aliases=["c4"])
    async def connect4(self, ctx):
        mentions = ctx.message.mentions
        player = ctx.author.id
        if len(mentions) == 1:
            opponent = mentions[0].id
            if opponent == player:
                await ctx.reply("You can't play with yourself, dunce")
                return None
            opponent_name = mentions[0].name
        elif len(mentions) > 1:
            await ctx.reply("You can't play with multiple people")
            return None
        else:
            opponent = self.bot_id
            opponent_name = self.bot.get_user(self.bot_id).name

        class MyView(View):
            def __init__(self):
                super().__init__(timeout=30)

            async def on_timeout(self):
                connect4.disable()
                await message.edit(content=f"**Don't want to play?\n<@{connect4.previous_player}> won! :partying_face:**\n{connect4.doc}", view=view)
        
        view = MyView()
        connect4 = Connect4(player, opponent, opponent_name, view, ctx)
        message = await ctx.send(connect4.doc, view=view)
        connect4.message = message
    
        if connect4.current_player == self.bot_id:
            j = connect4.get_best_move()[1] + 1
            if connect4.play(j) == False:
                return None
            else:
                await message.edit(content=f"{connect4.doc}")