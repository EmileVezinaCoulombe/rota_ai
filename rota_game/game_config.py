import json
from pathlib import Path
from typing import List


class GameConfig:
    __displacements: List[List[int]]
    __winning_positions: List[List[int]]

    def __init__(self):
        with open(Path(".").joinpath("rota_game/game_config.json")) as file:
            game_config = json.load(file)
        self.__displacements = [sorted(displacement) for displacement in game_config["displacements"]]
        self.__winning_positions = [sorted(winning_position) for winning_position in game_config["winning_positions"]]

    def get_displacements(self):
        return self.__displacements

    def get_winning_positions(self):
        return self.__winning_positions
