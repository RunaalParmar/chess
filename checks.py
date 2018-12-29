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

b_pawn_moves = [
	(2,0),(1,0),(1,1),(1,-1)
]

w_pawn_moves = [
	(-2,0),(-1,0),(-1,1),(-1,-1)
]

rook_moves = [
	(0,1),(0,2),(0,3),(0,4),(0,5),(0,6),(0,7),
	(0,-1),(0,-2),(0,-3),(0,-4),(0,-5),(0,-6),(0,-7),
	(1,0),(2,0),(3,0),(4,0),(5,0),(6,0),(7,0),
	(-1,0),(-2,0),(-3,0),(-4,0),(-5,0),(-6,0),(-7,0)
]

bishop_moves = [
	(1,1),(2,2),(3,3),(4,4),(5,5),(6,6),(7,7),
	(-1,-1),(-2,-2),(-3,-3),(-4,-4),(-5,-5),(-6,-6),(-7,-7),
	(1,-1),(2,-2),(3,-3),(4,-4),(5,-5),(6,-6),(7,-7),
	(-1,1),(-2,2),(-3,3),(-4,4),(-5,5),(-6,6),(-7,7)
]

queen_moves = rook_moves + bishop_moves

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
	return False

def in_check_from_king(board, pk_cords, player):
	"""
		Determine if king would be in check from enemy king
	"""
	for move in king_moves:
		row = pk_cords[0] + move[0]
		col = pk_cords[1] + move[1]
		if row < 8 and row >= 0 and col < 8 and col >= 0:
			if board.map[row][col].get_type() == "king":
				return True
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

	return False

def is_king_in_check(board, player):
	"""
		Ensures the player does not place their own king in check.
	"""
	# Find cordinates of the king
	pk_cords = find_king(board, player)

	# In check from enemy knight?
	if in_check_from_knight(board, pk_cords, player):
		return True

	# In check from enemy pawn?
	elif in_check_from_pawn(board, pk_cords, player):
		return True
		
	# In check from enemy king?
	elif in_check_from_king(board, pk_cords, player):
		return True

	# In check from cardinal direction? queen/rook
	elif in_check_from_cardinal(board, pk_cords, player):
		return True

	# In check from diagonal direction? queen/bishop
	elif in_check_from_diagonal(board, pk_cords, player):
		return True

	return False

def is_mate(board, player):
	"""
		Determine if the king is in checkmate or stalemate, 
		returns a string to indicate the result
	"""
	# Comment comment comment
	for row in range(8):
		for col in range(8):
			if board.map[row][col].get_color() == player:
				piece_type = board.map[row][col].get_type()

				if piece_type == "knight":
					p_moves = knight_moves
				elif piece_type == "bishop":
					p_moves = bishop_moves
				elif piece_type == "rook":
					p_moves = rook_moves
				elif piece_type == "queen":
					p_moves = queen_moves
				elif piece_type == "king":
					p_moves = king_moves
				elif piece_type == "pawn" and player == "black":
					p_moves = b_pawn_moves
				else:
					p_moves = w_pawn_moves

				for move in p_moves:
					end0 = row + move[0]
					end1 = col + move[1]

					if end0 < 8 and end1 < 8 and end0 >= 0 and end1 >= 0: 
						cords = [row, col, end0, end1]
						test_board = deepcopy(board)
						vec = test_board.move(cords, player)
						if vec[0]: 
							return None

	if is_king_in_check(board, player):
		cords = "checkmate"
	else:
		cords = "stalemate"

	return cords

