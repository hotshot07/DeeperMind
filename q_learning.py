from utils import *
import game
from minimax_agent import *
import math
import argparse
import random

# AI = 2
# HUMAN = 1

HUMAN = 3
AI = 2
TRAINING = 1


q_value_table = {}

def getQValue(state, action):
    # state is (row,col)
    if q_value_table.get((state,action)) is None:
        q_value_table[(state,action)] = 0

    return q_value_table[(state,action)]


def computeValueFromQValues(game_state, state):
    """
    Returns max_action Q(state,action)
    where the max is over legal actions.  Note that if
    there are no legal actions, which is the case at the
    terminal state, you should return a value of 0.0.
    """

    # state is (row,col)
    # for each possible action in the current state
    # find the max q value

    max_q_value = -math.inf

    for column_action in state.get_valid_moves():
        # column_action is a column number
        # get the q value for that action
        q_value = getQValue(state, column_action)
        if q_value > max_q_value:
            max_q_value = q_value

    return None

def qLearning(game_state, player_type):
    row = game_state.get_next_open_row(1)

    game_state.drop_piece(row, 1, player_type)
    game_state.check_for_win_and_handle(player_type)
    game_state.next_turn()

def setUpArgParser():
    parser = argparse.ArgumentParser()
    # parser.add_argument('row_count', type=int, help='Please enter number of rows in board')
    # parser.add_argument('column_count', type=int, help='Please enter number of columns in board')
    # parser.add_argument('connect', type=int, help='Please enter connect value e.x. connect=4 (connect 4)')
    parser.add_argument('training_mode', type=int, help='Please enter if training (True,False)')
    parser.add_argument('iterations', type=int, help='Please enter if training (True,False)')

    args = parser.parse_args()
    return args

def main(): # Based on Minimax main()
    args = setUpArgParser()

    game_state = game.Game(row_count=4, col_count=4, connect=3)
    training_mode = args.training_mode
    iterations = args.iterations
    # training_mode = False
    # iterations = 5

    #### 
    #if its in  training mode, run K number of iterations against a random player 

    #else:
    # human plays against q learing 
    print("Training Mode: ", training_mode)
    print("Iterations: ", iterations)
    if training_mode == 1:
        if iterations%2 == 0: # Play against Minimax when even
            if game_state.turn == 0: 
                None 
            else:
                best_move(game_state, 8) # play it against minimax.
            
        else: # Play against Random Agent when odd
            if game_state.turn == 0: #Taken from basic_search_agent.py main()
                game_state.process_events()
                random_agent(game_state)
                game_state.draw_board()
            
            else: # Q-Learning Turn
                None

    game_state.turn = 0
    while game_state.game_over != True:

        # Playing against a human
        if game_state.turn == 0: # 
            game_state.process_events() #What does this do?
            game_state.draw_board()
            
        else:
            # Call the trainined q-learning table/function
            qLearning(game_state, AI)
        
        game_state.draw_board()
        if game_state.get_valid_moves() == []:
            game_state.game_over = True

        if game_state.game_over:
            game_state.wait()



if __name__ == "__main__":
    main()