from utils import *
import game
import argparse


def setUpArgParser():
	parser = argparse.ArgumentParser()
	parser.add_argument('row_count', type=int, help='Please enter number of rows in board')
	parser.add_argument('column_count', type=int, help='Please enter number of columns in board')
	parser.add_argument('connect', type=int, help='Please enter connect value e.x. connect=4 (connect 4)')
	args = parser.parse_args()
	return args


def main():
	args = setUpArgParser()
	#initialise game state
	game_state = game.Game(row_count=args.row_count, col_count=args.column_count, connect=args.connect)

	#initial draw
	game_state.draw_board()
	game_state.update()

	#Game loop
	while not game_state.game_over:

		#Player 1 = RED, Player 2 = YELLOW
		game_state.process_events()
		game_state.draw_board()

		if game_state.get_valid_moves() == []:
			game_state.game_over = True
			
		if game_state.game_over:
			game_state.wait()


if __name__ == '__main__':
	main()

