import pygame, sys
from pygame.locals import *

BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
WOT = (25  , 25, 25)
WOT2 = (123  , 25, 44)
WINDOW_HEIGHT = 800 
WINDOW_WIDTH = 800
height = 8
width = 8
block_size=100


def startUI():
   
    pygame.init()
    SCREEN = pygame.display.set_mode((WINDOW_HEIGHT, WINDOW_WIDTH))
    CLOCK = pygame.time.Clock()
    SCREEN.fill(WHITE)
    color = BLACK

    for y in range(height):
        for x in range(width):
            rect = pygame.Rect(x*block_size, y*block_size, block_size, block_size)
            if (x+y)%2 == 0:
                color = BLACK
            else:
                color = WOT
            pygame.draw.rect(SCREEN, color, rect)
    
    while True:
        for event in pygame.event.get():
                if event.type==QUIT:
                    pygame.quit()
                    sys.exit()
        pygame.display.update()

def drawPiece():
    print()
    
def drawBoard(board):
     for i in range(height):
        for j in range(width):
            if board[i][j] == "a":
                rect = pygame.Rect(x*block_size, y*block_size, block_size, block_size)


