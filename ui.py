import pygame, sys
from pygame.locals import *

BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
GRAY = (25  , 25, 25)
PLAYER1_COLOR_PIECE = (123  , 25, 44)
PLAYER1_COLOR_KING = (123  , 30, 50)
PLAYER2_COLOR_PIECE = (111  , 44, 22)
PLAYER2_COLOR_KING = (111  , 50, 24)
WINDOW_HEIGHT = 800 
WINDOW_WIDTH = 800
CLOCK = pygame.time.Clock()
height = 8
width = 8
block_size=100


class GUI():
    
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_HEIGHT, WINDOW_WIDTH))
        
    def drawEmptyBoard(self):
        for x in range(height):
            for y in range(width):
                rect = pygame.Rect(x*block_size, y*block_size, block_size, block_size)
                if (x+y)%2 == 0:
                    color = BLACK
                else:
                    color = GRAY
                pygame.draw.rect(self.screen, color, rect)
        pygame.display.update()
        
    def drawBoardPieces(self,board):
        for x in range(height):
            for y in range(width):
                if board[x][y] == "a":
                    color =  PLAYER1_COLOR_PIECE
                elif board[x][y] == "A":
                    color =  PLAYER1_COLOR_KING
                elif board[x][y] == "n":
                    color =  PLAYER2_COLOR_PIECE
                elif board[x][y] == "N":
                    color =  PLAYER2_COLOR_KING
                else:
                    continue
                rect = pygame.Rect(y*block_size, x*block_size, block_size, block_size)
                pygame.draw.rect(self.screen, color, rect)
        pygame.display.update()
            
def startUI():
    
    pygame.init()

    while True:
        for event in pygame.event.get():
                if event.type==QUIT:
                    pygame.quit()
                    sys.exit()
        pygame.display.update()


                


