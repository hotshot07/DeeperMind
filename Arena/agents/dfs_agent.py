import copy
from collections import deque
import numpy as np
import csv
import game

class Dfs_agent:
    def __str__(self) -> str:
        return "DFS Agent"
    
    def __init__(self, agent_number):
        self.agent_number = agent_number
        self.actions = []

    def get_best_move(self, game_state: game.Game):
        #find dfs move
        board = copy.deepcopy(game_state.board)
        
        #data
        q = deque()
        explored = dict()
        final = None
    
        #append all initial states
        for col in game_state.get_valid_moves():
            row = game_state.get_next_open_row(col)
            q.append((row, col))
            explored[(row, col)] = ('start')
        
        while len(q) >0:
            pos = q.pop()
            #try pos
            if game_state.board[pos[0]][pos[1]] == 0:
                game_state.drop_piece(pos[0], pos[1], self.agent_number)
 
            #check if v is goal
            if game_state.check_for_win(self.agent_number):
                #win state
                final = pos
                break
            
            for c in game_state.get_valid_moves():
                r = game_state.get_next_open_row(c)

                if explored.get((r, c), None) == None:
                    #not yet explored
                    explored[(r, c)] = pos
                    # print(f'{pos}, {(r,c)}')
                    q.append((r,c))
        
        counter = 0
        while explored.get(final, None) not in ['start', None]:
            counter +=1
            final = explored.get(final, None)
        
        #reset board state
        game_state.board = board
        #return best bfs move
        if final:
            return final[1]
        else:
            return game_state.get_valid_moves()[0]
    

    
