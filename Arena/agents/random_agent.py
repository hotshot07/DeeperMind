import game
import random

class Random_agent:
    def __str__(self) -> str:
        return "Random Agent"
    
    def __init__(self, agent_number) -> None:
        self.agent_number = agent_number

    def get_best_move(self, game_state: game.Game):
        moves = game_state.get_valid_moves()
        col = random.choice(moves)
        return col