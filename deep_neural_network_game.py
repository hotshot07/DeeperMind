from utils import *
import game
import math
import random
from tensorflow import keras
import numpy as np

model = keras.models.load_model('bfs_iteration_2')


AI = 2
HUMAN = 1

def neural_network_move(game_state: game.Game):
    
    moves = game_state.get_valid_moves()
    
    values = model.predict(np.array(game_state.board.flatten().reshape(1,20)))
    
    values = values.tolist()
    print(values)
    max_val = max(list(values[0]))
    print(max_val)
    col = values[0].index(max_val)
    
    if col in moves:
        row = game_state.get_next_open_row(col)
        game_state.drop_piece(row, col, AI)
        game_state.check_for_win_and_handle(AI)
        game_state.next_turn()
    else:
        col = random.choice(moves)
        row = game_state.get_next_open_row(col)
        game_state.drop_piece(row, col, AI)
        game_state.check_for_win_and_handle(AI)
        game_state.next_turn()


def main():
    game_state = game.Game(row_count=4, col_count=5, connect=3)

    while game_state.game_over != True:
        if game_state.turn == 0:
            game_state.process_events()
            
            game_state.draw_board()
        else:
            neural_network_move(game_state)


        game_state.draw_board()
        
        if game_state.get_valid_moves() == []:
            game_state.game_over = True

        if game_state.game_over:
            game_state.wait()


if __name__ == '__main__':
    main()
    
