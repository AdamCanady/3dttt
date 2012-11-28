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

# This file will define the necessary elements to achieve gameplay from
# the user.


################
# Dependencies #
################

# Here's what we'll need in order to get this thing to work

# graphics library
from graphics import *
from init import *
import math
import sys
import random
import time

# To output color in the Terminal. Requires termcolor.py to be in the assets 
# directory.
from termcolor import colored

###############
# The Program #
###############


def doGame(gameboard, gameWindow, gameBoardPixels):
# Create a function that runs the game
	AIvsAI = False
	choice = raw_input("Would you like to do AI vs AI? (y/n): ")
	if choice == "y" or choice == "Y":
		AIvsAI = True
	
	while gameWindow.winfo_exists():
		gameWindow.update()
		
		# This line delays the infinite loop so the program doesn't use so much processing power.
		# It makes the AI noticably slower, but when the human is playing, there is almost no
		# difference in terms of response time.
		#time.sleep(0.025)
		
		#AI vs. AI
		if AIvsAI:
			if gameWindow.winfo_exists():
				AImove(gameWindow,gameboard,gameBoardPixels,"blue","human")
				checkForWinner(gameWindow, gameboard)
			if gameWindow.winfo_exists():
				AImove(gameWindow,gameboard,gameBoardPixels,"red","computer")
				checkForWinner(gameWindow, gameboard)
		

def doBoardUpdate(player,x,y,board,boardPixels):
# Create a function that updates the board with the current game state.
# It takes in the locations of the click and determine's which square  in 
# the DB to put a piece in.

	# Check all the spaces on the board and determine if a human or the computer
	# occupies that space.
	
	for i in range(0,4):
		for j in range(0,4):
			for k in range(0,4):
				if (-15 < (boardPixels[i][j][k][0] - x) < 15) and \
					(-15 < (boardPixels[i][j][k][1] - y) < 15):
						position = (i,j,k)
	if board[position[0]][position[1]][position[2]] == 0:
		board[position[0]][position[1]][position[2]] = player
		print player.capitalize(), "is now in space:", (position[0],position[1],position[2])
	else: 
		print "Sorry, something has gone awry! Have a free turn."

	#print board


def AImove(window,board,boardPixels,color,player):
# Create a function that will grab the maximum #-in-a-row's that appear on the board
# and returns the number and the combination. Mainly, we're looking for 3-in-a-row's
# so the computer can stop the human from winning.

	# Have the AI evaluate the board and return a favorable move
	nextMove, reason = evaluateBoard(board)
	# Put that move into the correct spot on our board matrix
	board[nextMove[0]][nextMove[1]][nextMove[2]] = player
	
	# Use that correct spot to find where to plot the circle on the graphics window,
	# set the correct properties and plot the circle on the GUI.
	print player.capitalize(), "Next Move:", nextMove
	if "Defensive" in reason:
		print "Reason:", colored(reason, "red")
	else:
		print "Reason:", colored(reason, "blue")

	if color == "red":
		file = "redblaster.gif"
		color = (0,0,0)
	else:
		file = "blueblaster.gif"
		color = (255,255,255)
	# AI place move on screen
	aicirclebkgd = Circle(Point(boardPixels[nextMove[0]][nextMove[1]][nextMove[2]][0],\
		boardPixels[nextMove[0]][nextMove[1]][nextMove[2]][1]), 15)
	aicirclebkgd.setFill(color_rgb(color[0],color[1],color[2]))
	aicirclebkgd.setOutline(color_rgb(color[0],color[1],color[2]))
	aicirclebkgd.draw(window)
	aicircle = Image(Point(boardPixels[nextMove[0]][nextMove[1]][nextMove[2]][0],\
		boardPixels[nextMove[0]][nextMove[1]][nextMove[2]][1]), file)
	aicircle.draw(window)


def evaluateBoard(board):

# This function looks around on the board ot see if it can make an advantageous move.
# Priority of moves is listed below. Values are returned to the AImove function as a 
# tuple and a reason: (board,row,column), reason

# Organization:

# This function is organized so that offensive instant-wins take priority, then 
# defensive blocks (if the human has 3-in-a-row) are completed, if none are found, it 
# will look for an offensive move, which will increase the number it has in-a -ow. 
# If it can't increase the number it has in a row, the AI will make a random move.


########################################################################

# Instant Win Offensive

# If the computer can make a move that will allow it to win instantly, do that before
# defensive moves, other offensive moves or random moves.

	# Initialize a variable that will become true if a human is occupying a space in 
	# that specific win-combination (so the computer doesn't play in spaces that it can't
	# win with).
	humanOccupied = False

	# Initialize some other variables we'll need down the road
	check = 0
	openSpace = 0

	# Let's look around and find out where we have the maximum number in a row,
	# then place a piece there. Start by looking where we have 3-in-a-row and place a piece
	# in the final spot to win, if possible. 

	threshold = [3]

	for l in threshold:

		# Check 2 diagonals within each board
		for i in range(0,4):
			for k in range(0,4):
				if board[i][k][k] == 0:
					openSpace = (i,k,k)
				if board[i][k][k] == "computer":
					check += 1
				if board[i][k][k] == "human":
					humanOccupied = True
			if check >= l and openSpace != 0 and humanOccupied == False: 
				return openSpace, "Instant-Win Offensive 1D Diagonal"
			check = 0
			humanOccupied = False
			openSpace = 0
		for i in range(0,4):
			for k in range(0,4):
				if board[i][3-k][k] == 0:
					openSpace = (i,3-k,k)
				if board[i][3-k][k] == "computer":
					check += 1
				if board[i][3-k][k] == "human":
					humanOccupied = True
			if check >= l and openSpace != 0 and humanOccupied == False: 
				return openSpace, "Instant-Win Offensive 1D Diagonal"
			check = 0
			humanOccupied = False
			openSpace = 0

		# Check 8 diagonals across the rows of all the boards
		for i in range(0,4):
			for k in range(0,4):
				if board[k][k][i] == 0:
					openSpace = (k,k,i)
				if board[k][k][i] == "computer":
					check += 1
				if board[k][k][i] == "human":
					humanOccupied = True
			if check >= l and openSpace != 0 and humanOccupied == False: 
				return openSpace, "Instant-Win Offensive Cross-Board Column Diagonal"
			check = 0
			humanOccupied = False
			openSpace = 0

		for i in range(0,4):
			for k in range(0,4):
				if board[k][3-k][i] == 0:
					openSpace = (k,3-k,i)
				if board[k][3-k][i] == "computer":
					check += 1
				if board[k][3-k][i] == "human":
					humanOccupied = True
			if check >= l and openSpace != 0 and humanOccupied == False: 
				return openSpace, "Instant-Win Offensive Cross-Board Column Diagonal"
			check = 0
			humanOccupied = False
			openSpace = 0

		# Check 8 diagonals across the columns of all the boards
		for i in range(0,4):
			for k in range(0,4):
				if board[k][i][k] == 0:
					openSpace = (k,i,k)
				if board[k][i][k] == "computer":
					check += 1
				if board[k][i][k] == "human":
					humanOccupied = True
			if check >= l and openSpace != 0 and humanOccupied == False: 
				return openSpace, "Instant-Win Offensive Cross-Board Row Diagonal"
			check = 0
			humanOccupied = False
			openSpace = 0

		for i in range(0,4):
			for k in range(0,4):
				if board[k][i][3-k] == 0:
					openSpace = (k,i,3-k)
				if board[k][i][3-k] == "computer":
					check += 1
				if board[k][i][3-k] == "human":
					humanOccupied = True
			if check >= l and openSpace != 0 and humanOccupied == False: 
				return openSpace, "Instant-Win Offensive Cross-Board Row Diagonal"
			check = 0
			humanOccupied = False
			openSpace = 0

		# Check 16 vertical possibilities
		for i in range(0,4):
			for j in range(0,4):
				for k in range(0,4):
					if board[k][j][i] == 0:
						openSpace = (k,j,i)
					if board[k][j][i] == "computer":
						check += 1
					if board[k][j][k] == "human":
						humanOccupied = True
				if check >= l and openSpace != 0 and humanOccupied == False: 
					return openSpace, "Instant-Win Offensive Cross-Board Vertical"
				check = 0
				humanOccupied = False
				openSpace = 0

		# Check all the rows for all four boards (4x4 = 16)
		for i in range(0,4):
			for j in range(0,4):
				for k in range(0,4):
					if board[i][j][k] == 0:
						openSpace = (i,j,k)
					if board[i][j][k] == "computer":
						check += 1
					if board[i][j][k] == "human":
						humanOccupied = True
				if check >= l and openSpace != 0 and humanOccupied == False: 
					return openSpace, "Instant-Win Offensive Row"
				check = 0
				humanOccupied = False
				openSpace = 0

		# Check all the columns for all four boards (4x4 = 16)
		for i in range(0,4):
			for j in range(0,4):
				for k in range(0,4):
					if board[i][k][j] == 0:
						openSpace = (i,k,j)
					if board[i][k][j] == "computer":
						check += 1
					if board[i][k][j] == "human":
						humanOccupied = True
				if check >= l and openSpace != 0 and humanOccupied == False: 
					return openSpace, "Instant-Win Offensive Column"
				check = 0
				humanOccupied = False
				openSpace = 0


########################################################################

# Defensive AI:
# Look around to see if the player has 3-in-a-row anywhere, and cut it off if possible

	# Initialize some variables we'll need down the road
	check = 0
	openSpace = 0

	# Check all the rows for all four boards (4x4 = 16)
	for i in range(0,4):
		for j in range(0,4):
			for k in range(0,4):
				if board[i][j][k] == 0:
					openSpace = (i,j,k)
				if board[i][j][k] == "human":
					check += 1
			if check == 3 and openSpace != 0: 
				return openSpace, "Defensive 1D Row"
			check = 0
			openSpace = 0

	# Check all the columns for all four boards (4x4 = 16)
	for i in range(0,4):
		for j in range(0,4):
			for k in range(0,4):
				if board[i][k][j] == 0:
					openSpace = (i,k,j)
				if board[i][k][j] == "human":
					check += 1
			if check == 3 and openSpace != 0: 
				return openSpace, "Defensive 1D Column"
			check = 0
			openSpace = 0

	# Check 16 vertical possibilities
	for i in range(0,4):
		for j in range(0,4):
			for k in range(0,4):
				if board[k][j][i] == 0:
					openSpace = (k,j,i)
				if board[k][j][i] == "human":
					check += 1
			if check == 3 and openSpace != 0: 
				return openSpace, "Defensive Vertical"
			check = 0
			openSpace = 0

	# Check 2 diagonals within each board
	for i in range(0,4):
		for k in range(0,4):
			if board[i][k][k] == 0:
				openSpace = (i,k,k)
			if board[i][k][k] == "human":
				check += 1
		if check == 3 and openSpace != 0: 
			return openSpace, "Defensive 1D Diagonal"
		check = 0
		openSpace = 0
	for i in range(0,4):
		for k in range(0,4):
			if board[i][3-k][k] == 0:
				openSpace = (i,3-k,k)
			if board[i][3-k][k] == "human":
				check += 1
		if check == 3 and openSpace != 0: 
			return openSpace, "Defensive 1D Diagonal"
		check = 0
		openSpace = 0

	# Check 8 diagonals across the rows of all the boards
	for i in range(0,4):
		for k in range(0,4):
			if board[k][k][i] == 0:
				openSpace = (k,k,i)
			if board[k][k][i] == "human":
				check += 1
		if check == 3 and openSpace != 0: 
			return openSpace, "Defensive Cross-Board Row Diagonal"
		check = 0
		openSpace = 0

	for i in range(0,4):
		for k in range(0,4):
			if board[k][3-k][i] == 0:
				openSpace = (k,3-k,i)
			if board[k][3-k][i] == "human":
				check += 1
		if check == 3 and openSpace != 0: 
			return openSpace, "Defensive Cross-Board Row Diagonal"
		check = 0
		openSpace = 0

	# Check 8 diagonals across the columns of all the boards
	for i in range(0,4):
		for k in range(0,4):
			if board[k][i][k] == 0:
				openSpace = (k,i,k)
			if board[k][i][k] == "human":
				check += 1
		if check == 3 and openSpace != 0: 
			return openSpace, "Defensive Cross-Board Column Diagonal"
		check = 0
		openSpace = 0

	for i in range(0,4):
		for k in range(0,4):
			if board[k][i][3-k] == 0:
				openSpace = (k,i,3-k)
			if board[k][i][3-k] == "human":
				check += 1
		if check == 3 and openSpace != 0: 
			return openSpace, "Defensive Cross-Board Column Diagonal"
		check = 0
		openSpace = 0


	# Check 4 "diagonal" diagonals through each of the boards

	# Can't iterate through this, so programming them in manually
	# Diag 1
	if board[0][0][0] == "human" and board[1][1][1] == "human" and \
		board[2][2][2] == "human":
		if board[3][3][3] == 0:
			openSpace = (3,3,3)
			return openSpace, "Defensive Cross-Board Complex Diagonal"
	if board[0][0][0] == "human" and board[1][1][1] == "human" and \
		board[3][3][3] == "human":
		if board[2][2][2] == 0:
			openSpace = (2,2,2)
			return openSpace, "Defensive Cross-Board Complex Diagonal"
	if board[0][0][0] == "human" and \
		board[2][2][2] == "human" and board[3][3][3] == "human":
		if board[1][1][1] == 0:
			openSpace = (1,1,1)
			return openSpace, "Defensive Cross-Board Complex Diagonal"
	if board[1][1][1] == "human" and \
		board[2][2][2] == "human" and board[3][3][3] == "human":
		if board[0][0][0] == 0:
			openSpace = (0,0,0)
			return openSpace, "Defensive Cross-Board Complex Diagonal"
	
	# Diag 2		
	if board[0][0][3] == "human" and board[1][1][2] == "human" and \
		board[2][2][1] == "human":
		if board[3][3][0] == 0:
			openSpace = (3,3,0)
			return openSpace, "Defensive Cross-Board Complex Diagonal"
	if board[0][0][3] == "human" and board[1][1][2] == "human" and \
		board[3][3][0] == "human":
		if board[2][2][1] == 0:
			openSpace = (2,2,1)
			return openSpace, "Defensive Cross-Board Complex Diagonal"
	if board[0][0][3] == "human" and  \
		board[2][2][1] == "human" and board[3][3][0] == "human":
		if board[1][2][2] == 0:
			openSpace = (1,2,2)
			return openSpace, "Defensive Cross-Board Complex Diagonal"
	if board[1][1][2] == "human" and \
		board[2][2][1] == "human" and board[3][3][0] == "human":
		if board[0][0][3] == 0:
			openSpace = (0,0,3)
			return openSpace, "Defensive Cross-Board Complex Diagonal"

	# Diag 3		
	if board[0][3][0] == "human" and board[1][2][1] == "human" and \
		board[2][1][2] == "human":
		if board[3][0][3] == 0:
			openSpace = (3,0,3)
			return openSpace, "Defensive Cross-Board Complex Diagonal"
	if board[0][3][0] == "human" and board[1][2][1] == "human" and \
		board[3][0][3] == "human":
		if board[2][1][2] == 0:
			openSpace = (2,1,2)
			return openSpace, "Defensive Cross-Board Complex Diagonal"
	if board[0][3][0] == "human" and \
		board[2][1][2] == "human" and board[3][0][3] == "human":
		if board[1][2][1] == 0:
			openSpace = (1,2,1)
			return openSpace, "Defensive Cross-Board Complex Diagonal"
	if board[1][2][1] == "human" and \
		board[2][1][2] == "human" and board[3][0][3] == "human":
		if board[0][3][0] == 0:
			openSpace = (0,3,0)
			return openSpace, "Defensive Cross-Board Complex Diagonal"
	
	# Diag 4
	if board[0][3][3] == "human" and board[1][2][2] == "human" and \
		board[2][1][1] == "human":
		if board[3][0][0] == 0:
			openSpace = (3,0,0)
			return openSpace, "Defensive Cross-Board Complex Diagonal"
	if board[0][3][3] == "human" and board[1][2][2] == "human" and \
		board[3][0][0] == "human":
		if board[2][1][1] == 0:
			openSpace = (2,1,1)
			return openSpace, "Defensive Cross-Board Complex Diagonal"
	if board[0][3][3] == "human" and \
		board[2][1][1] == "human" and board[3][0][0] == "human":
		if board[1][2][2] == 0:
			openSpace = (1,2,2)
			return openSpace, "Defensive Cross-Board Complex Diagonal"
	if board[1][2][2] == "human" and \
		board[2][1][1] == "human" and board[3][0][0] == "human":
		if board[0][3][3] == 0:
			openSpace = (0,3,3)
			return openSpace, "Defensive Cross-Board Complex Diagonal"

# If we don't need to cut anything off, point it towards trying to win by achieving 
# more-in-a-row if possible.

########################################################################
# Offensive AI

#TODO: make the computer look for Cross-Board Complex Diagonals

# Look for possibilities where there is a piece and an open space so we can start getting
# pieces in-a-row. This AI is structured to check for diagonal possibilities first as it 
# will be harder for the user to notice the pattern if the AI is going for diagonals.

	# Initialize a variable that will become true if a human is occupying a space in 
	# that specific win-combination (so the computer doesn't play in spaces that it can't
	# win with).
	humanOccupied = False

	# Let's look around and find out where we have the maximum number in a row,
	# then place a piece there. Start by looking where we have 2-in-a-row, then 1
	# and place a piece next to it.
	threshold = [2,1]

	for l in threshold:

		# Check 2 diagonals within each board
		for i in range(0,4):
			for k in range(0,4):
				if board[i][k][k] == 0:
					openSpace = (i,k,k)
				if board[i][k][k] == "computer":
					check += 1
				if board[i][k][k] == "human":
					humanOccupied = True
			if check >= l and openSpace != 0 and humanOccupied == False: 
				return openSpace, "Offensive 1D Diagonal"
			check = 0
			humanOccupied = False
			openSpace = 0
		for i in range(0,4):
			for k in range(0,4):
				if board[i][3-k][k] == 0:
					openSpace = (i,3-k,k)
				if board[i][3-k][k] == "computer":
					check += 1
				if board[i][3-k][k] == "human":
					humanOccupied = True
			if check >= l and openSpace != 0 and humanOccupied == False: 
				return openSpace, "Offensive 1D Diagonal"
			check = 0
			humanOccupied = False
			openSpace = 0

		# Check 8 diagonals across the rows of all the boards
		for i in range(0,4):
			for k in range(0,4):
				if board[k][k][i] == 0:
					openSpace = (k,k,i)
				if board[k][k][i] == "computer":
					check += 1
				if board[k][k][i] == "human":
					humanOccupied = True
			if check >= l and openSpace != 0 and humanOccupied == False: 
				return openSpace, "Offensive Cross-Board Column Diagonal"
			check = 0
			humanOccupied = False
			openSpace = 0

		for i in range(0,4):
			for k in range(0,4):
				if board[k][3-k][i] == 0:
					openSpace = (k,3-k,i)
				if board[k][3-k][i] == "computer":
					check += 1
				if board[k][3-k][i] == "human":
					humanOccupied = True
			if check >= l and openSpace != 0 and humanOccupied == False: 
				return openSpace, "Offensive Cross-Board Column Diagonal"
			check = 0
			humanOccupied = False
			openSpace = 0

		# Check 8 diagonals across the columns of all the boards
		for i in range(0,4):
			for k in range(0,4):
				if board[k][i][k] == 0:
					openSpace = (k,i,k)
				if board[k][i][k] == "computer":
					check += 1
				if board[k][i][k] == "human":
					humanOccupied = True
			if check >= l and openSpace != 0 and humanOccupied == False: 
				return openSpace, "Offensive Cross-Board Row Diagonal"
			check = 0
			humanOccupied = False
			openSpace = 0

		for i in range(0,4):
			for k in range(0,4):
				if board[k][i][3-k] == 0:
					openSpace = (k,i,3-k)
				if board[k][i][3-k] == "computer":
					check += 1
				if board[k][i][3-k] == "human":
					humanOccupied = True
			if check >= l and openSpace != 0 and humanOccupied == False: 
				return openSpace, "Offensive Cross-Board Row Diagonal"
			check = 0
			humanOccupied = False
			openSpace = 0

		# Check 16 vertical possibilities
		for i in range(0,4):
			for j in range(0,4):
				for k in range(0,4):
					if board[k][j][i] == 0:
						openSpace = (k,j,i)
					if board[k][j][i] == "computer":
						check += 1
					if board[k][j][k] == "human":
						humanOccupied = True
				if check >= l and openSpace != 0 and humanOccupied == False: 
					return openSpace, "Offensive Cross-Board Vertical"
				check = 0
				humanOccupied = False
				openSpace = 0

		# Check all the rows for all four boards (4x4 = 16)
		for i in range(0,4):
			for j in range(0,4):
				for k in range(0,4):
					if board[i][j][k] == 0:
						openSpace = (i,j,k)
					if board[i][j][k] == "computer":
						check += 1
					if board[i][j][k] == "human":
						humanOccupied = True
				if check >= l and openSpace != 0 and humanOccupied == False: 
					return openSpace, "Offensive Row"
				check = 0
				humanOccupied = False
				openSpace = 0

		# Check all the columns for all four boards (4x4 = 16)
		for i in range(0,4):
			for j in range(0,4):
				for k in range(0,4):
					if board[i][k][j] == 0:
						openSpace = (i,k,j)
					if board[i][k][j] == "computer":
						check += 1
					if board[i][k][j] == "human":
						humanOccupied = True
				if check >= l and openSpace != 0 and humanOccupied == False: 
					return openSpace, "Offensive Column"
				check = 0
				humanOccupied = False
				openSpace = 0

########################################################################
# Random AI	

	# If no strategic move has been done, do a random (but valid) move:
	while True:
		a = random.randint(0,3)
		b = random.randint(0,3)
		c = random.randint(0,3)

		if board[a][b][c] == 0:
			return (a,b,c), "Random"






def checkForWinner(window,board):
# This function checks for a winner. It looks for all 76 win 
# conditions and stop gameplay if one is achieved.

# Before checking win conditions, it needs to decide whether or not a stalemate has occurred.
# It does this by searching through the board to see if there are any zeros. If no zeros exist,
# a stalemate has occurred and it displays it as such.
	
	staleCounter = 0

	for i in range(0,4):
		for j in range(0,4):
			if 0 not in board[i][j]:
				staleCounter += 1
	if staleCounter == 16:
		return displayStaleMate(window)

# If a stalemate has not occurred, go ahead and check if someone has won or not.

	# Check both players
	for player in ["human","computer"]:
		check = 0
	# Check each win condition and see if a player has won.

	# Check all the rows for all four boards (4x4 = 16)
		for i in range(0,4):
			for j in range(0,4):
				for k in range(0,4):
					if board[i][j][k] == player:
						check += 1
						if check == 4: 
							if player == "computer":
								displayWinner(window,"computer")
							elif player == "human":
								displayWinner(window,"human")
							return True
 				# Reset the check if no winner has been found in a given row
				check = 0

		# Check all the columns for all four boards (4x4 = 16)
		for i in range(0,4):
			for j in range(0,4):
				for k in range(0,4):
					if board[i][k][j] == player:
						check += 1
						if check == 4: 
							if player == "computer":
								displayWinner(window,"computer")
							elif player == "human":
								displayWinner(window,"human")
							return True
 
				check = 0

		# Check 16 vertical possibilities
		for i in range(0,4):
			for j in range(0,4):
				for k in range(0,4):
					if board[k][j][i] == player:
						check += 1
						if check == 4: 
							if player == "computer":
								displayWinner(window,"computer")
							elif player == "human":
								displayWinner(window,"human")
							return True
 
				check = 0
		# Check 2 diagonals within each board
		for i in range(0,4):
			for k in range(0,4):
				if board[i][k][k] == player:
					check += 1
					if check == 4: 
						if player == "computer":
							displayWinner(window,"computer")
						elif player == "human":
							displayWinner(window,"human")
						return True

			check = 0
		for i in range(0,4):
			for k in range(0,4):
				if board[i][3-k][k] == player:
					check += 1
					if check == 4: 
						if player == "computer":
							displayWinner(window,"computer")
						elif player == "human":
							displayWinner(window,"human")
						return True

			check = 0
		# Check 8 diagonals across the rows of all the boards
		for i in range(0,4):
			for k in range(0,4):
				if board[k][k][i] == player:
					check += 1
					if check == 4: 
						if player == "computer":
							displayWinner(window,"computer")
						elif player == "human":
							displayWinner(window,"human")
						return True

			check = 0
		for i in range(0,4):
			for k in range(0,4):
				if board[k][3-k][i] == player:
					check += 1
					if check == 4: 
						if player == "computer":
							displayWinner(window,"computer")
						elif player == "human":
							displayWinner(window,"human")
						return True

			check = 0
		# Check 8 diagonals across the columns of all the boards
		for i in range(0,4):
			for k in range(0,4):
				if board[k][i][k] == player:
					check += 1
					if check == 4: 
						if player == "computer":
							displayWinner(window,"computer")
						elif player == "human":
							displayWinner(window,"human")
						return True

			check = 0
		for i in range(0,4):
			for k in range(0,4):
				if board[k][i][3-k] == player:
					check += 1
					if check == 4: 
						if player == "computer":
							displayWinner(window,"computer")
						elif player == "human":
							displayWinner(window,"human")
						return True

			check = 0
		# Check 4 "diagonal" diagonals through each of the boards

		# Can't iterate through this, so programming them in manually
		if board[0][0][0] == player and board[1][1][1] == player and \
			board[2][2][2] == player and board[3][3][3] == player:
				if player == "computer":
					displayWinner(window,"computer")
				elif player == "human":
					displayWinner(window,"human")
				return True
		if board[0][0][3] == player and board[1][1][2] == player and \
			board[2][2][1] == player and board[3][3][0] == player:
				if player == "computer":
					displayWinner(window,"computer")
				elif player == "human":
					displayWinner(window,"human")
				return True
		if board[0][3][0] == player and board[1][2][1] == player and \
			board[2][1][2] == player and board[3][0][3] == player:
				if player == "computer":
					displayWinner(window,"computer")
				elif player == "human":
					displayWinner(window,"human")
				return True
		if board[0][3][3] == player and board[1][2][2] == player and \
			board[2][1][1] == player and board[3][0][0] == player:
				if player == "computer":
					displayWinner(window,"computer")
				elif player == "human":
					displayWinner(window,"human")
				return True
	# Create a check for stale-mate
	# ...look for 0's, if there are none, displayStaleMate(window)

	#print "No winner yet!"

	# Create a function that will display the winner

def displayWinner(window,winner):
	print
	print "!!!!!!!!!!!!!!!!!!!!!!!"
	print winner.capitalize(), "has won the match!"
	print
	# Make it so users can't play anymore and only the "Exit" button will work.
	window.play(False)
	wait = raw_input("Press Enter to Continue")
	window.close()

def displayStaleMate(window):
	print "A Stale-Mate has occured! Better play again!"
	window.play(False)
	wait = raw_input("Press Enter to Continue")
	window.close()
	sys.exit()


