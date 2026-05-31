from dataclasses import dataclass
from dotenv import load_dotenv
from pathlib import Path
import tkinter as tk
import warnings
import torch
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


def quiet_device_check():
    with warnings.catch_warnings(record=False):
        warnings.filterwarnings(
            action="ignore",
            category=UserWarning
        )
        return torch.accelerator.is_available()


class Environment:

    def __init__(self):

        self.config = EnvConfig.from_env()

        device = "cpu"
        if quiet_device_check():
            self.device = torch.accelerator.current_accelerator()
            print(f"You are using the {device} accelerator.")
        else:
            print("You are using your CPU.")

        self.state_vector_X = torch.zeros(self.config.board_size_x*self.config.board_size_y).to(device)
        self.state_vector_O = torch.zeros(self.config.board_size_x*self.config.board_size_y).to(device)

        self.root = tk.Tk()
        self.root.title("Gomoku")
        self.current_player = "X"
        self.buttons = []


    def is_win(self):
        return


    def click_input(self, row, col):

        current_player = self.current_player
        button = self.buttons[row][col]

        if button["text"] == "":
            button["text"] = current_player
            self.current_player = "O" if current_player == "X" else "X"

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
