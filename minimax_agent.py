from utils import *
import game
import math
import random
import numpy as np
import csv
import time 

winmap = {
    'Win': 10,
    'Draw': 0,
    'Lose': -10
}

AI = 2
HUMAN = 1
counter = 0

class Minimax_Agent:
    def __init__(self, file) -> None:
        self.actions = []
        self.file = file
    
    def minimax(self, game_state: game.Game, depth, maximizing_player, alpha, beta):
        if depth == 0 or game_state.game_over or game_state.get_valid_moves() == []:
            global counter
            counter += 1
            if game_state.check_for_win(HUMAN):
                return winmap['Lose']
            if game_state.check_for_win(AI):
                return winmap['Win']
            return winmap['Draw']

        score = 0

        #if maximising: find highest evaluation from position
        if maximizing_player:
            max_eval = -math.inf
            #loop through child positions
            for col in game_state.get_valid_moves():
                row = game_state.get_next_open_row(col)
                game_state.board[row][col] = AI
                score += minimax(game_state, depth-1, False, alpha, beta)
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
                game_state.board[row][col] = HUMAN
                score += minimax(game_state, depth-1, True, alpha, beta)
                game_state.board[row][col] = 0
                max_eval = min(min_eval,score)
                
                beta = min(beta, score)
                if beta<=alpha:
                    break
            return max_eval


    def best_move(self, game_state: game.Game, depth):
        # global move
        global counter
        counter = 0
        move = []
        max_eval = -math.inf
        for col in game_state.get_valid_moves():
            row = game_state.get_next_open_row(col)
            game_state.board[row][col] = AI
            eval = minimax(game_state, depth-1, False, -math.inf, math.inf)
            game_state.board[row][col] = 0
            if eval > max_eval:
                max_eval = eval
                move = [row, col]
            
            #Enbale to show evaluations per move/column
            print(f'Column: {col}, Score: {eval}, Branches explore: {counter}')
        
        print('Move:', move)
        self.append_actions(game_state.board, move[1], game_state.col_count)
        game_state.drop_piece(move[0], move[1], AI)
        
        if game_state.check_for_win(AI):
            self.export_moves_to_csv()
            self.empty_actions()

        game_state.next_turn()


    def append_actions(self, board, col, col_count):
        action = np.zeros(col_count)
        action = action.flatten().tolist()
        action[col] = 1
        state = board.flatten().tolist()
        self.actions.append((state,action))


    def export_moves_to_csv(self):
        csv_writer = csv.writer(self.file)
        for action in self.actions:
            csv_writer.writerow([action[0]] + [action[1]])
    

    def empty_actions(self):
        #clear recorded actions
        self.actions = []
    
    



#leaving this here so it doesn't break existing code
def minimax(game_state: game.Game, depth, maximizing_player, alpha, beta):
    if depth == 0 or game_state.game_over or game_state.get_valid_moves() == []:
        global counter
        counter += 1
        if game_state.check_for_win(HUMAN):
            return winmap['Lose']
        if game_state.check_for_win(AI):
            return winmap['Win']
        return winmap['Draw']

    score = 0

    #if maximising: find highest evaluation from position
    if maximizing_player:
        max_eval = -math.inf
        #loop through child positions
        for col in game_state.get_valid_moves():
            row = game_state.get_next_open_row(col)
            game_state.board[row][col] = AI
            score += minimax(game_state, depth-1, False, alpha, beta)
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
            game_state.board[row][col] = HUMAN
            score += minimax(game_state, depth-1, True, alpha, beta)
            game_state.board[row][col] = 0
            max_eval = min(min_eval,score)
            
            beta = min(beta, score)
            if beta<=alpha:
                break
        return max_eval


def best_move(game_state: game.Game, depth):
    # global move
    global counter
    counter = 0
    move = []
    max_eval = -math.inf
    for col in game_state.get_valid_moves():
        row = game_state.get_next_open_row(col)
        game_state.board[row][col] = AI
        eval = minimax(game_state, depth-1, False, -math.inf, math.inf)
        game_state.board[row][col] = 0
        if eval > max_eval:
            max_eval = eval
            move = [row, col]
        
        #Enbale to show evaluations per move/column
        print(f'Column: {col}, Score: {eval}, Branches explore: {counter}')

    game_state.drop_piece(move[0], move[1], AI)
    game_state.check_for_win_and_handle(AI)
    game_state.next_turn()

def random_agent(game_state: game.Game):
    moves = game_state.get_valid_moves()
    col = random.choice(moves)
    row = game_state.get_next_open_row(col)
    game_state.drop_piece(row, col, HUMAN)
    game_state.check_for_win_and_handle(HUMAN)
    game_state.next_turn()

def main():
    # game_state = game.Game(row_count=4, col_count=5, connect=3)
    start = time.time()
    file = create_file(name='minimax_moves')
    csv_writer = csv.writer(file)
    csv_writer.writerow(['state']+['action'] )

    for i in range(5000):
        game_state = game_state = game.Game(row_count=4, col_count=5, connect=3)
        minimax_agent = Minimax_Agent(file=file)

        while game_state.game_over != True:
            if game_state.turn == 0:
                game_state.process_events()

                #enable for random agent
                random_agent(game_state)

                game_state.draw_board()
            else:

                #minimax's turn
                minimax_agent.best_move(game_state, 7)


            game_state.draw_board()
            if game_state.get_valid_moves() == []:
                game_state.game_over = True
                minimax_agent.empty_actions()

            if game_state.game_over:
                # game_state.wait()
                minimax_agent.empty_actions()
    
    end = time.time() - start 
    
    print("total time:", end)



if __name__ == '__main__':
    main()