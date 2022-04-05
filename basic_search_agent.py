import math
import random
import argparse
import copy
from collections import deque
import numpy as np
import csv

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
        self.actions = []
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
                    # print(f'{pos}, {(r,c)}')
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
                    # print(f'{pos}, {(r,c)}')
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

    
    def append_actions(self, board, col, col_count):
        action = np.zeros(col_count)
        action = action.flatten().tolist()
        action[col] = 1

        state = board.flatten().tolist()

        self.actions.append((state,action))
        # print(self.actions)

    def export_moves_to_csv(self, file):
        csv_writer = csv.writer(file)
        for action in self.actions:
            csv_writer.writerow([action[0]] + [action[1]])

        #clear recorded actions
        self.actions = []



def random_agent(game_state: game.Game):
    moves = game_state.get_valid_moves()
    col = random.choice(moves)
    row = game_state.get_next_open_row(col)
    return row, col
    
# def write_to_csv(file, board : np.ndarray, col, column_count):
#     csv_writer = csv.writer(file)

#     action = np.zeros(column_count)
#     action[col] = 1
#     action = action.flatten().tolist()

    
#     out = board.flatten().tolist()
#     print(out)
#     # print( lsitboard.flatten())
#     # file.write(f'{out}, {action}\n')
#     csv_writer.writerow([out] + [action])


def setUpArgParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('row_count', type=int, help='Please enter number of rows in board')
    parser.add_argument('column_count', type=int, help='Please enter number of columns in board')
    parser.add_argument('connect', type=int, help='Please enter connect value e.x. connect=4 (connect 4)')
    parser.add_argument('agent', type=str, help='Please enter the agent you would like to use (dfs,bfs)')
    args = parser.parse_args()
    return args


def main():
    args = setUpArgParser()
    
    file = create_file()
    file.write("state,action\n")
    
    
    win_count = 0
    #play 100 games
    for i in range(100000):
        game_state = game.Game(row_count=args.row_count, col_count=args.column_count, connect=args.connect, quiet=True)
        ai_agent = agent(args.agent)


        while game_state.game_over != True:
            if game_state.turn == 0:
                game_state.process_events()
                move = random_agent(game_state)
                #capture move in csv
                # write_to_csv(file, game_state.board, move[1], game_state.col_count)
                ai_agent.append_actions(game_state.board, move[1], game_state.col_count)
                
                game_state.drop_piece(move[0], move[1], HUMAN)
                game_state.check_for_win_and_handle(HUMAN)
                game_state.next_turn()
                game_state.draw_board()

            else:
                move = ai_agent.get_move(game_state)
                if move:
                    game_state.drop_piece(move[0], move[1], AI)
                    game_state.check_for_win_and_handle(AI)
                    if game_state.check_for_win(AI):
                        ai_agent.export_moves_to_csv(file)
                        win_count+=1
                    game_state.next_turn()
                else:
                    #AI cannot win, draw or lost
                    # print('forfeit')
                    game_state.game_over = True
                

            game_state.draw_board()
            if game_state.get_valid_moves() == []:
                game_state.game_over = True

            # if game_state.game_over:
            #     game_state.wait()
        print(f'{win_count}/{i}')
    print(f'Games won: {win_count}/{i}')

    file.close()
if __name__ == '__main__':
    main()