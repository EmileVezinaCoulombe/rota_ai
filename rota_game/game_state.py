from typing import Tuple, List

import numpy as np

from .player_position import PlayerPosition


class GameState:
    state: np.ndarray

    def __init__(self, player_positions: PlayerPosition, opponent_positions: PlayerPosition):
        self.state = np.zeros(shape=6, dtype=np.ubyte)

        for index, position in zip([range(0, 3), range(3, 6)], [player_positions, opponent_positions]):
            self.state[index[0]] = position.pawn1
            self.state[index[1]] = position.pawn2
            self.state[index[2]] = position.pawn3

    def __str__(self):
        board: np.ndarray = np.full(10, " ")
        board[self.state[0:3][self.state[0:3].nonzero()] - 1] = "X"
        board[self.state[3:6][self.state[3:6].nonzero()] - 1] = "O"
        formatted_board = ""
        separator = "\n-----\n"
        for y in range(0, 7, 3):
            formatted_board += "|".join(board[y:y + 3].tolist())
            formatted_board += separator
        formatted_board = formatted_board[:-6]
        return formatted_board

    def move(self, move: Tuple[int, int]):
        if move[0] not in range(0, 6):
            raise ValueError(f"Can't move the pawn number {move[0]}")
        if move[1] in self.state:
            raise ValueError(f"The position {move[1]} is already occupied")
        self.state[move[0]] = move[1]

    def change_player(self):
        player1: np.ndarray = self.state[0:3]
        player2: np.ndarray = self.state[3:6]
        self.state = np.append(player2, player1)

    def split_state(self) -> Tuple[List[int], List[int]]:
        player1: List[int] = self.state[0:3].tolist()
        player2: List[int] = self.state[3:6].tolist()
        return player1, player2
