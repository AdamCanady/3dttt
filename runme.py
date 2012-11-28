# TODO: clean up old code

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

# This file will be what the user runs in order to start up the program.
# It will contain everything necessary to initialize and run the gameplay
# and will display the winner once that is achieved.

################
# Dependencies #
################

# Here's what we'll load in order to make this thing work:

# grab sys so we can import things from other directories
import sys
sys.path.append('assets')

# graphics library
import graphics

# initialization script
import init

# gameplay script
import gameplay

###############
# The Program #
###############

# Create a function that starts up all the initialization processes.
def initialize():
	gameboard, gameBoardPixels = init.createDB()
	gameWindow = init.createGraphics(gameboard, gameBoardPixels)
	return gameboard, gameWindow, gameBoardPixels


def main():
	gameboard, gameWindow, gameBoardPixels = initialize()

	gameplay.doGame(gameboard, gameWindow, gameBoardPixels)

main()

