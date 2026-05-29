
from dataclasses import dataclass
from dotenv import load_dotenv
import os

load_dotenv()


@dataclass(frozen=True)
class EnvConfig:
    board_size_x: int
    board_size_y: int
    WIN_LENGTH: int

    @classmethod
    def from_env
