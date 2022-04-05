from utils import *
import game
import math
import random
from collections import defaultdict

class Qlearning():
    def __init__(self, game_state, epsilon=0.2, alpha=0.3, gamma=0.9):
        self.game_state = game_state
        self.winmap = {
                    'Win': 10,
                    'Draw': 0,
                    'Lose': -10
                    }
        self.coin_type = 2
        self.q_values = defaultdict(0)
        self.epsilon = epsilon # e-greedy chance of random exploration
        self.alpha = alpha # learning rate
        self.gamma = gamma # discount factor for future rewards 
        
    def getQValue(self, state, action):
        return(self.q_values[(state,action)])  
        
    def computeValueFromQValues(self):
        """
          Returns max_action Q(state,action)
          where the max is over legal actions.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return a value of 0.0.
        """
        #creating a list of q values from the current state using legal actions
        
        state = self.game_state.board.flatten()
        
        qvalues = [self.getQValue(state, action) for action in self.game_state.get_valid_moves()]
        #print q_values
        #returning max, default = 0.0
        return max(qvalues, default=0.0)
    
    def computeActionFromQValues(self, state):
        """
          Compute the best action to take in a state.  Note that if there
          are no legal actions, which is the case at the terminal state,
          you should return None.
        """
        
        #list of legal actions in a state
        legalActions =  self.game_state.get_valid_moves()
        
        #list of tuples of action and q_value 
        action_qvalue = []

        #no legal actions for terminal state, so None
        if not len(legalActions):
            return None

        for action in legalActions:
            action_qvalue.append((action, self.getQValue(state, action)))
        
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
        legalActions = self.getLegalActions(state)

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
        self.q_values[(state, action)] = (1-self.alpha) * self.getQValue(state, action) + self.alpha * (reward + self.discount * self.computeValueFromQValues(nextState))

    def getPolicy(self, state):
        return self.computeActionFromQValues(state)

    def getValue(self, state):
        return self.computeValueFromQValues(state)
    
    
    
    
    def learn(self, iterations):
        iterations = 1
        for x in range(iterations):
            
            
            
           return 0
       
    def update(self, chosen_action):
        
        state = self.game_state.board.flatten()
        
        self.q_values[(state, chosen_action[0])] = (1-self.alpha) * self.getQValue(state, chosen_action[0]) + self.alpha * (reward + self.discount * self.computeValueFromQValues(nextState))
        
        
    def getRandomMove(self):
        
        
        ### update this function to get best play from q learning states 
        moves = self.game_state.get_valid_moves()
        col = random.choice(moves)
        
        print(self.game_state.board.flatten())
        row = self.game_state.get_next_open_row(col)
        
        action = col 
        print(action)
        self.game_state.drop_piece(row, col, self.coin_type)
        self.game_state.check_for_win_and_handle(self.coin_type)
        self.game_state.next_turn()
        
        return self.game_state
        
    

def main(training = False):
    game_state = game.Game(row_count=4, col_count=5, connect=3)
    
    qlearning_agent = Qlearning(game_state)
    
    if training:
        #should play games against itself and all
        qlearning_agent.learn(iterations = 1)
        
    
    while game_state.game_over != True:
        if game_state.turn == 0:
            game_state.process_events()
            game_state.draw_board()
        else:
            qlearning_agent.game_state = game_state
            # to be updated by get best move
            # getBestMove()
            game_state = qlearning_agent.getRandomMove()


        game_state.draw_board()
        if game_state.get_valid_moves() == []:
            game_state.game_over = True

        if game_state.game_over:
            game_state.wait()








if __name__ == '__main__':
    main()