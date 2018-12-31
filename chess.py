"""
chess.py - Text-based chess game

By: Runaal Parmar
Dec 9, 2018
"""
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

my_board = Board()
saved_boards = []
saved_boards.insert(0, deepcopy(my_board))

turn_num = 1

while True:
	my_board.map_print()
	player = get_player(turn_num)

	if checks.is_king_in_check(my_board, player):
		print(colored("CHECK!", "red"))

	cords = checks.is_mate(my_board, player)

	if cords == "checkmate":
		print(colored("The " + player + " king is in checkmate!", "green"))
		winner = get_player(turn_num - 1)
		print(colored("The " + winner + " side is the winner!", "green"))
		cords = "exit"
	elif cords == "stalemate":
		print(colored("The " + player + " king is in stalemate!", "green"))
		print(colored("The match ends in a draw!", "green"))
		cords = "exit"
	elif cords == None:
		cords = my_board.clean_intake(player, turn_num) 

	if cords == "undo":
		if turn_num == 1:
			print(colored("Already at first turn!", "red"))
		else:
			turn_num -= 1
			saved_boards.pop()
			my_board = deepcopy(saved_boards[turn_num - 1])
	elif cords[:4] == "undo":
		turn_num = int(cords[5:])
		my_board = deepcopy(saved_boards[turn_num])
		saved_boards = saved_boards[0:turn_num]
	elif cords == "exit" or cords == "quit":
		print(colored("Exiting...", "red"))
		exit()
	else:
		vec = my_board.move(cords, player)
		if vec[0]:
			saved_boards.insert(turn_num, deepcopy(my_board))
			turn_num += 1
		else:
			print(colored(vec[1], "red"))
