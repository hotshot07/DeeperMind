import math
import game
import copy

class Minimax_agent:
    def __str__(self) -> str:
        return "Minimax Agent"
    
    def __init__(self, agent_number, depth=4) -> None:
        self.agent_number= agent_number
        self.opponent_agent_number = 1 if self.agent_number == 2 else 2
        self.depth = depth
        self.winmap = {
            'Win': 10,
            'Draw': 0,
            'Lose': -10
        }
        self.counter = 0

    def minimax(self, game_state: game.Game, depth, maximizing_player, alpha, beta):
        if depth == 0 or game_state.game_over or game_state.get_valid_moves() == []:
            self.counter += 1
            if game_state.check_for_win(self.opponent_agent_number):
                return self.winmap['Lose']
            if game_state.check_for_win(self.agent_number):
                return self.winmap['Win']
            return self.winmap['Draw']

        score = 0

        #if maximising: find highest evaluation from position
        if maximizing_player:
            max_eval = -math.inf
            #loop through child positions
            for col in game_state.get_valid_moves():
                row = game_state.get_next_open_row(col)
                game_state.board[row][col] = self.agent_number
                score += self.minimax(game_state, depth-1, False, alpha, beta)
                game_state.board[row][col] = 0
                max_eval = max(max_eval,score)
                
                alpha = max(alpha, score)
                if beta<=alpha:
                    break
            return max_eval


        #if minimising: find lowest evaluation from position
        if maximizing_player != True:
            min_eval = math.inf
            #loop through child positions
            for col in game_state.get_valid_moves():
                row = game_state.get_next_open_row(col)
                game_state.board[row][col] = self.opponent_agent_number
                score += self.minimax(game_state, depth-1, True, alpha, beta)
                game_state.board[row][col] = 0
                max_eval = min(min_eval,score)
                
                beta = min(beta, score)
                if beta<=alpha:
                    break
            return max_eval


    def get_best_move(self, game_state: game.Game):
        self.counter = 0
        move = []
        depth = copy.deepcopy(self.depth)
        max_eval = -math.inf
        for col in game_state.get_valid_moves():
            row = game_state.get_next_open_row(col)
            game_state.board[row][col] = self.agent_number
            eval = self.minimax(game_state, depth-1, False, -math.inf, math.inf)
            game_state.board[row][col] = 0
            if eval > max_eval:
                max_eval = eval
                move = [row, col]
            
            #Enbale to show evaluations per move/column
            print(f'Column: {col}, Score: {eval}, Branches explore: {self.counter}')
        
        return move[1]