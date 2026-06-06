from dataclasses import dataclass
from dotenv import load_dotenv
from pathlib import Path
import tkinter as tk
import numpy as np
import os

load_dotenv(Path(__file__).with_name("env.txt"))


@dataclass(frozen=True)
class EnvConfig:
    board_size_x: int
    board_size_y: int
    win_length: int

    @classmethod
    def from_env(cls):
        board_size_x = os.getenv("BOARD_SIZE_X")
        if not board_size_x:
            raise ValueError("env.txt is missing a size parameter.")

        board_size_y = os.getenv("BOADR_SIZE_Y")
        if not board_size_y:
            raise ValueError("env.txt is missing a size parameter.")

        win_length = os.getenv("WIN_LENGTH")
        if not win_length:
            raise ValueError("env.txt is missing win length specification.")

        return cls(
            board_size_x=int(board_size_x),
            board_size_y=int(board_size_y),
            win_length=int(win_length)
        )


class Environment:

    def __init__(self):

        self.config = EnvConfig.from_env()

        self.state_vector_X = np.zeros(self.config.board_size_x * self.config.board_size_y)
        self.state_vector_O = np.zeros(self.config.board_size_x * self.config.board_size_y)

        self.root = tk.Tk()
        self.root.title("Gomoku")
        self.current_player = "X"
        self.buttons = []

        self.check_alg = np.array([[0, 1], [1, 0], [1, 1], [1, -1]])

    def is_win_X(self, last_move):

        for check in self.check_alg:
            count = 0

            for i in range(2):
                sub_count = 1

                while (0 <= (last_move + (self.config.board_size_x * check[0] + check[1]) * sub_count * (-1) ** i)
                    < self.config.board_size_x * self.config.board_size_y and (self.state_vector_X[
                    last_move + (self.config.board_size_x * check[0] + check[1]) * sub_count * (-1) ** i] == 1
                    and sub_count < self.config.win_length + 1)):

                    sub_count += 1

                count += sub_count
                if count > self.config.win_length:
                    return True

        return False

    def is_win_O(self, last_move):

        for check in self.check_alg:
            count = 0

            for i in range(2):
                sub_count = 1

                while (0 <= (last_move + (self.config.board_size_x * check[0] + check[1]) * sub_count * (-1) ** i)
                    < self.config.board_size_x * self.config.board_size_y and (self.state_vector_O[
                    last_move + (self.config.board_size_x * check[0] + check[1]) * sub_count * (-1) ** i] == 1
                    and sub_count < self.config.win_length + 1)):
                    sub_count += 1

                count += sub_count
                if count > self.config.win_length:
                    return True

        return False

    def click_input(self, row, col):

        current_player = self.current_player
        button = self.buttons[row][col]

        if button["text"] == "":
            button["text"] = current_player

            if current_player == "X":
                self.current_player = "O"
                self.state_vector_X[row * self.config.board_size_x + col] = 1
                if self.is_win_X(row * self.config.board_size_x + col):
                    print("Congratulations, X wins!")
                    self.root.quit()

            else:
                self.current_player = "X"
                self.state_vector_O[row * self.config.board_size_x + col] = 1
                if self.is_win_O(row * self.config.board_size_x + col):
                    print("Congratulations, O wins!")
                    self.root.quit()

    def visualizer(self):
        for row in range(self.config.board_size_y):
            button_row = []
            for column in range(self.config.board_size_x):
                btn = tk.Button(self.root,
                                font=("Arial", 32),
                                width=5,
                                height=2,
                                command=lambda r=row, c=column: self.click_input(r, c)
                                )
                btn.grid(row=row, column=column)
                button_row.append(btn)
            self.buttons.append(button_row)


game = Environment()
game.visualizer()
game.root.mainloop()
