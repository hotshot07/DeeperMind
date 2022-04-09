from utils import flipCoin
import game
from minimax_agent_for_q_learning import *
import math
import argparse
import numpy as np
import copy
import random
import json
import os.path

HUMAN = 3
AI = 2
TRAINING = 1

reward = 1
gamma = 1
alpha = 0.3
epsilon = 0.3
q_value_table = {}


def readQTable():
    global q_value_table
    q_value_table_read = {}

    if os.path.exists('Q-tables/q_table_connect3.json'):
        with open("Q-tables/q_table_connect3.json", "r") as f:
            data = json.load(f)
            dic = json.loads(data)
            k = dic.keys()
            v = dic.values()
            k1 = [eval(i) for i in k]
            q_value_table_read = dict(zip(*[k1, v]))

    q_value_table = q_value_table_read


def getQValue(state, action):
    global first_move
    if first_move:
        state = tuple(map(tuple, state))
        if q_value_table.get((state, action)) is None:
            q_value_table[(state, action)] = 50
            first_move = False
    elif q_value_table.get((state, action)) is None:
        q_value_table[(state, action)] = 0

    return q_value_table[(state, action)]


def computeValueFromQValues(game_state, state):
    """
    Returns max_action Q(state,action)
    where the max is over legal actions.  Note that if
    there are no legal actions, which is the case at the
    terminal state, you should return a value of 0.0.
    """
    max_q_value = -math.inf
    actions = game_state.get_valid_moves()
    for column_action in actions:
        q_value = getQValue(state, column_action)
        if q_value > max_q_value:
            max_q_value = q_value

    return max_q_value


def computeMaxActionFromQValues(game_state, state):
    """
        Compute the best action to take in a state.  Note that if there
        are no legal actions, which is the case at the terminal state,
        you should return None.
    """
    # state is (row,col)
    # for each possible action in the current state find the max q value

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
        state = tuple(map(tuple, state))

        max_q_value = computeValueFromQValues(game_state, state)

        sample = reward + gamma*max_q_value
        current_q_value = getQValue(state, action)

        q_value = (1-alpha)*current_q_value + alpha*sample

        total_q_values.append([action, q_value])

    return None


def getAction(game_state, state):
    """
        Compute the action to take in the current state.  With
        probability self.epsilon, we should take a random action and
        take the best policy action otherwise.  Note that if there are
        no legal actions, which is the case at the terminal state, you
        should choose None as the action.
    """
    legalActions = game_state.get_valid_moves()
    print('Legal Actions in get epsilon action', legalActions)
    action = None

    random_action_probability = flipCoin(epsilon)
    if random_action_probability is True:
        action = random.choice(legalActions)
    else:
        action = computeMaxActionFromQValues(game_state, state)

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
    # else:
    #     reward = 0.5

    sample = reward + gamma*computeValueFromQValues(game_state, state)
    new_q_value = (1-alpha)*getQValue(state, action) + alpha*sample

    # update q value in q table
    q_value_table[(state, action)] = new_q_value


def qLearning(game_state, player_type):
    global first_move
    state = copy.deepcopy(game_state.board)
    state = tuple(map(tuple, state))
    
    best_action = getAction(game_state, state)

    row = game_state.get_next_open_row(best_action)
    update(game_state, state, best_action)

    game_state.drop_piece(row, best_action, player_type)
    game_state.check_for_win_and_handle(player_type)
    game_state.next_turn()
    return best_action


def setUpArgParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('training_mode', type=int,
                        help='Please enter if training (True,False)')
    parser.add_argument('iterations', type=int,
                        help='Please enter if training (True,False)')

    args = parser.parse_args()
    return args


def random_agent(q_learning_state, q_learning_action, game_state: game.Game):
    moves = game_state.get_valid_moves()
    col = random.choice(moves)
    row = game_state.get_next_open_row(col)
    game_state.drop_piece(row, col, 2)

    if game_state.game_over == True:
        winner_player2 = game_state.check_for_win(2)
        if winner_player2 == True:

            getQValue(q_learning_state, q_learning_action)
            q_value_table[(q_learning_state,
                           q_learning_action)] = -2
            q_value_table[(q_learning_state,
                           col)] = 1.5

    game_state.check_for_win_and_handle(2)
    game_state.next_turn()
    return col


def main():  # Based on Minimax main()
    global epsilon, first_move

    # read in Q value table
    # readQTable()

    args = setUpArgParser()
    game_state = game.Game(row_count=6, col_count=7, connect=4)
    training_mode = args.training_mode
    iterations = args.iterations
    first_move = True

    epsilon_decay_counter = 0
    win_counter_RL_against_minimax = 0
    loss_counter_RL_against_minimax = 0
    win_counter_RL_against_random = 0
    loss_counter_RL_against_random = 0

    if training_mode != 1:  # Playing against a human
        while game_state.game_over != True:
            if game_state.turn == 0:
                qLearning(game_state, TRAINING)

            else:
                game_state.process_events()
                game_state.draw_board()

            game_state.draw_board()
            if game_state.get_valid_moves() == []:
                game_state.game_over = True

            if game_state.game_over:
                game_state.wait()

    else:  # Training the Q-learning
        initial_state = copy.deepcopy(game_state.board)
        getQValue(initial_state, math.floor(game_state.col_count/2))
        print(q_value_table)
        q_learning_state = None
        q_learning_action = None
        while (iterations > 0):
            iterations = iterations - 1
            #game_state = game.Game(row_count=4, col_count=5, connect=3)

            epsilon_decay_counter += 1
            if epsilon_decay_counter == 100 and epsilon > 0.01:
                epsilon -= 0.018
                epsilon_decay_counter = 0

            print("**************ITERATION ", iterations,
                  "****************", epsilon)

            if iterations % 2 == 0:  # Play against Minimax when even
                print("**************ITERATION ", iterations,
                      "****************", epsilon)
                while game_state.game_over != True:
                    print("**************ITERATION ", iterations,
                          "****************", epsilon)
                    if game_state.turn == 0:
                        q_learning_state = tuple(
                            map(tuple, copy.deepcopy(game_state.board)))
                        q_learning_action = qLearning(game_state, TRAINING)
                    else:
                        # play it against minimax.
                        action_minimax = best_move(game_state, 4)

                        # If the previous q-learning action did not prevent minimax from winning, assign negative reward to the previous q-learning action
                        if game_state.game_over == True:
                            winner_player2 = game_state.check_for_win(2)
                            if winner_player2 == True:

                                getQValue(q_learning_state, q_learning_action)
                                q_value_table[(q_learning_state,
                                               q_learning_action)] = -2
                                q_value_table[(q_learning_state,
                                               action_minimax)] = 1.5

                    game_state.draw_board()
                    if game_state.get_valid_moves() == []:
                        game_state.game_over = True

                    if game_state.game_over:
                        game_state.wait()

                if game_state.check_for_win(1):
                    win_counter_RL_against_minimax = win_counter_RL_against_minimax + 1
                elif game_state.check_for_win(2):
                    loss_counter_RL_against_minimax = loss_counter_RL_against_minimax + 1

            else:
                q_learning_state_random_agent = None
                q_learning_action_random_agent = None
                while game_state.game_over != True:
                    print("**************ITERATION ", iterations,
                          "****************", epsilon)
                    if game_state.turn == 0:
                        q_learning_state_random_agent = tuple(
                            map(tuple, copy.deepcopy(game_state.board)))
                        q_learning_action_random_agent = qLearning(
                            game_state, TRAINING)
                    else:
                        rand_ag_action = random_agent(
                            q_learning_state_random_agent, q_learning_action_random_agent, game_state)  # play it against random
                        if game_state.game_over == True:
                            winner_player2 = game_state.check_for_win(2)
                            if winner_player2 == True:

                                getQValue(q_learning_state_random_agent,
                                          q_learning_action_random_agent)
                                q_value_table[(
                                    q_learning_state_random_agent, q_learning_action_random_agent)] = -2

                                q_value_table[(
                                    q_learning_state_random_agent, rand_ag_action)] = 1.5

                    game_state.draw_board()
                    if game_state.get_valid_moves() == []:
                        game_state.game_over = True

                    if game_state.game_over:
                        game_state.wait()

                if game_state.check_for_win(1):
                    win_counter_RL_against_random += 1
                elif game_state.check_for_win(2):
                    loss_counter_RL_against_random += 1

        # print('Final Q Table:', print(q_value_table))
        print('Game Summary ~~~~~~~~~~~~~~~')
        print('MINIMAX')
        print('\t Wins Against:', win_counter_RL_against_minimax)
        print('\t Losses Against:', loss_counter_RL_against_minimax)
        print('RANDOM AGENT')
        print('\t Wins Against:', win_counter_RL_against_random)
        print('\t Losses Against:', loss_counter_RL_against_random)

        # with open("Q-tables/q_table_connect3xx.json", "w") as f:
        #     k = q_value_table.keys()
        #     v = q_value_table.values()
        #     k1 = [str(i) for i in k]
        #     json.dump(json.dumps(dict(zip(*[k1, v]))), f)


if __name__ == "__main__":
    main()
