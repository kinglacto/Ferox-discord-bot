import json
import random
import threading
import os

import requests
import schedule
from PyDictionary import PyDictionary
from discord import Embed, ButtonStyle
from discord.ui import Button, View
from discord.ext import commands

from data import Data

class Fun(commands.Cog, Data):
    def __init__(self, bot):
        Data.__init__(self)
        self.bot = bot

        self.tenor_api_key = os.getenv('TENOR_API_KEY')

        self.dictionary = PyDictionary()

        self.num_key = {"0":"zero", "1":"one", "2":"two", "3":"three", "4":"four", "5":"five", "6":"six", "7":"seven", "8":"eight", "9":"nine"}
        self.ball_8_answers = self.retrieve(self.ball8_path)
        self.memes = self.retrieve(self.memes_path)

        schedule.every(6).hours.do(self.refresh_memes_database_caller)

    def refresh_memes_database_caller(self):
        threading.Thread(target=self.refresh_memes_database).start()
        
    def refresh_memes_database(self):
        memes = self.memes
        try:
            self.reddit_auth = requests.auth.HTTPBasicAuth(os.getenv('REDDIT_CLIENT_ID'), os.getenv('REDDIT_API_SECRET_KEY'))
            self.reddit_data = {'grant_type': 'password',
                                'username': os.getenv('REDDIT_USERNAME'),
                                'password': os.getenv('REDDIT_PASSWORD')}
            self.headers = {'User-Agent': 'MyAPI/0.0.1'}
            self.reddit_token = requests.post('https://www.reddit.com/api/v1/access_token', auth=self.reddit_auth, data=self.reddit_data, headers=self.headers).json()['access_token']
            self.headers["Authorization"] = f"bearer {self.reddit_token}"
        except:
            return None

        for name in ("memes", "Memes_Of_The_Dank", "MemesIRL", "DankMemesFromSite19", "goodanimemes"):
            for time_frame in ("hour", "day"):
                for listing in ("best", "hot", "top"):
                    try:
                        res = requests.get(f'https://oauth.reddit.com/r/{name}/{listing}.json?limit=100&t={time_frame}', headers=self.headers).json()
                        for post in res["data"]["children"][2:]:
                            try:
                                if "images" in post["data"]["preview"]:
                                    link = post["data"]["url_overridden_by_dest"]
                                    if link not in memes and link[-4:] in (".png", ".jpg"):
                                        memes[link] = post["data"]["title"]
                            except:
                                try:
                                    if "gif" in post["data"]["preview"]["variants"]:
                                        link = post["data"]["preview"]["variants"]["gif"]["source"]["url"]
                                        if link not in memes and link[-4:] in (".gif"):
                                            memes[link] = post["data"]["title"]
                                except:
                                    pass
                    except:
                        pass

        while len(memes) > 500:
            memes.popitem()

        filtered_memes = {}
        for key,value in memes.items():
            if value not in filtered_memes.values():
                filtered_memes[key] = value

        self.update_changes(self.memes_path, filtered_memes)
        self.memes = self.retrieve(self.memes_path)
        
    @commands.command()
    async def meme(self, ctx):
        current_player = ctx.message.author.id

        meme = random.choice(list(self.memes.items()))[0]
        embed = Embed(title=f"**{self.memes[meme]}**", description=Embed.Empty)
        embed.set_image(url=meme)

        buttons = [
            Button(label="Next Meme", style=ButtonStyle.green, custom_id="next", row=0),
            Button(label="End Interaction", style=ButtonStyle.grey, custom_id="end", row=0)
        ]

        class MyView(View):
            def __init__(self):
                super().__init__(timeout=30)

            async def on_timeout(self):
                nonlocal view, embed
                disable_buttons()
                await message.edit(embed=embed, view=view)
        
        def disable_buttons():
            nonlocal view
            view.clear_items()
            buttons = [
                Button(label="Next Meme", style=ButtonStyle.green, custom_id="next", row=0, disabled=True),
                Button(label="End Interaction", style=ButtonStyle.grey, custom_id="end", row=0, disabled=True)
            ]
            for button in buttons:
                button.callback = button_callback
                view.add_item(button)
            view.stop()

        async def button_callback(interaction):
            nonlocal view, message, embed
            if interaction.user.id == current_player:
                button_clicked = interaction.data["custom_id"]
                if button_clicked == "next":
                    meme = random.choice(list(self.memes.items()))[0]
                    embed = Embed(title=f"**{self.memes[meme]}**", description=Embed.Empty)
                    embed.set_image(url=meme)
                    await message.edit(embed=embed, view=view)
                elif button_clicked == "end":
                    disable_buttons()
                    await message.edit(embed=embed, view=view)
            else:
                await interaction.response.send_message(f"These aren't your gifs, use ``pls meme``", ephemeral=True)

        view = MyView()
        for button in buttons:
            button.callback = button_callback
            view.add_item(button)

        message = await ctx.send(embed=embed, view=view)
            
    @commands.command()
    async def gif(self, ctx):
        if self.tenor_api_key == "":
            return None

        search_term = ''.join(list(filter(None, str(ctx.message.content).split(" ")))[2:])

        if search_term == "":
            await ctx.reply("GIF of what bruh")
            return None

        try:
            r = requests.get("https://g.tenor.com/v1/search?q=%s&key=%s&limit=%s" % (search_term, self.tenor_api_key, 1))
        except:
            return None

        if r.status_code == 200:
            gif = json.loads(r.content)['results'][0]['media'][0]['mediumgif']['url']
            embed = Embed(title=f"**{search_term}**", description=Embed.Empty)
            embed.set_image(url=gif)
            await ctx.send(embed=embed)
        else:
            await ctx.reply("I ain't showing you a gif")

    @commands.command()
    async def roll(self, ctx):
        self.users = self.retrieve(self.users_path)
        user_id = str(ctx.message.author.id)
        try:
            wallet = self.users[user_id]["wallet"]
        except:
            self.register_user(ctx.message.author, str(ctx.message.author))
            wallet = self.users[user_id]["wallet"]

        amnt = list(filter(None, str(ctx.message.content).split(" ")))[2]

        if wallet > 0:
            if amnt.isdigit():
                amnt = int(amnt)
                if amnt > wallet:
                    await ctx.reply("You don't even have that much, fool")
                    return None
            elif amnt in ("all", "max"):
                amnt = wallet
            else:
                await ctx.reply("Stop wasting my time with invalid amounts")
                return None

            player = random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
            comp = random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])

            if player > comp:
                self.users[user_id]["wallet"] += amnt 
                self.update_changes(self.users_path, self.users)
                await ctx.reply(f"Banker rolled: ``{comp}`` \nYou rolled: ``{player}`` \nDamn son, you won ${amnt}")
            elif player < comp:
                self.users[user_id]["wallet"] -= amnt 
                self.update_changes(self.users_path, self.users)
                await ctx.reply(f"Banker rolled: ``{comp}`` \nYou rolled: ``{player}`` \nHaha, you lost ${amnt}")
            else:
                await ctx.reply(f"Banker rolled: ``{comp}`` \nYou rolled: ``{player}`` \nwhew, that was a tie")
        else:
            await ctx.reply("You have no money to gamble, you peasant")
    
    @commands.command()
    async def meaning(self, ctx):
        word = list(filter(None, str(ctx.message.content).split(" ")))[2]
        dic = self.dictionary.meaning(word)
        if dic == None:
            await ctx.reply("Not a valid word")
            return None
        doc = f"**__{word}__**\n\n"
        for i in dic:
            doc += f"**{i}**"
            for num, j in enumerate(dic[i]):
                if num == 3:
                    break
                doc += f"\n*{num + 1}) {j}*"    
            doc += "\n\n"
        await ctx.send(doc)

    @commands.command()
    async def emojify(self, ctx):
        sentence = list(filter(None, str(ctx.message.content).split(" ")))[2:]
        doc = ""
        for word in sentence:
            for letter in word:
                if letter.isalpha():
                    doc += f":regional_indicator_{letter.lower()}:"
                elif letter.isdigit():
                    doc += f":{self.num_key[letter]}:"
            doc += "    "
        await ctx.send(doc)

    @commands.command(aliases=["8ball"])
    async def ball_8(self, ctx):
        await ctx.reply(f":8ball: {random.choice(self.ball_8_answers)}")