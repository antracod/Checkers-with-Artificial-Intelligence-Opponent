import copy
import time


class Joc:
	NR_LINII = 8
	NR_COLOANE = 8
	JMIN = None
	JMAX = None
	SPREE = False
	GOL = '.'
	NEGRU = "n"
	NEGRU_REGE = "N"
	ALB = "a"
	ALB_REGE = "A"
	

	def __init__(self, board=None):
		self.spree_position = ()
		if board == None:
			self.board = []
			for i in range(0, 8):
				linie = []
				for j in range(0, 8):
					if (i == 0 and j %2 == 1) or (i == 1 and j %2 == 0) or (i == 2 and j %2 == 1):
						linie.append(self.ALB)
					elif(i == 5 and j % 2 == 0) or (i == 6 and j % 2 == 1) or (i == 7 and j % 2 == 0):
						linie.append(self.NEGRU)
					else:
						linie.append(self.GOL)
				self.board.append(linie)
		else:
			self.board = board

	def final(self,playerColor):
		
		#possibleMoves = self.mutari_joc(playerColor)

		#possibleMovesCount = len(possibleMoves)
		possibleMovesCount  = self.maiExistaMutariTotale()
		if possibleMovesCount == 0:
			finalScoreJmin = self.finalScore(self.JMIN)
			finalScoreJmax = self.finalScore(self.JMAX)

			if finalScoreJmax == finalScoreJmin:
				return "Joc termin cu o remiza"
			elif finalScoreJmax > finalScoreJmin:
				return self.JMAX
			else:
				return self.JMIN	
		return False

	#mutari Valid
	def maiExistaMutariTotale(self):
		blackPiecesLeft = 0
		whitePiecesLeft = 0
		for i in range(0,8):
			for j in range(0,8):
				if((self.board[i][j]=="n" or self.board[i][j]=="N") ):
					blackPiecesLeft +=1
				elif((self.board[i][j]=="a" or self.board[i][j]=="A") ):
					whitePiecesLeft +=1
				if whitePiecesLeft and blackPiecesLeft:
					break
		if whitePiecesLeft == 0 or blackPiecesLeft == 0:
			return 0
		for i in range(0,8):
			for j in range(0,8):
				if(isPiece(self.board[i][j])):
					allValidMoveSets1 = getSingleValidMoveset(self,i,j,False,self.board[i][j])
					allValidMoveSets2 = getSingleValidMoveset(self,i,j,True,self.board[i][j])
					if len(allValidMoveSets1) > 0  or len(allValidMoveSets2) > 0:
						return 1		
					
		return 0
     
	def mutari_joc(self, playerColor):
		"""
		Vedem daca userul curent este intr-un movespree (poate sau a capturat o piese)
		Returnam toate mutarile valide al acelui jucator (daca este sau nu obligat sa captureze)
		"""

		moveSpree = playerHasSpreeMoves(self,playerColor)
		allValidMoveSets = getAllValidMovesets(self,playerColor,moveSpree)

		return allValidMoveSets
	
	#Apelam mutari joc ca sa ne returneze toate mutarile valide 
	def getAllFutureStates(self,playerColor):
		gamesList = []
		mutari = self.mutari_joc(playerColor)
	
		for startPosition, futureMovesList in mutari.items():
				for finalPosition in futureMovesList:
						tmpArray = copy.deepcopy(self.board)
						updateBoard(tmpArray,startPosition,finalPosition,playerColor)
						newGame = Joc(tmpArray)
						gamesList.append(newGame)
		return gamesList


	def euristicaSlaba(self):
		#Cu cat are mai multe piese , cu atat scorul euristicii este mai mare
		#Atribuim regelui valoare 2 si piesei normale valoarea 2

		punctaj_regi_jmax = 0
		punctaj_piese_jmax = 0

		punctaj_regi_jmin = 0
		punctaj_piese_jmin = 0

		for linie in self.board: # iau fiecare linie si adaug la punctaje scorurile obtinute per linie
			
			punctaj_regi_jmin = punctaj_regi_jmin + 2 * linie.count(Joc.JMIN.upper())
			punctaj_piese_jmin = punctaj_piese_jmin + linie.count(Joc.JMIN.lower())

			punctaj_regi_jmax = punctaj_regi_jmax + 2 * linie.count(Joc.JMAX.upper())
			punctaj_piese_jmax = punctaj_piese_jmax + linie.count(Joc.JMAX.lower())


		punctaj_JMAX = punctaj_regi_jmax + punctaj_piese_jmax
		punctaj_JMIN = punctaj_regi_jmin + punctaj_piese_jmin

		# intorc diferenta dintre punctaje
		return punctaj_JMAX - punctaj_JMIN
    
   
	def euristicaOptima(self):
		#Cu cat o piese se apropie mai mult de marginea cealalta (ataca si are potential sa fie rege)
        #Cu atat are scor mai mare
        #Astfel pentru ai calculam scorul pt fiecare piese fiind = nr liniei piese + (1 sau 2 in functie de rege sau pion)
        # Include prima euristica , doar ca tine cont si de potentialul de a se transforma in rege
		punctaj_regi_jmax = 0
		punctaj_piese_jmax = 0

		punctaj_regi_jmin = 0
		punctaj_piese_jmin = 0

		for i in range(Joc.NR_LINII):
			for j in range(Joc.NR_COLOANE):

				if self.board[i][j] != Joc.GOL: 
                    
					if self.board[i][j] == Joc.JMAX.upper(): 
 						punctaj_regi_jmax = punctaj_regi_jmax + Joc.NR_LINII + 2

					elif self.board[i][j] == Joc.JMAX.lower(): 
						punctaj_piese_jmax = punctaj_piese_jmax + i + 1

					elif self.board[i][j] == Joc.JMIN.upper(): 
						punctaj_regi_jmin = punctaj_regi_jmin + Joc.NR_LINII + 2

					elif self.board[i][j] == Joc.JMIN.lower():
 						punctaj_piese_jmin = punctaj_piese_jmin + i + 1

		punctaj_JMAX = punctaj_regi_jmax + punctaj_piese_jmax
		punctaj_JMIN = punctaj_regi_jmin + punctaj_piese_jmin

        
		return punctaj_JMAX - punctaj_JMIN
 
	
	# linie deschisa inseamna linie pe care jucatorul mai poate forma o
	# configuratie castigatoare
	def linie_deschisa(self, lista, jucator):
		"""
		# rezolvare alternativa:
		juc_opus = 'x' if jucator=='0' else '0'
		if juc_opus in lista:
			return 0
		return 1
		"""

		# obtin multimea simbolurilor de pe linie
		mt = set(lista)
		# verific daca sunt maxim 2 simboluri
		if len(mt) <= 2:
			# daca multimea simbolurilor nu are alte simboluri decat pentru cel de
			# "gol" si jucatorul curent
			if mt <= {Joc.GOL, jucator}:  # incluziune de seturi
				# inseamna ca linia este deschisa
				return 1
			else:
				return 0
		else:
			return 0

	def linii_deschise(self, jucator):
		return None
	
	
	def chooseEuristic(self):
		return self.euristicaOptima()

	def estimeaza_scor(self, adancime, playerColor):
		t_final = self.final(self)
		if t_final == Joc.JMAX:
			return 999 + adancime
		elif t_final == Joc.JMIN:
			return -999 - adancime
		elif t_final == 'remiza':
			return 0
		else:
			return self.chooseEuristic()

	def finalScore(self, playerColor):
		finalscr = 0
		for i in self.board:
			for j in i:
				if(j == playerColor or j==playerColor.upper()):
					finalscr+=1
		return finalscr
          
          
 
	def __str__(self):
	#	sir= (" ".join([str(x) for x in self.matr[0:3]])+"\n"+
	#	" ".join([str(x) for x in self.matr[3:6]])+"\n"+
	#	" ".join([str(x) for x in self.matr[6:9]])+"\n")

		return None


class Stare:
	"""
	Clasa folosita de algoritmii minimax si alpha-beta
	Are ca proprietate tabla de joc
	Functioneaza cu conditia ca in cadrul clasei Joc sa fie definiti JMIN si JMAX (cei doi jucatori posibili)
	De asemenea cere ca in clasa Joc sa fie definita si o metoda numita mutari_joc() care ofera lista cu
	configuratiile posibile in urma mutarii unui jucator
	"""
	ADANCIME_MAX = None

	def __init__(self, tabla_joc, j_curent, adancime, parinte=None, scor=None):
		self.tabla_joc = tabla_joc  # un obiect de tip Joc => „tabla_joc.matr”
		self.j_curent = j_curent  # simbolul jucatorului curent

		# adancimea in arborele de stari
		#	(scade cu cate o unitate din „tata” in „fiu”)
		self.adancime = adancime

		# scorul starii (daca e finala, adica frunza a arborelui)
		# sau scorul celei mai bune stari-fiice (pentru jucatorul curent)
		self.scor = scor
		self.moveSpree = False
		# lista de mutari posibile din starea curenta
		self.mutari_posibile = []  # lista va contine obiecte de tip Stare

		# cea mai buna mutare din lista de mutari posibile pentru jucatorul curent
		self.stare_aleasa = None

	def jucator_opus(self):
		if self.j_curent == Joc.JMIN:
			return Joc.JMAX
		else:
			return Joc.JMIN

	def mutari_stare(self):
		l_mutari = self.tabla_joc.getAllFutureStates(self.j_curent)
		juc_opus = self.jucator_opus()

		l_stari_mutari = [
    Stare(
        mutare,
        juc_opus,
        self.adancime - 1,
         parinte=self) for mutare in l_mutari]
		return l_stari_mutari

	def __str__(self):
		sir = str(self.tabla_joc) + "(Juc curent:" + self.j_curent + ")\n"
		return sir


""" Algoritmul MinMax """


def min_max(stare):

	# Daca am ajuns la o frunza a arborelui, adica:
	# - daca am expandat arborele pana la adancimea maxima permisa
	# - sau daca am ajuns intr-o configuratie finala de joc
	if stare.adancime == 0 or stare.tabla_joc.final(stare.j_curent):
		# calculam scorul frunzei apeland "estimeaza_scor"
		stare.scor = stare.tabla_joc.estimeaza_scor(stare.adancime,stare.j_curent)
		return stare

	# Altfel, calculez toate mutarile posibile din starea curenta
	stare.mutari_posibile = stare.mutari_stare()

	# aplic algoritmul minimax pe toate mutarile posibile (calculand astfel
	# subarborii lor)

	mutari_scor = [min_max(mutare) for mutare in stare.mutari_posibile]

	if stare.j_curent == Joc.JMAX :
		# daca jucatorul e JMAX aleg starea-fiica cu scorul maxim
		stare.stare_aleasa = max(mutari_scor, key=lambda x: x.scor)
	else:
		# daca jucatorul e JMIN aleg starea-fiica cu scorul minim
		stare.stare_aleasa = min(mutari_scor, key=lambda x: x.scor)

	# actualizez scorul „tatalui” = scorul „fiului” ales
	
	stare.scor = stare.stare_aleasa.scor
	return stare


def alpha_beta(alpha, beta, stare):
	# Daca am ajuns la o frunza a arborelui, adica:
	# - daca am expandat arborele pana la adancimea maxima permisa
	# - sau daca am ajuns intr-o configuratie finala de joc
	if stare.adancime == 0 or stare.tabla_joc.final(stare.j_curent):
		# calculam scorul frunzei apeland "estimeaza_scor"
		stare.scor = stare.tabla_joc.estimeaza_scor(stare.adancime,stare.j_curent)
		return stare

	# Conditia de retezare:
	if alpha >= beta:
		return stare  # este intr-un interval invalid, deci nu o mai procesez

	# Calculez toate mutarile posibile din starea curenta (toti „fiii”)
	stare.mutari_posibile = stare.mutari_stare()

	if stare.j_curent == Joc.JMAX:
		scor_curent = float('-inf')  # scorul „tatalui” de tip MAX

		# pentru fiecare „fiu” de tip MIN:
		for mutare in stare.mutari_posibile:
			# calculeaza scorul fiului curent
			stare_noua = alpha_beta(alpha, beta, mutare)

			# incerc sa imbunatatesc (cresc) scorul si alfa
			# „tatalui” de tip MAX, folosind scorul fiului curent
			if scor_curent < stare_noua.scor:
				stare.stare_aleasa = stare_noua
				scor_curent = stare_noua.scor

			if alpha < stare_noua.scor:
				alpha = stare_noua.scor
				if alpha >= beta:  # verific conditia de retezare
					break  # NU se mai extind ceilalti fii de tip MIN

	elif stare.j_curent == Joc.JMIN:
		scor_curent = float('inf')  # scorul „tatalui” de tip MIN

		# pentru fiecare „fiu” de tip MAX:
		for mutare in stare.mutari_posibile:
			stare_noua = alpha_beta(alpha, beta, mutare)

			# incerc sa imbunatatesc (scad) scorul si beta
			# „tatalui” de tip MIN, folosind scorul fiului curent
			if scor_curent > stare_noua.scor:
				stare.stare_aleasa = stare_noua
				scor_curent = stare_noua.scor

			if beta > stare_noua.scor:
				beta = stare_noua.scor
				if alpha >= beta:  # verific conditia de retezare
					break  # NU se mai extind ceilalti fii de tip MAX

	# actualizez scorul „tatalui” = scorul „fiului” ales
	stare.scor = stare.stare_aleasa.scor

	return stare





def printIfFinal(stare_curenta):
	final = stare_curenta.tabla_joc.final(stare_curenta.j_curent)
	if(final):
		if (final == "remiza"):
			print("Remiza!")
		else:
			#CaLCUL PUNCTAJ
			print("A castigat " + final)
			print("Scor Jucator{}".format(stare_curenta.tabla_joc.finalScore(stare_curenta.tabla_joc.JMIN)))
			print("Scor AI{}".format(stare_curenta.tabla_joc.finalScore(stare_curenta.tabla_joc.JMAX)))
			
		return True

	return False


def updateBoard(board,startPosition,endPosition,playerColor):
	if(board[startPosition[0]][startPosition[1]] == playerColor.upper()):
		playerColor = playerColor.upper()
	if (endPosition[0] == 7 and playerColor == "a") or (endPosition[0] == 0 and playerColor == "n"):
		board[endPosition[0]][endPosition[1]] = playerColor.upper()
	else:
		board[endPosition[0]][endPosition[1]] = playerColor
	x1 = startPosition[0]
	y1 = startPosition[1]
	x2 = endPosition[0]
	y2 = endPosition[1]
	board[x1][y1] = Joc.GOL
	if((x1+x2)%2==0 and (y1+y2)%2==0):
		tmpx = int((x1+x2)/2)
		tmpy = int((y1+y2)/2)
		board[tmpx][tmpy] = Joc.GOL
	
 
def isPiece(tileColor):
    if tileColor == Joc.GOL:
        return False
    else:
        return True

def areOppositePlayers(playerColor1,playerColor2):
	if (playerColor1 == "a" or playerColor1 == "A") and (playerColor2 == "n" or playerColor2 == "N"):
		return True
	elif (playerColor2 == "a" or playerColor2 == "A") and (playerColor1 == "n" or playerColor1 == "N"):
		return True
	else:
		return False


def isInsideBoard(position):
    if position[0] >= 0 and position[0] < 8 and position[1] >= 0 and position[1] < 8:
        return True
    else:
    	return False


def getMoveset(playercolor):
    if playercolor == "a":
    	return [[1, 1], [1, -1]]
    elif playercolor == "n":
    	return [[-1,1],[-1,-1]]
    elif playercolor == "A" or playercolor == "N" :
    	return [[1,-1],[-1, -1] , [1, 1], [-1, 1]]
    else:
    	return []
		

def hasSpreeMove(currentBoard,i,j,playerColor):
    moveSet = getMoveset(currentBoard.board[i][j])
    
    for m in moveSet:
        simpleJumpI = i+m[0]
        simpleJumpJ = j+m[1]
        if(isInsideBoard([simpleJumpI+m[0],simpleJumpJ+m[1]]) and areOppositePlayers(currentBoard.board[simpleJumpI][simpleJumpJ],playerColor) and currentBoard.board[simpleJumpI+m[0]][simpleJumpJ+m[1]]==currentBoard.GOL):
            return True
    return False
            
 
def getSingleValidMoveset(currentBoard, i , j, moveSpree, playerColor):
	moveSet = getMoveset(currentBoard.board[i][j])
	singleValidMoveset = []

	for m in moveSet:
		simpleJumpI = i+m[0]
		simpleJumpJ = j+m[1]
		if(isInsideBoard([simpleJumpI,simpleJumpJ]) and currentBoard.board[simpleJumpI][simpleJumpJ]==Joc.GOL and moveSpree == False):
			singleValidMoveset.append([simpleJumpI,simpleJumpJ])
		if(isInsideBoard([simpleJumpI+m[0],simpleJumpJ+m[1]]) and areOppositePlayers(currentBoard.board[simpleJumpI][simpleJumpJ],playerColor) and currentBoard.board[simpleJumpI+m[0]][simpleJumpJ+m[1]]==Joc.GOL and moveSpree == True):
			singleValidMoveset.append([simpleJumpI+m[0],simpleJumpJ+m[1]])
	return singleValidMoveset
            
                
def getAllValidMovesets(currentBoard, playerColor ,moveSpree = False):
    allValidMovesets = {}
    tmpBoard = currentBoard.board
    for i in range(0,8):
        for j in range(0,8):
            if(tmpBoard[i][j] == playerColor or tmpBoard[i][j] == playerColor.upper()):
                tmpMoveSet = getSingleValidMoveset(currentBoard,i,j, moveSpree,playerColor)
                if tmpMoveSet!= []:
                	allValidMovesets[(i,j)]=tmpMoveSet
    return allValidMovesets

def playerHasSpreeMoves(currentBoard,playerColor):
    for i in range(0,8):
        for j in range(0,8):
            if((currentBoard.board[i][j] == playerColor or currentBoard.board[i][j] == playerColor.upper()) and hasSpreeMove(currentBoard,i,j,playerColor)):
                return True
    return False
    
