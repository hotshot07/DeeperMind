import math
import numpy as np
import copy
import random
import json
import os.path
import os

gamma = 1
alpha = 0.3
epsilon = 0
# q_value_table = {}


class Q_learning_agent:
    def __str__(self) -> str:
        return "Qlearning Agent"
    
    def __init__(self, agent_number,value):
        self.agent_number = agent_number
        self.q_value_table = None 
        self.value = value
        self.readQTable()
        
        

    def flipCoin(self, p):
        r = random.random()
        return r < p

    def readQTable(self):
        q_value_table_read = {}
        #print("LIST DIR ", os.listdir(os.getcwd()))
        # if os.path.exists('agents/q_tables/q_table_optimised_connect3.json'):
        with open(f"agents/q_tables/q_table_optimised_connect{self.value}.json", "r") as f:
            data = json.load(f)
            dic = json.loads(data)
            k = dic.keys()
            v = dic.values()
            k1 = [eval(i) for i in k]
            q_value_table_read = dict(zip(*[k1, v]))

        print("Q_value_table_read")
        self.q_value_table = q_value_table_read

    def getQValue(self, state, action):
        if self.q_value_table.get((state, action)) is None:
            self.q_value_table[(state, action)] = 0

        return self.q_value_table[(state, action)]

    def computeValueFromQValues(self, game_state, state):
        """
        Returns max_action Q(state,action)
        where the max is over legal actions.  Note that if
        there are no legal actions, which is the case at the
        terminal state, you should return a value of 0.0.
        """
        max_q_value = -math.inf
        actions = game_state.get_valid_moves()
        for column_action in actions:
            q_value = self.getQValue(state, column_action)
            if q_value > max_q_value:
                max_q_value = q_value

        return max_q_value

    def computeMaxActionFromQValues(self, game_state, state):
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
            q_value = self.getQValue(state, column_action)
            if q_value > max_q_value:
                max_q_value = q_value
                best_legal_action_in_state = column_action

        return best_legal_action_in_state

    def getAction(self, game_state, state):
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

        random_action_probability = self.flipCoin(epsilon)
        if random_action_probability is True:
            action = random.choice(legalActions)
        else:
            action = self.computeMaxActionFromQValues(game_state, state)

        return action

    def get_best_move(self, game_state):
        state = copy.deepcopy(game_state.board)
        state = tuple(map(tuple, state))
        best_action = self.getAction(game_state, state)
        #self.update(game_state, state, best_action)

        # best_action is a column number
        return best_action
