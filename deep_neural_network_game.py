from utils import *
import game
import math
import random
from tensorflow import keras
import numpy as np
from minimax_agent import best_move
from basic_search_agent import agent
import time 
model = keras.models.load_model('minimax_neural_75')


AI = 2
HUMAN = 1

def neural_network_move(game_state: game.Game, epsilon):
    
    moves = game_state.get_valid_moves()
    
    values = model.predict(np.array(game_state.board.flatten().reshape(1,20)))
    
    values = values.tolist()
    print(values)
    max_val = max(list(values[0]))
    print(max_val)
    col = values[0].index(max_val)
    
    print(col)
    print(moves)
    
    if col in moves:
        row = game_state.get_next_open_row(col)
        
        return (row,col)
    else:
        col = random.choice(moves) 
        row = game_state.get_next_open_row(col)
        return (row,col)
        

    # if random.random() > epsilon:
    #     if col in moves:
    #         row = game_state.get_next_open_row(col)
    #         game_state.drop_piece(row, col, HUMAN)
    #         game_state.check_for_win_and_handle(HUMAN)
    #         game_state.next_turn()
    # else:
    #     col = random.choice(moves)
    #     row = game_state.get_next_open_row(col)
    #     game_state.drop_piece(row, col, HUMAN)
    #     game_state.check_for_win_and_handle(HUMAN)
    #     game_state.next_turn()

def agent_move(ai_agent,game_state):
    move = ai_agent.get_move(game_state)
    return move 
   
    

def main():
    game_state = game.Game(row_count=4, col_count=5, connect=3)

    ai_agent1 = agent('dfs')
    
    ai_agent2 = agent('bfs')
    
    while game_state.game_over != True:
        if game_state.turn == 0:
            game_state.process_events()

            #move1 = agent_move(ai_agent1,game_state)
            
            move2 = neural_network_move(game_state,0.1)
            
            # # move_choice = random.choice([move1,move2])
            # print(game_state.print_board())
            game_state.drop_piece(move2[0],move2[1],HUMAN)
            game_state.check_for_win_and_handle(HUMAN)
            game_state.next_turn()
            
        else:
            best_move(game_state,9)
            # move = neural_network_move(game_state,0.1)
            # print(move)
            # print(game_state.print_board())
            # game_state.drop_piece(move[0],move[1],AI)
            # game_state.check_for_win_and_handle(AI)
            # game_state.next_turn()
            
            # move2 = agent_move(ai_agent1,game_state)
            # game_state.drop_piece(move1[0],move1[1],HUMAN)
            # game_state.drop_piece(move2[0],move2[1],AI)
            # game_state.check_for_win_and_handle(AI)
            # game_state.next_turn()
            
            time.sleep(2)


        game_state.draw_board()
        
        if game_state.get_valid_moves() == []:
            game_state.game_over = True

        if game_state.game_over:
            game_state.wait()


if __name__ == '__main__':
    main()
    
