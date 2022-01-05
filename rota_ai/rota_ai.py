import random
from typing import List, Tuple

from rota_game import GameState, GameConfig, GameStatus
from .game_play import GamePlay
from .model_config import ModelConfig
from .model_hyperparameters import ModelHyperparameters
from .rota_model import RotaModel


class RotaAi:
    __game_config: GameConfig
    __hyperparameters: ModelHyperparameters
    __player: RotaModel
    __opponent: RotaModel

    def __init__(self, model_config: ModelConfig, game_config: GameConfig):
        self.__game_config = game_config
        self.__hyperparameters = model_config.get_hyperparameters()
        self.__player = RotaModel(game_config)
        self.__opponent = RotaModel(game_config)

    def Train(self):

        for epoch in range(self.__hyperparameters.games):
            game_status, player_game_states, opponent_game_states = self._step()
            player_politic = self.__hyperparameters.politic_reward
            opponent_politic = self.__hyperparameters.politic_penalty

            if game_status == GameStatus.OpponentWin:
                player_politic, opponent_politic = opponent_politic, player_politic
            if game_status == GameStatus.Tie:
                player_politic = self.__hyperparameters.politic_tie
                opponent_politic = self.__hyperparameters.politic_tie
            self.__player.update_probable_moves(player_game_states, player_politic)
            self.__player.update_optimal_moves()
            self.__opponent.update_probable_moves(opponent_game_states, opponent_politic)
            self.__opponent.update_optimal_moves()

    def _step(self) -> Tuple[GameStatus, List[List[int]], List[List[int]]]:

        player1 = self.__player
        player2 = self.__opponent
        is_player_start = random.choice([True, False])
        if not is_player_start:
            player1, player2 = player2, player1

        game = GamePlay(player1, player2, self.__game_config, self.__hyperparameters.max_moves_by_game)
        game.play()

        player_game_states = game.player1_game_states
        opponent_game_states = game.player2_game_states
        if not is_player_start:
            player_game_states, opponent_game_states = opponent_game_states, player_game_states
            game.swap_game_status()

        return game.game_status, player_game_states, opponent_game_states

    def move(self, game_states: GameState) -> GameState:
        return self.__player.move(game_states)
