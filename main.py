from algo import *
from ui import*
import sys
import pygame, sys
import time
from pygame.locals import * 


def drawEmptyBoard(screen):
        for x in range(height):
            for y in range(width):
                rect = pygame.Rect(x*block_size, y*block_size, block_size, block_size)
                if (x+y)%2 == 0:
                    color = BLACK
                else:
                    color = GRAY
                pygame.draw.rect(screen, color, rect)
def drawBoardPieces(board,screen):
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
                #rect = pygame.circle(y*block_size+10, x*block_size+10, block_size-20, block_size-20)
                pygame.draw.circle(screen, color,(y*block_size+50, x*block_size+50), 40)

def getAlgorithmFromInput():
	algorithm = None
	while algorithm == None:
		print("Alege Algoritmul: ")
		print("1. Min Max")
		print("2. Alpha Beta")
		algorithm = input()
		if algorithm ==  "1":
			return 1
		elif algorithm == "2":
			return 2
		else:
			print("Input gresit")
			algorithm = None

def getDifficultyFromInput():
	difficulty = None
	while difficulty == None:
		print("Alege Dificultatea: ")
		print("1. Easy")
		print("2. Medium")
		print("3. Hard")
		difficulty = input()
		if difficulty ==  "1":
			return 3
		elif difficulty == "2":
			return 4
		elif difficulty == "3":
			return 5
		else:
			print("Input gresit")
			difficulty = None

def getHumanPlayerColorFromInput():
	color = None
	while color == None:
		print("Alege culoarea cu care sa joci :")
		print("1. Alb")
		print("2. Negru")
		color = input()
		if color ==  "1":
			return "a"
		elif color == "2":
			return "n"
		else:
			print("Input gresit")
			color = None

def printBoard(board):
	for i in range(0,8):
		print(board[i])
		
		
def validPlayerInput(stare_curenta):
	#Printeaza ce mutari sunt available
	
	moveSpree = True
	moveSpreeStarted = False
	# SA MAI ADAUG UN LOOP PT VERIFICARE DACA INPUT == VALID
	while moveSpree == True:
		printBoard(stare_curenta.tabla_joc.board)
		moveSpree = playerHasSpreeMoves(stare_curenta.tabla_joc,stare_curenta.j_curent)
		stare_curenta.moveSpree = moveSpree
		if moveSpreeStarted == True and moveSpree == False:
			break
		moveSpreeStarted = moveSpree

		print(moveSpree)
		print("Selectati de pe ce pozitie vrei sa mutati:  ")
		allValidMoveSets = getAllValidMovesets(stare_curenta.tabla_joc,stare_curenta.j_curent,moveSpree)
		for pereche in allValidMoveSets.keys():
			print(pereche, end=' ')
	  
		
	
		while True:
			print("Selecteaza linia:")
			startx = str(input())
			print("Selecteaza coloana:")
			starty = str(input())
			if(startx.isnumeric() and starty.isnumeric()):
				startx = int(startx)
				starty = int(starty)
				if (startx,starty) in allValidMoveSets.keys():
					break

		possibleHumanMoves = getSingleValidMoveset(stare_curenta.tabla_joc,startx,starty,stare_curenta.moveSpree,stare_curenta.j_curent)
	 
		print(possibleHumanMoves)
	 
		print("Selectati pe ce pozitie vrei sa mutati: ")
		while True:
			print("Selecteaza linia:")
			stopx = str(input())
			print("Selecteaza coloana:")
			stopy = str(input())
			if(stopx.isnumeric() and stopy.isnumeric()):
				stopx = int(stopx)
				stopy = int(stopy)
				if [stopx,stopy] in possibleHumanMoves:
					break
		updateBoard(stare_curenta.tabla_joc.board,(startx,starty),(stopx,stopy),Joc.JMIN)
	
	 		

def playerStatusInput():
	while True:
		print("Doresti sa joci in continuare ? :")
		print("1. Continua Jocul")
		print("2. Opreste ")
		statusInput = input()
		if statusInput == "1":
			break
		else:
			# --- afisam scoruri eventual
			print("Joc anulat")
			return False
	return True
			
def getInterfaceType():
	while True:
		print("Tip Interfata")
		print("1. Consola")
		print("2. GUI ")
		statusInput = input()
		if statusInput == "1":
			return 1
		elif statusInput =="2":
			return 2
		


def startgame(algorithm,humanPlayerColor,depth,ui):
	timpStartJoc = time.time()
	board = None
	game = Joc(board)
	
	print("Board initial: ")
	
	Joc.JMIN = humanPlayerColor
	Joc.JMAX = "n" if humanPlayerColor == "a" else "a"
	
	totalMovesHuman = 0
	totalMovesAI = 0
	

	Stare.ADANCIME_MAX = depth
	stare_curenta = Stare(game, "n", Stare.ADANCIME_MAX)
              
	
	while True:
		
		if printIfFinal(stare_curenta):
			print("Joc finalizat in :" + str(time.time() - timpStartJoc) + " secunde")
			print("Mutari total Alb{} si Negru{}".format(totalMovesHuman,totalMovesAI))
			break

		if stare_curenta.j_curent ==  Joc.JMIN:
			if(playerStatusInput()==False):
				print("Mutari total Alb: {} si Negru: {}".format(totalMovesHuman,totalMovesAI))
				print("Joc finalizat in :" + str(time.time() - timpStartJoc) + " secunde")
				sys.exit(0)
			tmpStartProcessHuman = time.time()
			validPlayerInput(stare_curenta)
			totalMovesHuman+=1
			print("Jucatorul a gandit :" + str(time.time() - tmpStartProcessHuman) + " secunde")
			stare_curenta.j_curent = stare_curenta.jucator_opus()
		else:
			print("AI TURN :")
			totalMovesAI +=1
			moveSpree = True
			moveSpreeStarted = False
			timpStartProcesAi = time.time()
			while moveSpree == True:
				moveSpree = playerHasSpreeMoves(stare_curenta.tabla_joc,stare_curenta.j_curent)
				stare_curenta.moveSpree = moveSpree
				if moveSpreeStarted == True and moveSpree == False:
					break
				moveSpreeStarted = moveSpree
				
				if(algorithm == 1):
					newState = min_max(stare_curenta)
				else:
					newState = alpha_beta(-5000,5000,stare_curenta) 
				stare_curenta.tabla_joc = newState.stare_aleasa.tabla_joc
			print("Ai-ul a gandit :" + str(time.time() - timpStartProcesAi) + " secunde")
			stare_curenta.j_curent = stare_curenta.jucator_opus()
	
	
			

def main():
 
	algorithm = getAlgorithmFromInput()
	humanPlayerColor = getHumanPlayerColorFromInput()
	depth = getDifficultyFromInput()
	ui = getInterfaceType()
	
	if(ui == 1):    
		startgame(algorithm,humanPlayerColor, depth, ui)
	else:
		screen = pygame.display.set_mode((WINDOW_HEIGHT, WINDOW_WIDTH))
		drawEmptyBoard(screen)
		start_time = pygame.time.get_ticks() / 1000
		clock = pygame.time.Clock()
  
		board = None
		game = Joc(board)



		Joc.JMIN = humanPlayerColor
		Joc.JMAX = "n" if humanPlayerColor == "a" else "a"
		boardChanged = True
		totalMovesHuman = 0
		totalMovesAI = 0
	
		Stare.ADANCIME_MAX = depth
		stare_curenta = Stare(game, "a", Stare.ADANCIME_MAX)
		lastClicked = False
		firstX = 0
		firstY = 0
		while True:
			clock.tick(15)
			
			time = pygame.time.get_ticks() / 1000
			elapsed = time - start_time
			if boardChanged == True:
				boardChanged = False
				drawEmptyBoard(screen)
				drawBoardPieces(stare_curenta.tabla_joc.board,screen)
				pygame.display.update()
			pygame.display.flip()
			repeatInput = False
			for event in pygame.event.get():
				if event.type==pygame.QUIT:
					pygame.quit()
					sys.exit()
				if  lastClicked == False and event.type == pygame.MOUSEBUTTONDOWN:
					lastClicked = True
					tmpY,tmpX = event.pos
					firstX = int(tmpX/100)
					firstY = int(tmpY/100)
						
				elif  lastClicked == True and event.type == pygame.MOUSEBUTTONDOWN :
					realY,realX = event.pos
					secondX = int(realX/100)
					secondY = int(realY/100)
					lastClicked = False
					
					moveSpree = True
					moveSpreeStarted = False
					
					while moveSpree == True:
						if printIfFinal(stare_curenta):
							break
						printBoard(stare_curenta.tabla_joc.board)
						moveSpree = playerHasSpreeMoves(stare_curenta.tabla_joc,stare_curenta.j_curent)
						stare_curenta.moveSpree = moveSpree
						if moveSpreeStarted == True and moveSpree == False:
							break
							
						moveSpreeStarted = moveSpree

						print(moveSpree)
						print("Selectati de pe ce pozitie vrei sa mutati:  ")
						allValidMoveSets = getAllValidMovesets(stare_curenta.tabla_joc,stare_curenta.j_curent,moveSpree)
						for pereche in allValidMoveSets.keys():
							print(pereche, end=' ')
						if((firstX,firstY) not in allValidMoveSets.keys()):
							repeatInput = True
							break
						print()
						print("Selecteaza linia:")
						print((firstX,firstY))
						startx = firstX
		
						print("Selecteaza coloana:")
		
						starty = firstY
						

						possibleHumanMoves = getSingleValidMoveset(stare_curenta.tabla_joc,startx,starty,stare_curenta.moveSpree,stare_curenta.j_curent)
		
						print(possibleHumanMoves)
						if([secondX,secondY] not in possibleHumanMoves):
							repeatInput = True
							break
   
						print("Selectati pe ce pozitie vrei sa mutati: ")
						print("Selecteaza linia:")
						stopx = secondX
						print("Selecteaza coloana:")
						stopy = secondY
						
						updateBoard(stare_curenta.tabla_joc.board,(startx,starty),(stopx,stopy),Joc.JMIN)
						drawEmptyBoard(screen)
						drawBoardPieces(stare_curenta.tabla_joc.board,screen)
						lastClicked = False
						pygame.display.update()
						if moveSpreeStarted == True and moveSpree == True:
							repeatInput == True
							break

					if(repeatInput == True):
						continue
					
					print("AI TURN :")
					moveSpree = True
					moveSpreeStarted = False
					stare_curenta.j_curent = stare_curenta.jucator_opus()
					while moveSpree == True:
						if printIfFinal(stare_curenta):
							break
						moveSpree = playerHasSpreeMoves(stare_curenta.tabla_joc,stare_curenta.j_curent)
						stare_curenta.moveSpree = moveSpree
						if moveSpreeStarted == True and moveSpree == False:
							break
						moveSpreeStarted = moveSpree
						if(algorithm == 1):
							newState = min_max(stare_curenta)
						else:
							newState = alpha_beta(-5000,5000,stare_curenta) 
						stare_curenta.tabla_joc = newState.stare_aleasa.tabla_joc
						drawEmptyBoard(screen)
						drawBoardPieces(stare_curenta.tabla_joc.board,screen)
						pygame.display.update()
					stare_curenta.j_curent = stare_curenta.jucator_opus()
	

if __name__ == "__main__" :
	  main()
