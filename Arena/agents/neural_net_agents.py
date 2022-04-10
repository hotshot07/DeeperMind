import copy
from collections import deque
import numpy as np
import csv
import game
from tensorflow import keras
import os 
import tensorflow as tf
tf.get_logger().setLevel('ERROR')


# Parent class 
class BaseNeuralAgent3:
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

        print(prob_dict_sorted)
       
        for column, probability in prob_dict_sorted.items():
            print("top move:",column)
            print("move available",moves)
            if column in moves:
                return column
            

class BaseNeuralAgent4:
    def __init__(self, agent_number, model):
        self.agent_number = agent_number
        self.model = model  

    def get_best_move(self, game_state: game.Game):
        moves = game_state.get_valid_moves()
    
        probability_vector = self.model.predict(np.array(game_state.board.flatten().reshape(1,42)))
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
            


class NNHybridAgent(BaseNeuralAgent3):
    def __str__(self) -> str:
        return "NNHybrid Agent3"
    
    def __init__(self, agent_number):
        model = keras.models.load_model('agents/models/hybrid_model')
        super().__init__(agent_number, model)
        

class NNBfsAgent(BaseNeuralAgent3):
    def __str__(self) -> str:
        return "NN BFs Agent3"
    def __init__(self, agent_number):
        model = keras.models.load_model('agents/models/bfs_model')
        super().__init__(agent_number, model)
        
        
class NNMinimaxAgent(BaseNeuralAgent3):
    def __str__(self) -> str:
        return "NN Minimax Agent3"
    
    def __init__(self, agent_number):
        model = keras.models.load_model('agents/models/minimax_neural_75')
        super().__init__(agent_number, model) 

class NNHybridAgent4(BaseNeuralAgent4):
    def __str__(self) -> str:
        return "NN Hybrid Agent4"
    
    def __init__(self, agent_number):
        model = keras.models.load_model('agents/models/hybrid_model_connect4')
        super().__init__(agent_number, model)
        

class NNDfsAgent4(BaseNeuralAgent4):
    def __str__(self) -> str:
        return "NN Dfs Agent4"
    
    def __init__(self, agent_number):
        model = keras.models.load_model('agents/models/df_neural_agent_connect4')
        super().__init__(agent_number, model)
        
        
class NNMinimaxAgent4(BaseNeuralAgent4):
    def __str__(self) -> str:
        return "NN Minimax Agent4"
    
    def __init__(self, agent_number):
        model = keras.models.load_model('agents/models/minimax_neural_connect4')
        super().__init__(agent_number, model)   
        
class NNEverything(BaseNeuralAgent4):
    def __str__(self) -> str:
        return "NN Everything Agent4"
    
    def __init__(self, agent_number):
        model = keras.models.load_model('agents/models/hybrid_everything_model_connect4')
        super().__init__(agent_number, model)  
        
    
    