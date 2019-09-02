"""
chess.py - Text-based chess game

By: Runaal Parmar
Dec 9, 2018
"""
import os
from copy import deepcopy
from termcolor import colored
from board import Board
import checks

def get_player(turn_num):
	"""
		returns the player for the current turn number
	"""
	if turn_num % 2 == 1:
		player = "white"
	else:
		player = "black"
	return player

# Save initial state of the board as turn 0
my_board = Board()
prev_board = deepcopy(my_board)
saved_boards = []
saved_boards.insert(0, deepcopy(my_board))

# Begin turn 1
turn_num = 1

while True:
	my_board.map_print()
	player = get_player(turn_num)

	# Notify the player if they are in check
	if checks.is_king_in_check(my_board, player):
		print(colored("CHECK!", "red"))

	# Cords holds the coordinates for the moves, but also holds 
	# any special commands, such as exit, quit, undo, etc.
	cords = checks.is_mate(my_board, player, prev_board)

	# If the player is in checkmate, end the game and display the winner
	if cords == "checkmate":
		print(colored("The " + player + " king is in checkmate!", "green"))
		winner = get_player(turn_num - 1)
		print(colored("The " + winner + " side is the winner!", "green"))
		cords = "exit"
	# If the player is in stalemate, end the game and display a draw
	elif cords == "stalemate":
		print(colored("The " + player + " king is in stalemate!", "green"))
		print(colored("The match ends in a draw!", "green"))
		cords = "exit"
	# If cords has no special commands, intake new set of coordinates
	elif cords == None:
		cords = my_board.clean_intake(player, turn_num) 

	# Undo one turn, if possible
	if cords == "undo":
		if turn_num == 1:
			print(colored("Already at first turn!", "red"))
		else:
			turn_num -= 1
			saved_boards.pop()
			my_board = deepcopy(saved_boards[turn_num - 1])
			prev_board = deepcopy(saved_boards[turn_num - 2])
	# Undo to desired turn, if possible
	elif cords[:4] == "undo":
		turn_num = int(cords[5:])
		my_board = deepcopy(saved_boards[turn_num - 1])
		prev_board = deepcopy(saved_boards[turn_num - 2])
		saved_boards = saved_boards[0:turn_num - 1]

	# End game if requested by "exit" or "quit"
	elif cords == "exit" or cords == "quit":
		print(colored("Exiting...", "red"))
		exit()

	# If no special actions are required, attempt to move the piece
	else:
		vec = my_board.move(cords, player, prev_board)
		if vec[0]:
			prev_board = deepcopy(saved_boards[turn_num - 1])
			saved_boards.insert(turn_num, deepcopy(my_board))
			turn_num += 1
			os.system('clear')
		else:
			# Print error message
			os.system('clear')
			print(colored(vec[1], "red"))
