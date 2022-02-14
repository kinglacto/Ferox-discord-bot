from discord import ButtonStyle
from discord.ui import Button
import random

class Connect4():
    def __init__(self, player, opponent, opponent_name, view, ctx,board=None, turn=None) -> None:
        if board == None or turn == None:
            self.reset()
        else:
            self.board = board
            self.turn = turn

        self.player = player
        self.opponent = opponent
        self.opponent_name = opponent_name
        self.view = view
        self.ctx = ctx

        self.message = None
        self.bot_id = 931128710524985364
        self.win_amount = 50000
        self.red_circle = "🔴"
        self.yellow_circle = "🟡"
        self.white_circle = "⚪"
        self.current_player = random.choice((self.player, self.opponent))
        self.previous_player = player if self.current_player == self.opponent else self.opponent
        self.doc = ""

        self.buttons = [
            Button(label="1", style=ButtonStyle.blurple, custom_id="1", row=0),
            Button(label="2", style=ButtonStyle.blurple, custom_id="2", row=0),
            Button(label="3", style=ButtonStyle.blurple, custom_id="3", row=0),
            Button(label="4", style=ButtonStyle.blurple, custom_id="4", row=0),
            Button(label="5", style=ButtonStyle.blurple, custom_id="5", row=1),
            Button(label="6", style=ButtonStyle.blurple, custom_id="6", row=1),
            Button(label="7", style=ButtonStyle.blurple, custom_id="7", row=1),
        ]

        for button in self.buttons:
            button.callback = self.button_callback
            self.view.add_item(button)
        
        self.play("initial_message")

    async def button_callback(self, interaction):
        if interaction.user.id == self.current_player:
            button_clicked = interaction.data["custom_id"]
            if self.play(button_clicked) == False:
                await interaction.response.send_message(f"Invalid move, try again", ephemeral=True)
                return None
            else:
                await self.message.edit(content=f"{self.doc}")

            if self.is_draw():
                self.disable()
                await self.message.edit(content=f"**Game has ended in a draw!\n{self.doc}", view=self.view)
                return None
            elif self.check_for_winner() in (1, -1):
                self.disable()
                await self.message.edit(content=f"**Game over! <@{self.previous_player}> won! :partying_face:**\n{self.doc}", view=self.view)
                return None

            if self.current_player == self.bot_id:
                j = self.get_best_move()[1] + 1
                if self.play(j) == False:
                    return None
                else:
                    await self.message.edit(content=f"{self.doc}")

                if self.is_draw():
                    self.disable()
                    await self.message.edit(content=f"**Game has ended in a draw!\n{self.doc}", view=self.view)
                    return None
                elif self.check_for_winner() in (1, -1):
                    self.disable()
                    await self.message.edit(content=f"**Game over! <@{self.previous_player}> won! :partying_face:**\n{self.doc}", view=self.view)
                    return None


        elif interaction.user.id in (self.player, self.opponent):
            await interaction.response.send_message(f"It isn't your turn!", ephemeral=True)
        else:
            await interaction.response.send_message(f"This isn't your game! use ``pls c4`` to start your own", ephemeral=True)

    def play(self, button_clicked):
        if button_clicked != "initial_message":
            column = int(button_clicked) - 1
            for row in range(5, -1, -1):
                if self.board[row][column] == 0:
                    break
            else:
                return False

            possible = self.make_move((row, column))
            if not possible:
                return False
            else:
                self.current_player = self.player if self.current_player == self.opponent else self.opponent
                self.previous_player = self.player if self.current_player == self.opponent else self.opponent

        header = f"**{self.ctx.author.name} vs. {self.opponent_name}**\n\nYour move <@{self.current_player}> {self.red_circle if self.turn == 1 else self.yellow_circle}\nYou have 30 seconds!"
        numbers_str = "\n\n:one:  :two:  :three:  :four:  :five:  :six:  :seven:"
        board = "\n"
        for i in range(6):
            board += "\n"
            for j in range(7):
                if self.board[i][j] == 1:
                    circle = self.red_circle
                elif self.board[i][j] == -1:
                    circle = self.yellow_circle
                elif self.board[i][j] == 0:
                    circle = self.white_circle
                board += f"{circle}  "

        self.doc = header + numbers_str + board
        return True

    def disable(self):
        self.view.clear_items()
        self.buttons = [
            Button(label="1", style=ButtonStyle.blurple, custom_id="1", row=0, disabled=True),
            Button(label="2", style=ButtonStyle.blurple, custom_id="2", row=0, disabled=True),
            Button(label="3", style=ButtonStyle.blurple, custom_id="3", row=0, disabled=True),
            Button(label="4", style=ButtonStyle.blurple, custom_id="4", row=0, disabled=True),
            Button(label="5", style=ButtonStyle.blurple, custom_id="5", row=1, disabled=True),
            Button(label="6", style=ButtonStyle.blurple, custom_id="6", row=1, disabled=True),
            Button(label="7", style=ButtonStyle.blurple, custom_id="7", row=1, disabled=True),
        ]
        for button in self.buttons:
            button.callback = self.button_callback
            self.view.add_item(button)
        self.view.stop()

    def reset(self) -> None:
        self.turn = 1
        self.board = [[0 for _ in range(7)] for __ in range(6)]

    def is_valid(self, s) -> bool:
        i, j = s[0], s[1]
        try:
            if self.board[i][j] == 0:
                if i == 5:
                    return True
                else:
                    if self.board[i + 1][j] in (1, -1):
                        return True
        except IndexError:
            return False
        return False

    def is_draw(self) -> bool:
        for i in range(6):
            for j in range(7):
                if self.board[i][j] == 0:
                    return False
        return True
    
    def check_for_winner(self) -> int:
        for i in range(6):
            for j in range(7):
                if self.board[i][j] in (1, -1):
                    if i <= 2 and (self.board[i][j] == self.board[i + 1][j] == self.board[i + 2][j] == self.board[i + 3][j]):
                        return self.board[i][j]
                    elif i >= 3 and (self.board[i][j] == self.board[i - 1][j] == self.board[i - 2][j] == self.board[i - 3][j]):
                        return self.board[i][j]
                    elif j <= 3 and (self.board[i][j] == self.board[i][j + 1] == self.board[i][j + 2] == self.board[i][j + 3]):
                        return self.board[i][j]
                    elif j >= 3 and self.board[i][j] == self.board[i][j - 1] == self.board[i][j - 2] == self.board[i][j - 3]:
                        return self.board[i][j]
                    elif i <= 2 and j <= 3 and (self.board[i][j] == self.board[i + 1][j + 1] == self.board[i + 2][j + 2] == self.board[i + 3][j + 3]):
                        return self.board[i][j]
                    elif i >= 3 and j >= 3 and (self.board[i][j] == self.board[i - 1][j - 1] == self.board[i - 2][j - 2] == self.board[i - 3][j - 3]):
                        return self.board[i][j]
                    elif i <= 2 and j >= 3 and (self.board[i][j] == self.board[i + 1][j - 1] == self.board[i + 2][j - 2] == self.board[i + 3][j - 3]):
                        return self.board[i][j]
                    elif i >= 3 and j <= 3 and (self.board[i][j] == self.board[i - 1][j + 1] == self.board[i - 2][j + 2] == self.board[i - 3][j + 3]):
                        return self.board[i][j]
        return 0

    def make_move(self, s) -> bool:
        if self.is_valid(s):
            i, j = s
            self.board[i][j] = self.turn
            self.turn *= -1
            return True
        return False

    def get_all_valid_moves(self) -> list:
        valid_moves = []
        for i in range(6):
            for j in range(7):
                if self.is_valid((i, j)):
                    valid_moves.append((i, j))
        return valid_moves

    def get_best_move(self) -> tuple:
        self.opponent_color = self.turn * -1
        return self.minimax(5, -10000000, 10000000, True)[1]

    def minimax(self, depth, alpha, beta, is_maximising) -> list:
        all_valid_moves = self.get_all_valid_moves()
        winner = self.check_for_winner()
        is_draw = self.is_draw()
        
        if depth == 0 or (winner in (1, -1) or is_draw):
            if winner == self.turn:
                return 100000, None
            elif winner == self.opponent_color:
                return -100000, None
            elif is_draw:
                return 0, None
            else:
                return self.heuristic(), None

        if is_maximising:
            best_score = -10000000
            best_move = None
            for move in all_valid_moves:
                self.board[move[0]][move[1]] = self.turn
                score = self.minimax(depth - 1, alpha, beta, False)[0]
                self.board[move[0]][move[1]] = 0
                if score > best_score:
                    best_score = score
                    best_move = move
                alpha = max(alpha, best_score)
                if alpha >= beta:
                    break
            return best_score, best_move
        
        else:
            best_score = 10000000
            best_move = None
            for move in all_valid_moves:
                self.board[move[0]][move[1]] = self.opponent_color
                score = self.minimax(depth - 1, alpha, beta, True)[0]
                self.board[move[0]][move[1]] = 0
                if score < best_score:
                    best_score = score
                    best_move = move
                beta = min(beta, best_score)
                if alpha >= beta:
                    break
            return best_score, best_move

    def heuristic(self) -> int:
        score = 0
        if self.board[5][3] == 0:
            score += 1000
        elif self.board[5][3] == self.opponent_color:
            score -= 1000

        for i in range(6):
            if self.board[i][4] == 0:
                score += 100

        if self.board[0][0] == 0 or self.board[0][6] == 0 or self.board[5][0] == 0 or self.board[5][6] == 0:
            score += 10
        if self.board[0][0] == self.opponent_color or self.board[0][6] == self.opponent_color or self.board[5][0] == self.opponent_color or self.board[5][6] == self.opponent_color:
            score += 10

        for i in range(6):
            for j in range(7):
                n = 1 if self.board[i][j] == self.turn else -1
                if i <= 4 and (self.board[i][j] == self.board[i + 1][j] != 0) and (self.is_valid((i + 2, j)) or self.is_valid((i - 1, j))):
                    score += n * 100
                if i <= 3 and (self.board[i][j] == self.board[i + 1][j] == self.board[i + 2][j] != 0) and (self.is_valid((i + 3, j)) or self.is_valid((i - 1, j))):
                    score += n * 100
                if i >= 1 and (self.board[i][j] == self.board[i - 1][j] != 0) and (self.is_valid((i - 2, j)) or self.is_valid((i + 1, j))):
                    score += n * 100
                if i >= 2 and (self.board[i][j] == self.board[i - 1][j] == self.board[i - 2][j] != 0) and (self.is_valid((i - 3, j)) or self.is_valid((i + 1, j))):
                    score += n * 100
                if j <= 5 and (self.board[i][j] == self.board[i][j + 1] != 0) and (self.is_valid((i, j + 2))):
                    score += n * 50
                if j <= 4 and (self.board[i][j] == self.board[i][j + 1] == self.board[i][j + 2] != 0) and (self.is_valid((i, j + 3))):
                    score += n * 100
                if i <= 4 and j <= 5 and (self.board[i][j] == self.board[i + 1][j + 1] != 0) and (self.is_valid((i + 2, j + 2))):
                    score += n * 50
                if i <= 3 and j <= 3 and (self.board[i][j] == self.board[i + 1][j + 1] == self.board[i + 2][j + 2] != 0) and (self.is_valid((i + 3, j + 3))):
                    score += n * 100
                if i >= 1 and j >= 1 and (self.board[i][j] == self.board[i - 1][j - 1] != 0) and (self.is_valid((i - 2, j - 2))):
                    score += n * 50
                if i >= 2 and j >= 2 and (self.board[i][j] == self.board[i - 1][j - 1] == self.board[i - 2][j - 2] != 0) and (self.is_valid((i - 3, j - 3))):
                    score += n * 100
                if i <= 4 and j >= 1 and (self.board[i][j] == self.board[i + 1][j - 1] != 0) and (self.is_valid((i + 2, j - 2))):
                    score += n * 50
                if i <= 3 and j <= 4 and (self.board[i][j] == self.board[i + 1][j - 1] == self.board[i + 2][j - 2] != 0) and (self.is_valid((i + 3, j - 3))):
                    score += n * 100
                if i >= 1 and j <= 5 and (self.board[i][j] == self.board[i - 1][j + 1] != 0) and (self.is_valid((i - 2, j + 2))):
                    score += n * 50
                if i >= 2 and j <= 4 and (self.board[i][j] == self.board[i - 1][j + 1] == self.board[i - 2][j + 2] != 0) and (self.is_valid((i - 3, j + 3))):
                    score += n * 100
        return score