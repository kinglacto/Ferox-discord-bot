import json
from datetime import datetime

class Data():
    def __init__(self):
        self.now = datetime.now()
        self.users_path = "data/users.json"
        self.help_category_path = "data/help_category.json"
        self.help_commands_path = "data/help_commands.json"
        self.ball8_path = "data/8ball.json"
        self.memes_path = "data/memes.json"
        self.runtimes_path = "data/runtimes.json"

    def retrieve(self, file_path):
        file_opened = open(f"{file_path}", "r")
        data_retrieved = json.load(file_opened)
        file_opened.close()
        return data_retrieved

    def update_changes(self, file_path, data):
        file_opened = open(f"{file_path}", "w")
        json.dump(data, file_opened)
        file_opened.close()

    def register_user(self, user, user_name):
        if not user.bot:
            self.users = self.retrieve(self.users_path)
            if user.id not in self.users:
                new_entry = {
                    f"{user.id}":
                        {
                            "user_name": f"{user_name}",
                            "wallet": 1000,
                            "bank": 10000,
                            "bank_space": 1000000,
                            "investments": {}
                        }
                }
                self.users.update(new_entry)
                users_local_file = open(self.users_path, "r+")
                users_local_file.seek(0)
                json.dump(self.users, users_local_file)
                users_local_file.close()
                return True
            return False
        return False