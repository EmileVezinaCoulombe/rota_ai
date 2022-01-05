from itertools import combinations
from typing import Tuple, List, Any

import numpy as np

from rota_game import GameState, PlayerPosition, Moves, GameConfig


class RotaModel:
    __possible_game_states: np
    __probable_moves: np
    __optimal_moves: np

    def __init__(self, game_config: GameConfig):
        participant_positions_combinations = self._positions_combinations()
        combinations_count = len(participant_positions_combinations)
        self.__possible_game_states = np.zeros([combinations_count, 6], dtype=np.ubyte)
        self.__probable_moves = np.zeros([combinations_count, 10, 3], dtype=np.float)

        for index, participant_positions in enumerate(participant_positions_combinations):
            player_positions = PlayerPosition(participant_positions[0],
                                              participant_positions[1],
                                              participant_positions[2])
            opponent_positions = PlayerPosition(participant_positions[3],
                                                participant_positions[4],
                                                participant_positions[5])
            game_state = GameState(player_positions, opponent_positions)
            moves = Moves(game_config, game_state)
            self.__possible_game_states[index, :] = game_state.state
            self.__probable_moves[index, ...] = moves.transitions
        self.update_optimal_moves()

    def predict(self, game_state: GameState):
        game_index = self.get_game_index(game_state.state)
        moves = self.__probable_moves[game_index]
        return self._move_info(moves)

    def move(self, game_state: GameState) -> GameState:
        game_index = self.get_game_index(game_state.state)
        move: Tuple[int, int]
        if sum(game_state.state) == 0:
            pawn_to_move = 0
            place_to_move = np.argmax(self._RotaModel__probable_moves[game_index][:, 0]).item()
            move = (pawn_to_move, place_to_move)
        elif game_state.state[0] != 0 and game_state.state[1] == 0:
            pawn_to_move = 1
            place_to_move = np.argmax(self._RotaModel__probable_moves[game_index][:, 1]).item()
            move = (pawn_to_move, place_to_move)
        elif game_state.state[0] != 0 and game_state.state[1] != 0 and game_state.state[2] == 0:
            pawn_to_move = 2
            place_to_move = np.argmax(self._RotaModel__probable_moves[game_index][:, 2]).item()
            move = (pawn_to_move, place_to_move)
        else:
            move = tuple(self.__optimal_moves[game_index])
        game_state.move(move)
        return game_state

    def update_optimal_moves(self):
        pawn_to_move, place_to_move = self._moving_info()
        self.__optimal_moves = np.array(
            [pawn_to_move, place_to_move]).swapaxes(1, 0)

    def update_probable_moves(self, game_states: List[List[int]], politic: float):
        for state_list in game_states:
            state = np.array(state_list, dtype=np.ubyte)
            game_index = self.get_game_index(state)
            moves = self.__probable_moves[game_index]
            pawn_to_move = np.argmax(np.amax(moves, axis=0)).item()
            place_to_move = np.argmax(moves[:, pawn_to_move]).item()
            self.__probable_moves[game_index][place_to_move][pawn_to_move] += politic

    def _moving_info(self) -> Tuple[np.ndarray, np.ndarray]:
        pawn_to_move = np.argmax(np.amax(self.__probable_moves, axis=1), axis=1)
        probable_move_by_pawns = self.__probable_moves.argmax(axis=1)
        place_to_move = np.array(
            [pawns_move[pawn_to_move[index]] for index, pawns_move in
             enumerate(probable_move_by_pawns)])  # todo: refactor
        return pawn_to_move, place_to_move

    @staticmethod
    def _move_info(moves: np.ndarray) -> Tuple[int, int]:
        pawn_to_move = np.argmax(np.amax(moves, axis=0)).item()
        place_to_move = np.argmax(moves[:, pawn_to_move]).item()
        return pawn_to_move, place_to_move

    def get_game_index(self, state: np.ndarray) -> int:
        return np.where((self.__possible_game_states == state).all(axis=1))[0].item()

    @staticmethod
    def _positions_combinations() -> List[Tuple[Any, ...]]:
        positions_combinations = list(combinations(range(1, 10), 6))

        starting_states = [(0, 0, 0, 0, 0, 0)]

        for first_move in range(1, 10):
            starting_states.append((first_move, 0, 0, 0, 0, 0))
            starting_states.append((0, 0, 0, first_move, 0, 0))

            for second_move in range(1, 10):
                if first_move != second_move:
                    starting_states.append((first_move, 0, 0, second_move, 0, 0))
                    starting_states.append((second_move, 0, 0, first_move, 0, 0))

                for third_move in range(1, 10):
                    if len({first_move, second_move, third_move}) == 3:
                        starting_states.append((first_move, third_move, 0, second_move, 0, 0))
                        starting_states.append((second_move, 0, 0, first_move, third_move, 0))

                    for forth_move in range(1, 10):
                        if len({first_move, second_move, third_move, forth_move}) == 4:
                            starting_states.append((first_move, third_move, 0, second_move, forth_move, 0))
                            starting_states.append((second_move, forth_move, 0, first_move, third_move, 0))

                        for fifth_move in range(1, 10):
                            if len({first_move, second_move, third_move, forth_move, fifth_move}) == 5:
                                starting_states.append((first_move, third_move, fifth_move, second_move, forth_move, 0))
                                starting_states.append((second_move, forth_move, 0, first_move, third_move, fifth_move))

                            for sixth_move in range(1, 10):
                                if len({first_move, second_move, third_move, forth_move, fifth_move, sixth_move}) == 6:
                                    starting_states.append(
                                        (first_move, third_move, fifth_move, second_move, forth_move, sixth_move))
                                    starting_states.append(
                                        (second_move, forth_move, sixth_move, first_move, third_move, fifth_move))

        positions_combinations.extend(starting_states)
        positions_combinations = list(sorted(set(map(tuple, positions_combinations))))

        return positions_combinations
