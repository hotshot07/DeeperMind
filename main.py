from utils import *
import game

ROW_COUNT = 6
COLUMN_COUNT = 7


#initialise game state
game_state = game.Game(row_count=ROW_COUNT, col_count=COLUMN_COUNT)

#initial draw
game_state.draw_board()
game_state.update()

#Game loop
while not game_state.game_over:

	#Player 1 = RED, Player 2 = YELLOW
	game_state.process_events()
	game_state.print_board()
	game_state.draw_board()

	if game_state.game_over:
		game_state.wait()