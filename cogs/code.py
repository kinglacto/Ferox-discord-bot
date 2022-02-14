import requests
from cogs.data import Data
from discord.ext import commands

class Code(commands.Cog, Data):
    def __init__(self, bot):
        Data.__init__(self)
        self.bot = bot
        self.runtimes = self.retrieve("data\\runtimes.json")

    @commands.command()
    async def run(self, ctx):
        content = ctx.message.content
        split_list = content.split("```")

        if len(split_list) < 3:
            await ctx.reply("Please paste your code within code blocks")
            return None
        else:
            try:
                code = split_list[1][split_list[1].index("\n"):]
            except:
                await ctx.reply("Please paste your code within code blocks")
                return None
            arg = ""
            try:
                arg = split_list[2][split_list[2].index("\n") + 1:]
            except:
                pass
        
        try:
            language = list(filter(None, str(content).split("```")))[0].split(" ")[2][:-1]
        except:
            await ctx.reply("Please specify a valid language")
            return None

        for entry in self.runtimes:
            if (language == entry["language"]) or (language in entry["aliases"]):
                version = entry["version"]
                break
        else:
            await ctx.reply("Invalid language")
            return None

        payload = {
            "language":language,
            "version":version,
            "files":
            [
                {
                    "content": code
                }
            ],
            "stdin": arg

        }
        res = requests.post(
            url='https://emkc.org/api/v2/piston/execute',
            json=payload).json()
            
        output = res["run"]["stdout"]
        if output == "":
            error = res["run"]["stderr"]
            await ctx.send(f"<@{ctx.message.author.id}> I received an error ```Traceback (most recent call last): \n{error}\n```")
        else:
            await ctx.send(f"Here is your output <@{ctx.message.author.id}> ```\n{output}\n```")