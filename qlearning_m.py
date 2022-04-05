from email.policy import default
from locale import windows_locale
from utils import *
from copy import deepcopy
import game
import math
import random
from collections import defaultdict
import json
import minimax_agent

class Qlearning():
    def __init__(self, game_state, epsilon=0.2, alpha=0.3, gamma=0.9):
        self.game_state = game_state
        
        self.winmap = {
                    'Win': 10,
                    'Draw': 0,
                    'Lose': -10
                    }
        self.coin_type = 2
        self.q_values = dict()
        self.epsilon = epsilon # e-greedy chance of random exploration
        self.alpha = alpha # learning rate
        self.gamma = gamma # discount factor for future rewards 
        self.discount = 0.8
        
    def getQValue(self, state, action):
        # print(state, action)
        # print(state, action)
        # print(self.q_values[1])
        key = f'{state.flatten().tolist()},{action}'
        if self.q_values.get(key) is None:
            self.q_values[key] = 0
        return(self.q_values[key])  
        
    def computeValueFromQValues(self, state):
        """
          Returns max_action Q(state,action)
          where the max is over legal actions.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return a value of 0.0.
        """
        #creating a list of q values from the current state using legal actions
        
        state = state.flatten()
        
        qvalues = [self.getQValue(state, action) for action in self.game_state.get_valid_moves()]
        #print q_values
        #returning max, default = 0.0
        return max(qvalues, default=0.0)
    
    def computeActionFromQValues(self, state : game.Game):
        """
          Compute the best action to take in a state.  Note that if there
          are no legal actions, which is the case at the terminal state,
          you should return None.
        """
        
        #list of legal actions in a state
        legalActions =  state.get_valid_moves()
        
        #list of tuples of action and q_value 
        action_qvalue = []

        #no legal actions for terminal state, so None
        if not len(legalActions):
            return None

        for action in legalActions:
            # print(state, action)
            action_qvalue.append((action, self.getQValue(state.board, action)))
        
        #print(action_qvalue)
        
        #returning action with max q_value from the list of tuples
        return max(action_qvalue, key=lambda x: x[1])[0]
    
    
    def getAction(self, state):
        """
          Compute the action to take in the current state.  With
          probability self.epsilon, we should take a random action and
          take the best policy action otherwise.  Note that if there are
          no legal actions, which is the case at the terminal state, you
          should choose None as the action.

          HINT: You might want to use util.flipCoin(prob)
          HINT: To pick randomly from a list, use random.choice(list)
        """
        #gets all the legal actions in the current state
        legalActions = state.get_valid_moves()
        # print(legalActions)
        if random.uniform(0,1) < self.epsilon:
            return random.choice(legalActions)
        else:
            #returning the best action if we're not going random
            return self.computeActionFromQValues(state)
    
    def update(self, state, action, nextState, reward):
        """
          The parent class calls this to observe a
          state = action => nextState and reward transition.
          You should do your Q-Value update here

          NOTE: You should never call this function,
          it will be called on your behalf
        """
        # Q(s,a) ← (1−α)Q(s,a)+α ·sample
        # sample=R(s,a,s′)+γmaxQ(s′,a′)
        # algo quite similar to value iteration, position of max is changed
        # pprint(self.q_values)
        key = f'{state.flatten().tolist()},{action}'
        self.q_values[key] = (1-self.alpha) * self.getQValue(state, action) + self.alpha * (reward + self.discount * self.computeValueFromQValues(nextState))

    def getPolicy(self, state):
        # print('policy state',state)
        return self.computeActionFromQValues(state)

    def getValue(self, state):
        return self.computeValueFromQValues(state)
    
    def random_agent(self, game_state: game.Game):
        moves = game_state.get_valid_moves()
        col = random.choice(moves)
        row = game_state.get_next_open_row(col)
        return row, col
    
    def playGame(self):
        
        #change to customisable parameters
        train_game_state = game.Game(row_count=4, col_count=5, connect=3)
        
        human = 1
        # print('playing game')
        while train_game_state.game_over != True:
            #ai turn

            # 1.) get action, or legal action
            col = self.getAction(train_game_state)
            row = train_game_state.get_next_open_row(col)

            # 2.) copy state
            old_state = deepcopy(train_game_state.board)

            #3.) drop_piece
            train_game_state.drop_piece(row, col, self.coin_type)

            #4.) calculate reward
            win = train_game_state.check_for_win(self.coin_type)
            if win:
                reward = 1
                train_game_state.game_over = True
            else:
                reward = 0

            #5.) update qstate
            self.update(old_state, col, train_game_state.board, reward)
            
            
            #6.) other player's turn -> same but for other player
            old_state = deepcopy(train_game_state.board)
            # human_row, human_col = self.random_agent(train_game_state)
            human_row, human_col = minimax_agent.best_move(train_game_state, 4)
            train_game_state.drop_piece(human_row, human_col, human)
            win = train_game_state.check_for_win(self.coin_type)
            if win:
                reward = -1
                train_game_state.game_over = True
            else:
                reward = 0
            self.update(old_state, col, train_game_state.board, reward)

            if train_game_state.get_valid_moves() == []:
                train_game_state.game_over = True




    
    
    def learn(self, iterations):
        iterations = 1000
        for x in range(iterations):
            #iteration = full game
            self.playGame()
            # print(self.q_values)

        
        file = create_json_file()
        file.write(json.dumps(self.q_values))
    # def update(self, chosen_action):
        
    #     state = self.game_state.board.flatten()
        
    #     self.q_values[(state, chosen_action[0])] = (1-self.alpha) * self.getQValue(state, chosen_action[0]) + self.alpha * (reward + self.discount * self.computeValueFromQValues(nextState))
        
        
    def getRandomMove(self):
        
        
        ### update this function to get best play from q learning states 
        moves = self.game_state.get_valid_moves()
        col = random.choice(moves)
        
        # print(self.game_state.board.flatten())
        row = self.game_state.get_next_open_row(col)
        
        action = col 
        # print(action)
        self.game_state.drop_piece(row, col, self.coin_type)
        self.game_state.check_for_win_and_handle(self.coin_type)
        self.game_state.next_turn()
        
        return self.game_state
        
    

def main(training = True):
    game_state = game.Game(row_count=4, col_count=5, connect=3)
    
    qlearning_agent = Qlearning(game_state)
    qlearning_agent.q_values = load_from_json()
    # print(qlearning_agent.q_values)
    if training:
        #should play games against itself and all
        qlearning_agent.learn(iterations = 1)
    
    
    
    while game_state.game_over != True:
        # print('loop')
        if game_state.turn == 0:
            game_state.process_events()
            game_state.draw_board()
        else:
            qlearning_agent.game_state = game_state
            # to be updated by get best move
            # getBestMove()
            # game_state = qlearning_agent.getRandomMove()
            col = qlearning_agent.getPolicy(game_state)
            # print(col)
            row = game_state.get_next_open_row(col)

            if (col,row):
                game_state.drop_piece(row, col, 2)
                game_state.draw_board()
                game_state.check_for_win_and_handle(2)
                game_state.next_turn()
            else:
                #AI cannot win, draw or lost
                # print('forfeit')
                game_state.game_over = True
            
            # print('next')



        game_state.draw_board()
        if game_state.get_valid_moves() == []:
            print('no moves')
            game_state.game_over = True

        if game_state.game_over:
            print('game over')
            game_state.wait()








if __name__ == '__main__':
    main()