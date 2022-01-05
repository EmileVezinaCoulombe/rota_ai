from itertools import cycle
from typing import List

from rota_game import PlayerPosition, GameState, GameConfig, GameStatus
from .rota_model import RotaModel


class GamePlay:
    __player1: RotaModel
    __player2: RotaModel
    __game_config: GameConfig
    player1_game_states: List[List[int]]
    player2_game_states: List[List[int]]
    game_status: GameStatus
    max_moves: int

    def __init__(self, player1: RotaModel, player2: RotaModel, game_config: GameConfig, max_moves: int):
        self.player1_game_states = []
        self.player2_game_states = []
        self.__player1 = player1
        self.__player2 = player2
        self.__game_config = game_config
        self.game_status = GameStatus.UnResolved
        self.max_moves = max_moves

    def play(self):
        move_count = 1
        is_player1_turn = True
        participant = cycle([self.__player1, self.__player2])
        game_state = GameState(PlayerPosition(0, 0, 0), PlayerPosition(0, 0, 0))
        self.save_states(game_state, is_player1_turn)

        while self.game_status == GameStatus.UnResolved:
            game_state = next(participant).move(game_state)
            self.game_status = self._game_status(game_state, is_player1_turn, move_count)

            # Change turn
            if is_player1_turn:
                print(f"==================\n{self.game_status}\n")
                print(game_state)
            else:
                game_state.change_player()
                print(f"==================\n{self.game_status}\n")
                print(game_state)
                game_state.change_player()
            self.save_states(game_state, is_player1_turn)
            is_player1_turn = not is_player1_turn
            game_state.change_player()
            next(participant)
            move_count += 1

    def swap_game_status(self):
        if self.game_status == GameStatus.PlayerWin:
            self.game_status = GameStatus.OpponentWin
        elif self.game_status == GameStatus.OpponentWin:
            self.game_status = GameStatus.PlayerWin
        elif self.game_status == GameStatus.Tie:
            self.game_status = GameStatus.Tie
        else:
            self.game_status = GameStatus.UnResolved

    def _game_status(self, game_state: GameState, is_player1_turn: bool, move_count: int) -> GameStatus:
        winning_positions = self.__game_config.get_winning_positions()
        player1_positions, player2_positions = game_state.split_state()
        if not is_player1_turn:
            player1_positions, player2_positions = player2_positions, player1_positions

        if sorted(player1_positions) in winning_positions:
            return GameStatus.PlayerWin
        if sorted(player2_positions) in winning_positions:
            return GameStatus.OpponentWin
        if move_count > self.max_moves:
            return GameStatus.Tie
        return GameStatus.UnResolved

    def save_states(self, game_state: GameState, is_player1_turn: bool):
        if is_player1_turn:
            self.player1_game_states.append(game_state.state)
            game_state.change_player()
            self.player2_game_states.append(game_state.state)
            game_state.change_player()
        else:
            game_state.change_player()
            self.player1_game_states.append(game_state.state)
            game_state.change_player()
            self.player2_game_states.append(game_state.state)
