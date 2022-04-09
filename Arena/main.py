# from utils import *
import game
import argparse
from arena import Arena


def setup_argparser():
    parser = argparse.ArgumentParser()
    parser.add_argument('row_count', type=int, help='Please enter number of rows in board')
    parser.add_argument('column_count', type=int, help='Please enter number of columns in board')
    parser.add_argument('connect', type=int, help='Please enter connect value e.x. connect=4 (connect 4)')
    parser.add_argument('--agent1', type=str, help='Please enter agent 1 name')
    parser.add_argument('--agent2', type=str, help='Please enter agent 2 name')
    args = parser.parse_args()
    return args


def process_move(game_state: game.Game, col, piece):
    row = game_state.get_next_open_row(col)
    print("agent drops piece", piece)
    game_state.drop_piece(row=row,col=col,piece=piece)

    #needed for drawing pygame, disable for real speed
    game_state.process_events()
    game_state.draw_board()

    #check if just won
    if game_state.check_for_win(piece):
        print("this agent just won")
        game_state.game_over = True
        return True

    #no moves left
    if game_state.get_valid_moves() == []:
        print("no moves")
        game_state.game_over = True
    
    game_state.next_turn()


def main():
    args = setup_argparser()
    
    #create arena
    arena = Arena(args.agent1, args.agent2)
    #create game
    game_state = game.Game(row_count=args.row_count, col_count=args.column_count, connect=args.connect)


	# initial draw
    game_state.draw_board()
    game_state.update()

	#Game loop
    while not game_state.game_over:
        
    	#Player 1 = RED, Player 2 = YELLOW

        if game_state.turn == 0:
            if len(game_state.get_valid_moves()) == 1:
                col = game_state.get_valid_moves()[0]
            else:
                col = arena.agent_1.get_best_move(game_state)
            win = process_move(game_state=game_state, col=col, piece=arena.agent_1.agent_number)
            if win:
                arena.victor = arena.agent_1.agent_number
        
        if game_state.turn == 1:
            if len(game_state.get_valid_moves()) == 1:
                col = game_state.get_valid_moves()[0]
            else:
                col = arena.agent_2.get_best_move(game_state)
            win = process_move(game_state=game_state, col=col, piece=arena.agent_2.agent_number)
            if win:
                arena.victor = arena.agent_2.agent_number
        
        
        
        
    
    print('-'*40)
    print('game over')
    if arena.victor:
        print(f'victor = {arena.victor}')
    else:
        print(f'Tie')

    game_state.wait()

if __name__ == '__main__':
    main()