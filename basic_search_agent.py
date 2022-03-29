import math
import random
import argparse
import copy
from collections import deque

from utils import *
import game

winmap = {
    'Win': 1,
    'Draw': 0,
    'Lose': -1
}

AI = 2
HUMAN = 1
counter = 0


class agent:
    def __init__(self, type):
        self.type = type
    
    def bfs(self, game_state: game.Game):
        #find best bfs move
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
            pos = q.popleft()
            #try pos
            if game_state.board[pos[0]][pos[1]] == 0:
                game_state.drop_piece(pos[0], pos[1], AI)
 
            #check if v is goal
            if game_state.check_for_win(AI):
                #win state
                final = pos
                break
            
            for c in game_state.get_valid_moves():
                r = game_state.get_next_open_row(c)

                if explored.get((r, c), None) == None:
                    #not yet explored
                    explored[(r, c)] = pos
                    print(f'{pos}, {(r,c)}')
                    q.append((r,c))
        
        counter = 0
        while explored.get(final, None) not in ['start', None]:
            counter +=1
            final = explored.get(final, None)
        
        #reset board state
        game_state.board = board
        #return best bfs move
        return final

    def dfs(self, game_state: game.Game):
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
                game_state.drop_piece(pos[0], pos[1], AI)
 
            #check if v is goal
            if game_state.check_for_win(AI):
                #win state
                final = pos
                break
            
            for c in game_state.get_valid_moves():
                r = game_state.get_next_open_row(c)

                if explored.get((r, c), None) == None:
                    #not yet explored
                    explored[(r, c)] = pos
                    print(f'{pos}, {(r,c)}')
                    q.append((r,c))
        
        counter = 0
        while explored.get(final, None) not in ['start', None]:
            counter +=1
            final = explored.get(final, None)
        
        #reset board state
        game_state.board = board
        #return best bfs move
        return final

    def get_move(self, game_state: game.Game):
        if self.type == 'dfs': return self.dfs(game_state)
        if self.type == 'bfs': return self.bfs(game_state)


def setUpArgParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('row_count', type=int, help='Please enter number of rows in board')
    parser.add_argument('column_count', type=int, help='Please enter number of columns in board')
    parser.add_argument('connect', type=int, help='Please enter connect value e.x. connect=4 (connect 4)')
    parser.add_argument('--agent', type=str, help='Please enter the agent you would like to use (dfs,bfs)')
    args = parser.parse_args()
    return args


def main():
    args = setUpArgParser()
    game_state = game.Game(row_count=args.row_count, col_count=args.column_count, connect=args.connect)
    ai_agent = agent(args.agent)


    while game_state.game_over != True:
        if game_state.turn == 0:
            game_state.process_events()
            game_state.draw_board()

        else:
            move = ai_agent.get_move(game_state)
            if move:
                game_state.drop_piece(move[0], move[1], AI)
                game_state.check_for_win_and_handle(AI)
                game_state.next_turn()
            else:
                #AI cannot win, draw or lost
                print('forfeit')
                game_state.game_over = True
            

        game_state.draw_board()
        if game_state.get_valid_moves() == []:
            game_state.game_over = True

        if game_state.game_over:
            game_state.wait()



if __name__ == '__main__':
    main()