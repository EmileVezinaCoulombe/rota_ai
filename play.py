import rota_game
from rota_ai import RotaAi, ModelConfig

if __name__ == "__main__":
    model_config = ModelConfig()
    game_config = rota_game.GameConfig()
    ai = RotaAi(model_config, game_config)
    ai.Train()
