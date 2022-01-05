import json
from pathlib import Path

from .model_hyperparameters import ModelHyperparameters


class ModelConfig:
    __hyperparameters: ModelHyperparameters

    def __init__(self):
        with open(Path(".").joinpath("rota_ai/model_config.json")) as file:
            hyperparameters = json.load(file)["hyperparameters"]

        politic_reward = hyperparameters["politics"]["reward"]
        politic_penalty = hyperparameters["politics"]["penalty"]
        politic_tie = hyperparameters["politics"]["tie"]
        games = hyperparameters["games"]
        max_moves_by_game = hyperparameters["max_moves_by_game"]
        self.__hyperparameters = ModelHyperparameters(politic_reward, politic_penalty, politic_tie, games,
                                                      max_moves_by_game)

    def get_hyperparameters(self) -> ModelHyperparameters:
        return self.__hyperparameters
