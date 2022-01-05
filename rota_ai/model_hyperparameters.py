from dataclasses import dataclass


@dataclass()
class ModelHyperparameters:
    politic_reward: float
    politic_penalty: float
    politic_tie: float
    games: int
    max_moves_by_game: int
