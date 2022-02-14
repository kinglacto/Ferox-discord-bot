import json
from datetime import datetime
from discord.ext import commands

class Data():
    def __init__(self):
        self.now = datetime.now()
        self.log_file_path = "logs.log"

    def log(self, message):
        try:
            with open(f"{self.log_file_path}", "a") as logs:
                logs.write(self.now.strftime("%d/%m/%Y %H:%M:%S") + f" {message}\n")
        except:
            return None

    def retrieve(self, file_path):
        file_opened = open(f"{file_path}", "r+")
        data_retrieved = json.load(file_opened)
        file_opened.close()
        return data_retrieved

    def update_changes(self, file_path, data):
        file_opened = open(f"{file_path}", "w")
        json.dump(data, file_opened)
        file_opened.close()

    def register(self, user_id, user_name):
        self.users = self.retrieve("data/users.json")
        new_entry = {
            f"{user_id}":
                {
                    "user_name": f"{user_name}",
                    "wallet": 1000,
                    "bank": 10000,
                    "bank_space": 1000000,
                    "investments": []
                }
        }

        users_local_file = open("data/users.json", "r+")
        self.users.update(new_entry)
        users_local_file.seek(0)
        json.dump(self.users, users_local_file)
        users_local_file.close()

    @commands.Cog.listener()
    async def on_ready(self):
        self.users = self.retrieve("data/users.json")
        for member in list(self.bot.get_all_members()):
            if str(member.id) not in self.users:
                self.register(member.id, str(member))

    @commands.Cog.listener()
    async def on_member_join(self, member):
        self.users = self.retrieve("data/users.json")
        if str(member.id) not in self.users:
                self.register(member.id, str(member))