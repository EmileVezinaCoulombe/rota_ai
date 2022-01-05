import numpy as np

from .game_config import GameConfig
from .game_state import GameState


class Moves:
    transitions: np.ndarray
    transitions = np.ones([10, 3])
    transitions[0] = 0

    def __init__(self, game_config: GameConfig, game_state: GameState):
        occupied_places = np.ones(10)
        occupied_places[game_state.state] = 0
        self.transitions = self.transitions * occupied_places[:, np.newaxis]

        for pawn in range(3):
            displacement_available = np.zeros(10)
            pawn_displacement = game_config.get_displacements()[game_state.state[pawn]]
            displacement_available[pawn_displacement] = 1
            self.transitions[:, pawn] = self.transitions[:, pawn] * displacement_available
