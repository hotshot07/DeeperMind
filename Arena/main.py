import utils
import game
import argparse
import random

from arena import Arena


def setup_argparser():
    parser = argparse.ArgumentParser()
    parser.add_argument('row_count', type=int, help='Please enter number of rows in board')
    parser.add_argument('column_count', type=int, help='Please enter number of columns in board')
    parser.add_argument('connect', type=int, help='Please enter connect value e.x. connect=4 (connect 4)')
    parser.add_argument('--agent1', type=str, help='Please enter agent 1 name')
    parser.add_argument('--agent2', type=str, help='Please enter agent 2 name')
    parser.add_argument('--games', type=int, help='Please enter agent number of games')
    args = parser.parse_args()
    return args


def process_move(game_state: game.Game, col, piece, agent):
    row = game_state.get_next_open_row(col)
    game_state.drop_piece(row=row,col=col,piece=piece)

    #needed for drawing pygame, disable for real speed
    game_state.process_events()
    game_state.draw_board()

    #check if just won
    if game_state.check_for_win(piece):
        print("this agent just won", piece)
        game_state.game_over = True
        return True

    #no moves left
    if game_state.get_valid_moves() == []:
        print("no moves")
        game_state.game_over = True
    
    game_state.next_turn()


def main():
    args = setup_argparser()
    opponents = []

    #create arena
    if args.agent2 == 'all':
        opponents = ['dfs','bfs','minimax','random', 'qlearn', 'nn-minimax', 'nn-bfs', 'nn-hybrid']
    else:
        opponents = [args.agent2]

    #create a file to contain test results
    file = utils.create_file(args.agent1)
    utils.write_col_names(file)
    
    for opponent in opponents:

        if opponent == args.agent1:
            continue
        
        arena = Arena(args.agent1, opponent, args.games)

        random_first_move = True 
        
        
        
        #run several games
        for x in range(arena.num_games):
            arena.new_game()
            game_state = game.Game(row_count=args.row_count, col_count=args.column_count, connect=args.connect)
            
            
            
            total_moves_a1 = 0
            total_moves_a2 = 0
            
            #Game loop
            while not game_state.game_over:
                
                #Player 1 = RED, Player 2 = YELLOW
                
                if game_state.turn == 0:
                    if len(game_state.get_valid_moves()) == 1:
                        col = game_state.get_valid_moves()[0]
                    else:
                        col = arena.agent_1.get_best_move(game_state)
                        if total_moves_a1 == 0 and random_first_move:
                            col = random.randint(0,args.column_count-1)
                            
                        total_moves_a1 = total_moves_a1 + 1

                    win = process_move(game_state=game_state, col=col, piece=arena.agent_1.agent_number, agent=arena.agent_1)
                    if win:
                        arena.victor = arena.agent_1.agent_number
                        arena.agent_2_losses +=1
                
                if game_state.turn == 1:
                    if len(game_state.get_valid_moves()) == 1:
                        col = game_state.get_valid_moves()[0]
                    else:
                        col = arena.agent_2.get_best_move(game_state)
                        if total_moves_a2 == 0 and random_first_move:
                            col = random.randint(0,args.column_count-1)
                            
                        total_moves_a2 = total_moves_a2 + 1
                            
                    win = process_move(game_state=game_state, col=col, piece=arena.agent_2.agent_number, agent=arena.agent_2)
                    if win:
                        arena.victor = arena.agent_2.agent_number
                        arena.agent_2_wins +=1

                        
            total_moves_a1 = 0
            total_moves_a2 = 0
            
            if arena.victor == None:
                arena.agent_2_ties +=1
            
        utils.write_to_file(file, opponent, wins=arena.agent_2_wins, ties=arena.agent_2_ties, losses=arena.agent_2_losses)  
        
        print('-'*40)
        print('game over')
        print(f'(Agent 2) Wins:{arena.agent_2_wins}, Ties:{arena.agent_2_ties}, Losses:{arena.agent_2_losses}')

if __name__ == '__main__':
    main()