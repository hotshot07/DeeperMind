from utils import *
import game
import math
import random


score = {
    'Win': 1,
    'Draw': 0,
    'Lose': -1
}

AI = 2
HUMAN = 1
counter = 0

def minimax(game_state: game.Game, depth, maximizing_player, alpha, beta):
    if depth == 0 or game_state.game_over or game_state.get_valid_moves() == []:
        global counter
        counter += 1
        if game_state.check_for_win(HUMAN):
            return score['Lose']
        if game_state.check_for_win(AI):
            return score['Win']
        return score['Draw']



    #if maximising: find highest evaluation from position
    if maximizing_player:
        max_eval = -math.inf
        #loop through child positions
        for col in game_state.get_valid_moves():
            row = game_state.get_next_open_row(col)
            game_state.board[row][col] = AI
            eval = minimax(game_state, depth-1, False, alpha, beta)
            game_state.board[row][col] = 0
            max_eval = max(max_eval,eval)
            
            alpha = max(alpha, eval)
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
            eval = minimax(game_state, depth-1, True, alpha, beta)
            game_state.board[row][col] = 0
            max_eval = min(min_eval,eval)
            
            beta = min(beta, eval)
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
        # print('eval:', eval, counter)
        print('Branches explored', counter)

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
    game_state = game.Game(row_count=5, col_count=6, connect=4)

    while game_state.game_over != True:
        if game_state.turn == 0:
            game_state.process_events()

            #enable for random agent
            # random_agent(game_state)

            game_state.draw_board()
        else:
            best_move(game_state, 8)
            


        game_state.draw_board()
        if game_state.get_valid_moves() == []:
            game_state.game_over = True

        if game_state.game_over:
            game_state.wait()



if __name__ == '__main__':
    main()