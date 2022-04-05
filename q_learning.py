from mysqlx import Column
from utils import *
import game
from minimax_agent import *
import math
import argparse
import numpy as np
import copy
import random

HUMAN = 3
AI = 2
TRAINING = 1

reward = 1
gamma = 1
alpha = 0.8
epsilon = 0.1

q_value_table = {}

def getQValue(state, action):
    if q_value_table.get((state,action)) is None:
        q_value_table[(state,action)] = 0

    return q_value_table[(state,action)]


def computeValueFromQValues(game_state,state):
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
    actions = game_state.get_valid_moves()
    for column_action in actions:
        # column_action is a column number
        # get the q value for that action
        q_value = getQValue(state, column_action)
        if q_value > max_q_value:
            max_q_value = q_value

    return max_q_value


def computeMaxActionFromQValues(game_state,state):
    """
        Compute the best action to take in a state.  Note that if there
        are no legal actions, which is the case at the terminal state,
        you should return None.
    """

    # state is (row,col)
    # for each possible action in the current state
    # find the max q value

    max_q_value = -math.inf
    best_legal_action_in_state = None
    
    actions = game_state.get_valid_moves()
    for column_action in actions:
        # column_action is a column number
        # get the q value for that action
        q_value = getQValue(state, column_action)
        if q_value > max_q_value:
            max_q_value = q_value
            best_legal_action_in_state = column_action

    return best_legal_action_in_state


def computeActionFromQValues(game_state):
    total_q_values = []
    state = copy.deepcopy(game_state.board)

    for action in game_state.get_valid_moves():
        print(type(state))
        state = tuple(map(tuple,state))
        
        print(state)
        print(type(state))
        max_q_value = computeValueFromQValues(game_state,state)
        print('Max Q value: ', max_q_value)
        sample = reward + gamma*max_q_value
        current_q_value = getQValue(state, action)

        q_value = (1-alpha)*current_q_value + alpha*sample

        total_q_values.append([action,q_value])

    return None

def getAction(game_state):
    """
        Compute the action to take in the current state.  With
        probability self.epsilon, we should take a random action and
        take the best policy action otherwise.  Note that if there are
        no legal actions, which is the case at the terminal state, you
        should choose None as the action.

        HINT: You might want to use util.flipCoin(prob)
        HINT: To pick randomly from a list, use random.choice(list)
    """
    # Legal Actions from present state
    legalActions = game_state.get_valid_moves()
    action = None
   
    random_action_probability = util.flipCoin(self.epsilon)
    if random_action_probability is True:
        action = random.choice(legalActions)
    else:
        action = self.computeActionFromQValues(state)

    return action

def update(game_state, state, action):

    reward = 0
    if game_state.game_over == True:
        winner_RL = game_state.check_for_win(1)
        winner_player2 = game_state.check_for_win(2)

        if winner_RL == True:
            reward = 2
        elif winner_player2 == True:
            reward = -2
        else:
            reward = 0.5

    else:
        reward = 0.5

    sample = reward + gamma*computeValueFromQValues(game_state,state)
    new_q_value = (1-alpha)*getQValue(state, action) + alpha*sample
    
    # update q value in q table
    q_value_table[(state,action)] = new_q_value
    print(q_value_table)
 
    return None

def qLearning(game_state, player_type):

    # Sample = R(s,a,s') + gamma*max a'(Q(s',a'))
        # max a'(Q(s',a')) => computeValueFromQValues
        # gamma => Hardcoded
        # R(s,a,s') => Hardcoded. Check if victory
    
    # To update the Q value in the table
    # Q(s,a) <- (1-Alpha)Q(s,a) + (Alpha)(sample)=> computeActionFromQValues
        # Alpha => set manually
        # Q(s,a) => getQValue

    # Max(Q(s,a)) from all possible actions (all columns not already full)
    
    state = copy.deepcopy(game_state.board)
    state = tuple(map(tuple,state))
    best_action = computeMaxActionFromQValues(game_state,state)
    print('Best Action', best_action)
    
    row = game_state.get_next_open_row(best_action)
    print('Row', row)
    update(game_state, state, best_action)

    game_state.drop_piece(row, best_action, player_type)
    game_state.check_for_win_and_handle(player_type)
    game_state.next_turn()

def setUpArgParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('training_mode', type=int, help='Please enter if training (True,False)')
    parser.add_argument('iterations', type=int, help='Please enter if training (True,False)')

    args = parser.parse_args()
    return args

def random_agent(game_state: game.Game):
    moves = game_state.get_valid_moves()
    col = random.choice(moves)
    row = game_state.get_next_open_row(col)
    game_state.drop_piece(row, col, 2)
    game_state.check_for_win_and_handle(2)
    game_state.next_turn()

def main(): # Based on Minimax main()
    args = setUpArgParser()

    game_state = game.Game(row_count=4, col_count=5, connect=3)
    training_mode = args.training_mode
    iterations = args.iterations

    
    # Q-learning algo needs to be the first to make move, otherwise fix the check win
    # logic in the update() function
    
    if training_mode != 1: # Playing against a human
        while game_state.game_over != True:
            if game_state.turn == 0: # 
                qLearning(game_state, AI)
                
                
            else:
                game_state.process_events() #What does this do?
                game_state.draw_board()
        
            game_state.draw_board()
            if game_state.get_valid_moves() == []:
                game_state.game_over = True

            if game_state.game_over:
                game_state.wait()

    else: # Training the Q-learning
        counter = 0
        while (iterations > 0 ):
            iterations = iterations - 1
            game_state = game.Game(row_count=4, col_count=5, connect=3)

            counter = counter + 1
            print("**************ITERATION ", counter, "****************")

            if iterations%2 == 0: # Play against Minimax when even
                while game_state.game_over != True: 
                    if game_state.turn == 0: 
                        qLearning(game_state, TRAINING)
                    else:
                        best_move(game_state, 4) # play it against minimax.
                    
                    game_state.draw_board()
                    if game_state.get_valid_moves() == []:
                        game_state.game_over = True
                        

                    if game_state.game_over:
                        game_state.wait()
            else:
                while game_state.game_over != True:
                    if game_state.turn == 0: 
                        qLearning(game_state, TRAINING)
                    else:
                        random_agent(game_state) # play it against minimax.
                    
                    game_state.draw_board()
                    if game_state.get_valid_moves() == []:
                        game_state.game_over = True
                        

                    if game_state.game_over:
                        game_state.wait()
        
        print('Final Q Table:', print(q_value_table))
                
                
            




if __name__ == "__main__":
    main()