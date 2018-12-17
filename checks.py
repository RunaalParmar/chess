"""
checks.py - Ensures neither kind moves into or remains in check 

By: Runaal Parmar 
Dec 13, 2018
"""
from copy import deepcopy
from termcolor import colored
from piece import Piece

knight_moves = [
	(1,2),(2,1),(-1,2),(-2,1),(1,-2),(2,-1),(-1,-2),(-2,-1)
]

king_moves = [
	(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)
]

def find_king(board, player):
	"""
		Find and return the coordinates of own kings
	"""
	k_cords = [9, 9]
	for row in range(8):
		for col in range(8):
			if board.map[row][col].get_type() == "king":
				# Save king location
				if board.map[row][col].get_color() == player:
					k_cords[0] = row
					k_cords[1] = col
	return k_cords

def in_check_from_knight(board, pk_cords, player):
	"""
		Determine if king would be in check from enemy knight
	"""
	for move in knight_moves:
		row = pk_cords[0] + move[0]
		col = pk_cords[1] + move[1]
		if row < 8 and row >= 0 and col < 8 and col >= 0:
			if board.map[row][col].get_type() == "knight":
				if (board.map[row][col].get_color() != player):
					return True
				else:
					return False

def in_check_from_pawn(board, pk_cords, player):
	"""
		Determine if king would be in check from enemy pawn
	"""
	if player == "white":
		if board.map[pk_cords[0]-1][pk_cords[1]+1].get_type() == "pawn":
			if board.map[pk_cords[0]-1][pk_cords[1]+1].get_color() != player:
				return True
		if board.map[pk_cords[0]-1][pk_cords[1]-1].get_type() == "pawn":
			if board.map[pk_cords[0]-1][pk_cords[1]-1].get_color() != player:
				return True
	else:
		if board.map[pk_cords[0]+1][pk_cords[1]+1].get_type() == "pawn":
			if board.map[pk_cords[0]+1][pk_cords[1]+1].get_color() != player:
				return True
		if board.map[pk_cords[0]+1][pk_cords[1]-1].get_type() == "pawn":
			if board.map[pk_cords[0]+1][pk_cords[1]-1].get_color() != player:
				return True

def in_check_from_king(board, pk_cords, player):
	"""
		Determine if king would be in check from enemy king
	"""
	for move in king_moves:
		row = pk_cords[0] + move[0]
		col = pk_cords[1] + move[1]
		if row < 8 and row >= 0 and col < 8 and col >= 0:
			if board.map[row][col].get_type() == "king":
				print(colored("Cannot move into check from enemy king"))
				return True
			else:
				return False

def in_check_from_cardinal(board, pk_cords, player):
	"""
		Determine if in check from enemy rook or queen (non diagonal)
	"""
	up_flag = " "
	down_flag = " "
	left_flag = " "
	right_flag = " "

	for i in range(8):
		# Ensure no checks from above:
		if pk_cords[0] - i > 0:
			if up_flag == " ":
				if board.map[pk_cords[0]-i][pk_cords[1]].get_color() != player:
					up_flag = board.map[pk_cords[0]-i][pk_cords[1]].get_type()
		if up_flag == "queen" or up_flag == "rook":
			return True

		# Ensure no checks from below:
		if pk_cords[0] + i < 8:
			if down_flag == " ":
				if board.map[pk_cords[0]+i][pk_cords[1]].get_color() != player:
					down_flag = board.map[pk_cords[0]+i][pk_cords[1]].get_type()
		if down_flag == "queen" or down_flag == "rook":
			return True

		# Ensure no checks from the left:
		if pk_cords[1] - i > 0:
			if left_flag == " ":
				if board.map[pk_cords[0]][pk_cords[1]-i].get_color() != player:
					left_flag = board.map[pk_cords[0]][pk_cords[1]-i].get_type()
		if left_flag == "queen" or left_flag == "rook":
			return True

		# Ensure no checks from the right:
		if pk_cords[1] + i < 8:
			if right_flag == " ":
				if board.map[pk_cords[0]][pk_cords[1]+i].get_color() != player:
					right_flag = board.map[pk_cords[0]][pk_cords[1]+i].get_type()
		if right_flag == "queen" or right_flag == "rook":
			return True

	return False

def in_check_from_diagonal(board, pk_cords, player):
	"""
		Determines if in check from a diagonal queen/bishop
	"""
	return False

def puts_king_in_check(board, cords, player):
	"""
		Ensures the player does not place their own king in check.
	"""
	# Create duplicate board
	test_board = deepcopy(board)

	# Make the desired move on duplicate board
	test_board.map[cords[2]][cords[3]] = test_board.map[cords[0]][cords[1]]
	test_board.map[cords[0]][cords[1]] = Piece(" ", " ", " ")

	# Find cordinate of kings, and save own king locatino
	pk_cords = find_king(test_board, player)

	# In check from enemy knight?
	if in_check_from_knight(test_board, pk_cords, player):
		print(colored("In check from the Knight!", "red"))
		return True

	# In check from enemy pawn?
	if in_check_from_pawn(test_board, pk_cords, player):
		print(colored("In check from the Pawn!", "red"))
		return True
		
	# In check from enemy king?
	if in_check_from_king(test_board, pk_cords, player):
		print(colored("In check from the enemy King!", "red"))
		return True

	# In check from cardinal direction? queen/rook
	if in_check_from_cardinal(test_board, pk_cords, player):
		print(colored("Cannot move into or stay in check!"))
		return True

	# In check from diagonal direction? queen/bishop
	if in_check_from_diagonal(test_board, pk_cords, player):
		print(colored("Cannot move into or stay in check!"))
		return True

	return False 

