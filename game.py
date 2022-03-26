import sys
import pygame
import utils
import math
import numpy as np

from settings import *

class Game:
    def __init__(self, row_count, col_count) -> None:
        self.pygame = pygame.init()
        self.col_count = col_count
        self.row_count = row_count
        self._init_board()
        self.game_over = False
        self.turn = 0

        self.width = self.col_count * SQUARESIZE
        self.height = (self.row_count +1) * SQUARESIZE

        self._init_screen()
        self._init_font()  
    

    def _init_board(self) -> None:
        self.board = np.zeros((self.row_count,self.col_count))
        self.print_board()


    def _init_screen(self) -> None:
        pygame.display.init()
        self.screen = pygame.display.set_mode(size=(self.width,self.height))
    

    def _init_font(self) -> None:
        pygame.font.init()
        self.myfont = pygame.font.SysFont("monospace", 75)
    

    def update(self) -> None:
        pygame.display.update()
    

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(self.screen, BLACK, (0,0, self.width, SQUARESIZE))
                posx = event.pos[0]
                print(self.turn)
                if self.turn == 0:
                    pygame.draw.circle(self.screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)
                else:
                    pygame.draw.circle(self.screen, YELLOW, (posx, int(SQUARESIZE/2)), RADIUS)
            self.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(self.screen, BLACK, (0,0, self.width, SQUARESIZE))
                self.player_turn(event)            
            

    def player_turn(self, event):
        piece = 1 if self.turn == 0 else 2
        colour = RED if self.turn == 0 else YELLOW

        posx = event.pos[0]
        col = int(math.floor(posx/SQUARESIZE))

        if self.is_valid_location(col):
            row = self.get_next_open_row(col)
            self.drop_piece(row, col, piece)

            if self.check_for_win(piece):
                label = self.myfont.render(f"Player {piece} wins!!", 1, colour)
                self.screen.blit(label, (40,10))
                self.game_over = True
            
            self.next_turn()
    

    def get_next_open_row(self, col: int)  -> int:
        for r in range(self.col_count):
            if self.board[r][col] == 0:
                return r

##-----------Checking-Functions---------------------------------------------------------------------##

    def check_for_win(self, piece: int) -> bool:
        # Check horizontal locations for win
        for c in range(self.col_count-3):
            for r in range(self.row_count):
                if self.board[r][c] == piece and self.board[r][c+1] == piece and self.board[r][c+2] == piece and self.board[r][c+3] == piece:
                    return True

        # Check vertical locations for win
        for c in range(self.col_count):
            for r in range(self.row_count-3):
                if self.board[r][c] == piece and self.board[r+1][c] == piece and self.board[r+2][c] == piece and self.board[r+3][c] == piece:
                    return True

        # Check positively sloped diaganols
        for c in range(self.col_count-3):
            for r in range(self.row_count-3):
                if self.board[r][c] == piece and self.board[r+1][c+1] == piece and self.board[r+2][c+2] == piece and self.board[r+3][c+3] == piece:
                    return True

        # Check negatively sloped diaganols
        for c in range(self.col_count-3):
            for r in range(3, self.row_count):
                if self.board[r][c] == piece and self.board[r-1][c+1] == piece and self.board[r-2][c+2] == piece and self.board[r-3][c+3] == piece:
                    return True
    

    def is_valid_location(self, col)  -> bool:
        return self.board[self.row_count-1][col] == 0
    

##-----------Interaction-Functions---------------------------------------------------------------------##

    def drop_piece(self, row: int, col: int, piece: int) -> None:
        self.board[row][col] = piece

    
    def next_turn(self):
        self.turn += 1
        self.turn = self.turn % 2
    
##-----------Display-Functions---------------------------------------------------------------------##

    def print_board(self) -> None:
	    print(np.flip(self.board, 0))


    def draw_board(self) -> None:
        for c in range(self.col_count):
            for r in range(self.row_count):
                pygame.draw.rect(self.screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
                pygame.draw.circle(self.screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)

        for c in range(self.col_count):
            for r in range(self.row_count):
                if self.board[r][c] == 1:
                    pygame.draw.circle(self.screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), self.height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
                elif self.board[r][c] == 2:
                    pygame.draw.circle(self.screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), self.height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
        pygame.display.update()



    def wait(self):
        pygame.time.wait(3000)