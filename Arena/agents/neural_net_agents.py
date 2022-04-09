import copy
from collections import deque
import numpy as np
import csv
import game
from tensorflow import keras
import os 

# Parent class 
class BaseNeuralAgent:
    def __init__(self, agent_number, model):
        self.agent_number = agent_number
        self.model = model  

    def get_best_move(self, game_state: game.Game):
        moves = game_state.get_valid_moves()
    
        probability_vector = self.model.predict(np.array(game_state.board.flatten().reshape(1,20)))
        probability_list = probability_vector.tolist()[0]
        
        # [ 0.3, 0.4, 0.2 0.1 , 0.0 ]
        # to 
        # {
        #     0: 0.3,
        #     1 :0.4
        #     ...
        # }
        
        probability_dict = { index:val for index,val in enumerate(probability_list)}
        
        # sorts by value in reverse 
        
        prob_dict_sorted = {k: v for k, v in sorted(probability_dict.items(), key=lambda item: item[1], reverse=True)}
        
        for column, probability in prob_dict_sorted.items():
            if column in moves:
                return column
            


class NNHybridAgent(BaseNeuralAgent):
    def __init__(self, agent_number):
        model = keras.models.load_model('agents/models/hybrid_model')
        super().__init__(agent_number, model)
        

class NNBfsAgent(BaseNeuralAgent):
    def __init__(self, agent_number):
        model = keras.models.load_model('agents/models/bfs_model')
        super().__init__(agent_number, model)
        
        
class NNMinimaxAgent(BaseNeuralAgent):
    def __init__(self, agent_number):
        print(os.listdir())
        model = keras.models.load_model('agents/models/minimax_neural_75')
        super().__init__(agent_number, model)   
        
        
    
    