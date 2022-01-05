from enum import Enum


class GameStatus(Enum):
    PlayerWin = 0
    OpponentWin = 1
    Tie = 2
    UnResolved = 3
