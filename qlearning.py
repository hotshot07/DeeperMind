from collections import defaultdict
from email.policy import default
from utils import *
import game
import math
import random
from pprint import pprint
 
 
AI = 2
HUMAN = 1
 
class Qlearning():
    def __init__(self, game_state, epsilon=0.2, alpha=0.3, gamma=0.9):
        """
        Initialize a Q-learner with parameters epsilon, alpha and gamma
        and its coin type
        """
        self.game_state = game_state
        self.winmap = {
                    'Win': 10,
                    'Draw': 0,
                    'Lose': -10
                    }
        self.q = {}
        self.epsilon = epsilon # e-greedy chance of random exploration
        self.alpha = alpha # learning rate
        self.gamma = gamma # discount factor for future rewards 
        
    def getQ(self, state, action):
        """
        Return a probability for a given state and action where the greater
        the probability the better the move
        """
        # encourage exploration; "optimistic" 1.0 initial values
        if self.q.get((state, action)) is None:
            self.q[(state, action)] = 1.0

        return self.q.get((state, action))    
        
    def choose_action(self, state, actions):
        """
        Return an action based on the best move recommendation by the current
        Q-Table with a epsilon chance of trying out a new move
        """
        current_state = self.game_state.board 
        
        print(current_state)

        if random.random() < self.epsilon: # explore!
            chosen_action = random.choice(actions)
            return chosen_action

        qs = [self.getQ(current_state, a) for a in actions]
        
        maxQ = max(qs)

        if qs.count(maxQ) > 1:
            # more than 1 best option; choose among them randomly
            best_options = [i for i in range(len(actions)) if qs[i] == maxQ]
            i = random.choice(best_options)
        else:
            i = qs.index(maxQ)

        return actions[i]
    
    def learn(self, board, actions, chosen_action, game_over, game_logic):
        """
        Determine the reward based on its current chosen action and update
        the Q table using the reward recieved and the maximum future reward
        based on the resulting state due to the chosen action
        """
        reward = 0
        sel
        if (self.game_state.game_over):
            if self.game_state.check_for_win(HUMAN):
                return self.winmap['Lose']
            if self.game_state.check_for_win(AI):
                return self.winmap['Win']
            return self.winmap['Draw']
        
        prev_state = board.get_prev_state()
        prev = self.getQ(prev_state, chosen_action)
        result_state = board
        maxqnew = max([self.getQ(result_state, a) for a in actions])
        self.q[(prev_state, chosen_action)] = prev + self.alpha * ((reward + self.gamma*maxqnew) - prev) 
        # print("Q value for " + str(prev_state) + " and " + str(chosen_action) + " is " + str(self.q[(prev_state, chosen_action)]))   
        pprint(self.q)

def main():
    game_state = game.Game(row_count=4, col_count=5, connect=3)

    ############ MAKE AGENT LEARNNNNNN ###########
    
    # playing against a random agent: saving the state+ action as key, 
    # q vlaue as value is a dictionary
    # and basicalllt saving that in a json. 
    
    ##############################################
    
    ######## LOAD Q Values FROM JSON ################
    
    ##### now you can play agianst agent ###########
    
    
    while game_state.game_over != True:
        if game_state.turn == 0:
            game_state.process_events()

            #enable for random agent
            #random_agent(game_state)

            game_state.draw_board()
        else:
            
            for cols in game_state.get_valid_moves():
                row = game_state.get_next_open_row(cols)
                
                print(row,cols)
                
                
            game_state.game_over = True
                

        game_state.draw_board()
        if game_state.get_valid_moves() == []:
            game_state.game_over = True

        if game_state.game_over:
            game_state.wait()
            
            
if __name__ == '__main__':
    main()