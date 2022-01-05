from dataclasses import dataclass

import numpy as np


@dataclass
class PlayerPosition:
    pawn1: np.uint8 = np.ubyte(0)
    pawn2: np.uint8 = np.ubyte(0)
    pawn3: np.uint8 = np.ubyte(0)

    def __init__(self, pawn1: int, pawn2: int, pawn3: int):
        self.pawn1 = np.ubyte(pawn1)
        self.pawn2 = np.ubyte(pawn2)
        self.pawn3 = np.ubyte(pawn3)
