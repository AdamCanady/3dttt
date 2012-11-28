################
# Project Info #
################

 CS 111 Final Project by Adam Canady
 Dave Musicant, Fall 2012

 In this project, I'll be creating 3-dimensional tic-tac-toe. It
 is played until a stale-mate occurs, or one player gets 4 in-a-row.
 The AI that is developed for this program works by using the Minimax
 algorithm that will minimize risk and maximize strategic plays by the
 computer.

####################
# File Information #
####################

This file details the following:
1. A description of the program and its features.
2. A brief description and justification of how it is constructed (classes, functions, etc.)
3. A discussion of the current status of the program, what works and what doesn't, etc.

#############################################################################################################

1. This program is an implementation of 3D Tic-Tac-Toe. It creates a window that the user can click
on to place a game piece on the game board. The AI responds with its own 'intelligent' move. On each
move, the program checks to see if there was a winner and displays who the winner was. If a stalemate
is reached, the program displays that a stalemate has been reached.

2. To start the program, the user must run the file 'runme.py' using Python. This file adds the
'assets' directory to the system path and allows it to import files within. It is constructed as such
to simplify the layout of the program. The only assets that cannot be placed in the 'assets' folder
are the graphics, because the graphics library only looks for files in the same directory as the root
program thread.

The file 'runme.py' initializes several variables, a gameboard and a window from 'init.py' (found in 
the 'assets' directory) and starts the doGame function from 'gameplay.py' (also in the 'assets' directory).

The function doGame starts an infinite loop to update the window until it is closed.

When a user clicks on the window, the button click is checked against a condition to see if they have clicked 
in a valid spot. If so, a game piece is placed in that spot and it is noted in the gameboard.

Upon an AI's turn, the computer calculates the current state of the gameboard and determines the best move
to do for the current turn. It does not look ahead turns, however (discussed later).

After each player's turn, the computer checks to see if either player has won. If so, it displays a message
detailing the winner.

Once a winner is declared, the program waits for the user to press 'Enter' before exiting.

3. Currently, the game is fully operational. If run, it asks the user whether or not they want to do AI vs. AI
mode. If so, it will run until one side wins. One thing that could be fixed is that in AI vs. AI mode, it
displays that a 'human' has won if the blue side wins. It could say that 'Computer Blue' has won instead.

Another more major change would be an improvement of the algorithm. Currently, the AI does not 'look ahead'
during turns. Instead, it considers the best possible move it can do right now. Here is a list of the
priorities it considers for moves:

	1. Instant-Win moves - where it had 3 in-a-row and can instantly win in this move.
	2. Defensive moves - if the user has 3 in-a-row, it will try to block one of the moves.
	3. Combo-building Offensive moves - if the AI has 2 or 1 in a row, it will make a move to extend
	   it's combo to try to build a win more quickly.

