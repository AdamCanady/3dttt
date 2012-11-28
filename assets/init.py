################
# Project Info #
################

# CS 111 Final Project by Adam Canady
# Dave Musicant, Fall 2012

# In this project, I'll be creating 3-dimensional tic-tac-toe. It
# is played until a stale-mate occurs, or one player gets 4 in-a-row.
# The AI that is developed for this program works by using the Minimax
# algorithm that will minimize risk and maximize strategic plays by the
# computer.

####################
# File Information #
####################

# This file will contain all the necessary things to build up the framework
# for the game to run off of.

# Space background from: 
# http://www.selepri.com/Ministry/Gaming/tabid/114/Default.aspx

###############
# The Program #
###############

# import the modules we need
from graphics import *
from gameplay import *

# Create the data storage space for the players to play on.
def createDB():
	board1 = [[0,0,0,0],
			  [0,0,0,0],
			  [0,0,0,0],
			  [0,0,0,0]]
	board2 = [[0,0,0,0],
			  [0,0,0,0],
			  [0,0,0,0],
			  [0,0,0,0]]
	board3 = [[0,0,0,0],
			  [0,0,0,0],
			  [0,0,0,0],
			  [0,0,0,0]]
	board4 = [[0,0,0,0],
			  [0,0,0,0],
			  [0,0,0,0],
			  [0,0,0,0]]

	board = [board1, board2, board3, board4]

	board1pixels = [[(68,153),(109,153),(150,153),(192,153)],
			   		[(65,176),(109,176),(152,176),(192,176)],
			  		[(60,202),(108,202),(153,202),(198,202)],
			  		[(60,229),(108,229),(154,229),(201,229)]]
	board2pixels = [[(69,282),(107,282),(151,282),(191,282)],
			  		[(64,310),(107,310),(151,310),(194,310)],
			  		[(61,340),(107,340),(151,340),(197,340)],
			  		[(60,373),(107,373),(151,373),(201,373)]]
	board3pixels = [[(66,432),(108,432),(151,432),(191,432)],
			  		[(64,463),(108,463),(151,463),(195,463)],
			  		[(62,496),(108,496),(151,496),(198,496)],
			  		[(59,532),(108,532),(151,532),(202,532)]]
	board4pixels = [[(67,590),(108,590),(152,590),(193,590)],
			  		[(64,625),(108,625),(152,625),(193,625)],
			  		[(62,664),(108,664),(152,664),(198,664)],
			  		[(58,706),(108,706),(152,706),(200,706)]]

	boardPixels = [board1pixels,board2pixels,board3pixels,board4pixels]

	return board, boardPixels

def createGraphics(board, boardPixels):

	class ClickableWindow(GraphWin):

		# initialize the clickable window as a GraphWin with all click actions handled
		# through the mouseHandler function
		def __init__(self, *args):
			GraphWin.__init__(self, *args)
			self.setBackground(color_rgb(255, 255, 255))
			
			background = Image(Point(250,380), "background.gif")
			background.draw(self)
			
			self.bind_all('<Button-1>', self.mouseHandler)

# Human vs. AI
		
		def mouseHandler(self, event):
			#print "X:", event.x, "Y:", event.y
			move = False
			# Draw a circle where the user placed it
			for i in range(0,4):
				for j in range(0,4):
					for k in range(0,4):
						if (-15 < (boardPixels[i][j][k][0] - event.x) < 15) and \
							(-15 < (boardPixels[i][j][k][1] - event.y) < 15):
								x = boardPixels[i][j][k][0]
								y = boardPixels[i][j][k][1]
								if board[i][j][k] == 0:
									move = True
			# Check for quit game button press
			if 289 < event.x < 444 and 664 < event.y < 707:
				gameWindow.close()

			# Update the correct board to indicate the current game state
			if move:
				if gameWindow.winfo_exists():

					humancirclebkgd = Circle(Point(x,y), 15)
					humancirclebkgd.setFill(color_rgb(255,255,255))
					humancirclebkgd.setOutline(color_rgb(255,255,255))
					humancirclebkgd.draw(self)

					humancircle = Image(Point(x,y), "blueblaster.gif")
					humancircle.draw(self)

					doBoardUpdate("human",event.x,event.y,board,boardPixels)
					checkForWinner(self, board)
				
				if gameWindow.winfo_exists():
					AImove(self,board,boardPixels,"red","computer")
					checkForWinner(self, board)
			else:
				print "Please make a valid move."
		
		# Only allow users to click the Exit button. (Ignore other input)
		def exitOnly(self, event):
			# Check for quit game button press
			if 289 < event.x < 444 and 664 < event.y < 707:
				gameWindow.close()

		# Reassign mouse clicks to exitOnly so that users can't play after 
		# someone has won.
		def play(self, play):
			if play == False:
				self.bind_all('<Button-1>', self.exitOnly)


	gameWindow = ClickableWindow('3D Tic-Tac-Toe by Adam Canady', 500, 760)
	return gameWindow