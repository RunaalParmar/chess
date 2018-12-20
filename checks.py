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
	null_piece = Piece(" ", " ", " ")
	flag = [deepcopy(null_piece) for i in range(4)]

	for i in range(1, 8):
		# Ensure no checks from above:
		if pk_cords[0] - i > 0:
			if flag[0].get_type() == " ":
				flag[0] = board.map[pk_cords[0]-i][pk_cords[1]]

		# Ensure no checks from below:
		if pk_cords[0] + i < 8:
			if flag[1].get_type() == " ":
				flag[1] = board.map[pk_cords[0]+i][pk_cords[1]]

		# Ensure no checks from the left:
		if pk_cords[1] - i > 0:
			if flag[2].get_type() == " ":
				flag[2] = board.map[pk_cords[0]][pk_cords[1]-i]

		# Ensure no checks from the right:
		if pk_cords[1] + i < 8:
			if flag[3].get_type() == " ":
				flag[3] = board.map[pk_cords[0]][pk_cords[1]+i]

	# Check all flags for threats from cardinal directions
	for threat in flag:
		if threat.get_color() != player:
			if threat.get_type() == "queen" or threat.get_type() == "rook":
				return True

	# King is not in check from cardinal direction!
	return False

def in_check_from_diagonal(board, pk_cords, player):
	"""
		Determines if in check from a diagonal queen/bishop
	"""
	null_piece = Piece(" ", " ", " ")
	flag = [deepcopy(null_piece) for i in range(4)]

	for i in range(1, 8):
		# Ensure no checks a1 diagonal:
		if pk_cords[0] + i < 8 and pk_cords[1] - i > 0:
			if flag[0].get_type() == " ":
				flag[0] = board.map[pk_cords[0]+i][pk_cords[1]-i]

		# Ensure no checks a8 diagonal:
		if pk_cords[0] - i > 0 and pk_cords[1] - i > 0:
			if flag[1].get_type() == " ":
				flag[1] = board.map[pk_cords[0]-i][pk_cords[1]-i]

		# Ensure no checks h1 diagonal:
		if pk_cords[0] + i < 8 and pk_cords[1] + i < 8:
			if flag[2].get_type() == " ":
				flag[2] = board.map[pk_cords[0]+i][pk_cords[1]+i]

		# Ensure no checks h8 diagonal:
		if pk_cords[0] - i > 0 and pk_cords[1] + i < 8:
			if flag[3].get_type() == " ":
				flag[3] = board.map[pk_cords[0]-i][pk_cords[1]+i]

	# Check each flag for a threatening piece
	for threat in flag:
		if threat.get_color() != player:
			if threat.get_type() == "queen" or threat.get_type() == "bishop":
				return True

	# If this point is reached, king is not in check from diagonal direction!
	return False

def is_king_in_check(board, player):
	"""
		Ensures the player does not place their own king in check.
	"""
	# Find cordinates of the king
	pk_cords = find_king(board, player)

	# In check from enemy knight?
	if in_check_from_knight(board, pk_cords, player):
		print(colored("In check from the Knight!", "red"))
		return True

	# In check from enemy pawn?
	if in_check_from_pawn(board, pk_cords, player):
		print(colored("In check from the Pawn!", "red"))
		return True
		
	# In check from enemy king?
	if in_check_from_king(board, pk_cords, player):
		print(colored("In check from the enemy King!", "red"))
		return True

	# In check from cardinal direction? queen/rook
	if in_check_from_cardinal(board, pk_cords, player):
		print(colored("Cannot move into or stay in check!"))
		return True

	# In check from diagonal direction? queen/bishop
	if in_check_from_diagonal(board, pk_cords, player):
		print(colored("Cannot move into or stay in check!"))
		return True

	# The king is not in check from any direction
	return False 

def is_mate(board, player):
	"""
		Determine if the king is in checkmate or stalemate, 
		returns a string to indicate the result
	"""
	return None

	# Find cordinates of the king
	pk_cords = find_king(board, player)

	# Check if it is possible to move out of the way
	for move in king_moves:
		test_board = deepcopy(board)

		k_cords = [pk_cords[0] + move[0], pk_cords[1] + move[1]]

        test_board.map[k_cords[0]][k_cords[1]] = test_board.map[pk_cords[0]][pk_cords[1]]
        test_board.map[pk_cords[0]][pk_cords[1]] = Piece(" ", " ", " ")

		if not(is_king_in_check(test_board, player)):
			return None

	# Check if it is possible to take the offending piece
	













