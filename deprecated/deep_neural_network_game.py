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
    
    # moves = game_state.get_valid_moves()
    
    # values = model.predict(np.array(game_state.board.flatten().reshape(1,20)))
    
    # values = values.tolist()
    # print(values)
    # max_val = max(list(values[0]))
    # col = values[0].index(max_val)
    
    # if col in moves:
    #     row = game_state.get_next_open_row(col)
        
    #     return (row,col)
    # else:
    #     col = random.choice(moves) 
    #     row = game_state.get_next_open_row(col)
    #     return (row,col)
    
    
    moves = game_state.get_valid_moves()
    
    probability_vector = model.predict(np.array(game_state.board.flatten().reshape(1,20)))
    probability_list = probability_vector.tolist()[0]
    
    print(probability_vector)
    print(probability_list)
        # [ 0.3, 0.4, 0.2 0.1 , 0.0 ]
        # to 
        # {
        #     0: 0.3,
        #     1 :0.4
        #     ...
        # }
        
    probability_dict = { index:val for index,val in enumerate(probability_list)}
    print(probability_dict)
        # sorts by value
    prob_dict_sorted = {k: v for k, v in sorted(probability_dict.items(), key=lambda item: item[1], reverse=True)}
    print(prob_dict_sorted)
    
    for column, probability in prob_dict_sorted.items():
        if column in moves:
            row = game_state.get_next_open_row(column)
            
            return (row, column) 
        

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
   
   
def random_move(game_state, coin_type):
    
    moves = game_state.get_valid_moves()
    col = random.choice(moves)
    row = game_state.get_next_open_row(col)
    game_state.drop_piece(row, col, coin_type)
    game_state.check_for_win_and_handle(coin_type)
    game_state.next_turn()
    

def main():
    game_state = game.Game(row_count=4, col_count=5, connect=3)

    ai_agent1 = agent('dfs')
    
    ai_agent2 = agent('bfs')
    
    move_counter_1 = 0
    move_counter_2 = 0
    
    while game_state.game_over != True:
        if game_state.turn == 0:
            game_state.process_events()

            #move1 = agent_move(ai_agent1,game_state)
            
            if move_counter_1 == 0: 
                random_move(game_state,HUMAN)
            else:
                # move2 = neural_network_move(game_state,0.1)
                move1 = agent_move(ai_agent2,game_state)
                game_state.drop_piece(move1[0],move1[1],HUMAN)
                game_state.check_for_win_and_handle(HUMAN)
                game_state.next_turn()
                
            
            # # move_choice = random.choice([move1,move2])
            # print(game_state.print_board())
            
            move_counter_1+=1
            
        else:
            
            if move_counter_2 == 0: 
                random_move(game_state,AI)
            else:
                move2 = neural_network_move(game_state,0.1)
                
                game_state.drop_piece(move2[0],move2[1],AI)
                game_state.check_for_win_and_handle(AI)
                game_state.next_turn()
                print(game_state.print_board())
                
            move_counter_2+=1
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
            
            time.sleep(1)

        

        game_state.draw_board()
        
        if game_state.get_valid_moves() == []:
            game_state.game_over = True

        if game_state.game_over:
            game_state.wait()


if __name__ == '__main__':
    main()
    
