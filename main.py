from algo import *
from ui import*
import sys

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
	  
		print()
		print("Selecteaza linia:")
	 
		startx = int(input())
	 
		print("Selecteaza coloana:")
	 
		starty = int(input())
	 
		possibleHumanMoves = getSingleValidMoveset(stare_curenta.tabla_joc,startx,starty,stare_curenta.moveSpree,stare_curenta.j_curent)
	 
		print(possibleHumanMoves)
	 
		print("Selectati pe ce pozitie vrei sa mutati: ")
		print("Selecteaza linia:")
		stopx = int(input())
		print("Selecteaza coloana:")
		stopy = int(input())
		updateBoard(stare_curenta.tabla_joc.board,(startx,starty),(stopx,stopy),Joc.JMIN)
		#startUI()
		#drawBoard(stare_curenta.tabla_joc.board)
	 		

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
			sys.exit(0)
			
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
	board = None
	game = Joc(board)
	
	print(game.finalScore("n"))
	print(game.finalScore("a"))
	
	print("Board initial: ")
	
	Joc.JMIN = humanPlayerColor
	Joc.JMAX = "n" if humanPlayerColor == "a" else "a"
	
	totalMovesHuman = 0
	totalMovesAI = 0
	

	Stare.ADANCIME_MAX = depth
	stare_curenta = Stare(game, "a", Stare.ADANCIME_MAX)
	
	while True:
		if afis_daca_final(stare_curenta):
			break

		if stare_curenta.j_curent ==  Joc.JMIN:
			playerStatusInput()
			validPlayerInput(stare_curenta)
			stare_curenta.j_curent = stare_curenta.jucator_opus()
		else:
			print("AI TURN :")
			moveSpree = True
			moveSpreeStarted = False
			
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
			stare_curenta.j_curent = stare_curenta.jucator_opus()
			
	

def main():
	algorithm = getAlgorithmFromInput()
	humanPlayerColor = getHumanPlayerColorFromInput()
	depth = getDifficultyFromInput()
	ui = getInterfaceType()
	if(ui == 1):    
		startgame(algorithm,humanPlayerColor, depth, ui)
	else:
		startUI()
  

if __name__ == "__main__" :
	  main()
