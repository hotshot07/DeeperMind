import game

#it's you!

class Human_agent:
    def __str__(self) -> str:
        return "Human Agent"
    
    def __init__(self, agent_number) -> None:
        self.agent_number = agent_number

    def get_best_move(self, game_state: game.Game):

        turn = True
        while turn:
            col = game_state.process_events()
            if col is not None:
                turn = False

            game_state.draw_board()
            
        return col