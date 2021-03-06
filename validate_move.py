"""
validate_move.py - Defines the checks which prevent non-valid moves in chess

By: Runaal Parmar 
Dec 17, 2018
"""
from termcolor import colored
from copy import deepcopy
from piece import Piece
import checks

def is_valid_pawn_move(board, cords, player, row_vec, col_vec, prev_board):
	"""
		Checks if the requested move is valid for a pawn
	"""
	# Define default return
	vec = [True]

	# Determine if the move/attack is valid for either player
	if player == "black" and col_vec == 0 and row_vec == 1:
		black_move = True
	else:
		black_move = False
	if player == "white" and col_vec == 0 and row_vec == -1:
		white_move = True
	else:
		white_move = False
	if player == "black" and abs(col_vec) == 1 and row_vec == 1:
		black_attacking = True
	else:
		black_attacking = False
	if player == "white" and abs(col_vec) == 1 and row_vec == -1:
		white_attacking = True
	else:
		white_attacking = False

	# Either color moving the pawn 2 steps
	if col_vec == 0 and abs(row_vec) == 2:
		if board.map[cords[2]][cords[3]].get_symbol() == " ":
			if cords[0] != 1 and cords[0] != 6:
				vec = [False, "Pawn can only move 2 spaces on its first move!"]
		else:
			vec = [False, "Pawn cannot walk into opposing piece!"]

	# Either color moving the pawn 1 step
	elif white_move or black_move:
		if board.map[cords[2]][cords[3]].get_symbol() == " ":
			if cords[2] == 7 or cords[2] == 0:
				board.map[cords[0]][cords[1]].promote(cords, player)
		else:
			vec = [False, "Pawn cannot walk into opposing piece!"]

	# Either color attacking with the pawn
	elif white_attacking or black_attacking:
		if board.map[cords[2]][cords[3]].get_type() == " ":
			# En passant for white pawn
			if white_attacking:
				if board.map[cords[2]+1][cords[3]].get_type() == "pawn":
					if board.map[cords[2]+1][cords[3]].get_color() == "black":
						if prev_board.map[cords[2]+1][cords[3]].get_type() == " ":
							if prev_board.map[cords[2]][cords[3]].get_type() == " ":
								vec = [True]
								board.map[cords[2]+1][cords[3]] = Piece(" ", " ", " ", " ")
								return vec
			# En passant for black pawn
			elif black_attacking:
				if board.map[cords[2]-1][cords[3]].get_type() == "pawn":
					if board.map[cords[2]-1][cords[3]].get_color() == "white":
						if prev_board.map[cords[2]-1][cords[3]].get_type() == " ":
							if prev_board.map[cords[2]][cords[3]].get_type() == " ":
								vec = [True]
								board.map[cords[2]-1][cords[3]] = Piece(" ", " ", " ", " ")
								return vec
			# No valid piece to attack!
			vec = [False, "No pieces for the pawn to attack!"]

		# Found a piece for the pawn to attack
		elif board.map[cords[2]][cords[3]].get_color() != player:
			if cords[2] == 7 or cords[2] == 0:
				board.map[cords[0]][cords[1]].promote(cords, player)

	# Invalid move for the pawn
	else:
		vec = [False, "This is not a valid move for a pawn!"]

	return vec

def is_valid_king_move(board, cords, row_vec, col_vec, player):
	"""
		Checks if the requested move is valid for the king
	"""
	# The King can move one step in any direction
	if abs(row_vec) <= 1 and abs(col_vec) <= 1:
		vec = [True]
		return vec

	# Check if castling
	if abs(col_vec) == 2:
		if board.map[cords[0]][cords[1]].get_has_moved() == False:
			if col_vec < 0:
				col = 0
			else:
				col = 7
			mid_col = cords[1] + (col_vec//2)

			if board.map[cords[0]][mid_col].get_type() == " ":
				if board.map[cords[0]][col].get_has_moved() == False:
					if checks.is_king_in_check(board, player) == True:
						vec = [False, "Cannot castle while in check!"]
						return vec

					test_board = deepcopy(board)
					test_board.map[cords[0]][mid_col] = test_board.map[cords[0]][cords[1]]
					test_board.map[cords[0]][cords[1]] = Piece(" ", " ", " ", " ")
					if checks.is_king_in_check(test_board, player) == True:
						vec = [False, "Cannot castle through a check!"]
						return vec

					test_board = deepcopy(board)
					test_board.map[cords[0]][cords[3]] = test_board.map[cords[0]][cords[1]]
					test_board.map[cords[0]][cords[1]] = Piece(" ", " ", " ", " ")
					if checks.is_king_in_check(test_board, player) == True:
						vec = [False, "Cannot castle into a check!"]
						return vec

					# If this point is reached, the castle move is valid
					board.map[cords[0]][mid_col] = board.map[cords[0]][col]
					board.map[cords[0]][mid_col].set_has_moved()
					board.map[cords[0]][col] = Piece(" ", " ", " ", " ")
					vec = [True]
					return vec

			else:
				vec = [False, "Cannot castle through a piece!"]
				return vec

	vec = [False, "This is not a valid move for a King!"]
	return vec

def is_valid_knight_move(board, row_vec, col_vec):
	"""
		Checks if the requested move is valid for the knight
	"""
	# Define default return
	vec = [True]

	# Checks all 8 moves for the knight
	if abs(row_vec) == 2 and abs(col_vec) == 1:
		return vec
	elif abs(row_vec) == 1 and abs(col_vec) == 2:
		return vec

	vec = [False, "This is not a valid move for a Knight!"]
	return vec

def is_valid_queen_move(board, cords, row_vec, col_vec):
	"""
		Checks if the requested move is valid for the queen
	"""
	# Define default return
	vec = [True]

	collision = None
	# Checks diagonal 1
	if row_vec == col_vec:
		row1 = min(cords[0], cords[2]) + 1
		col1 = min(cords[1], cords[3]) + 1
		row2 = max(cords[0], cords[2])
		while row1 < row2:
			if board.map[row1][col1].get_symbol() != " ":
				collision = "yes"
			row1 += 1
			col1 += 1
	# Checks diagonal 2
	elif row_vec*-1 == col_vec:
		row1 = min(cords[0], cords[2]) + 1
		col1 = max(cords[1], cords[3]) - 1
		row2 = max(cords[0], cords[2])
		while row1 < row2:
			if board.map[row1][col1].get_symbol() != " ":
				collision = "yes"
			row1 += 1
			col1 -= 1
	# Checks the row if the move is valid
	elif row_vec == 0:
		start = min(cords[1], cords[3]) + 1
		end = max(cords[1], cords[3])
		while start < end:
			if board.map[cords[0]][start].get_symbol() != " ":
				collision = "yes"
			start += 1
	# Checks the column if the move is valid
	elif col_vec == 0:
		start = min(cords[0], cords[2]) + 1
		end = max(cords[0], cords[2])
		while start < end:
			if board.map[start][cords[1]].get_symbol() != " ":
				collision = "yes"
			start += 1
	else:
		vec = [False, "This is not a valid move for a Queen!"]
		return vec

	# If collisions occured, move is bad!
	if collision == "yes":
		vec = [False, "The Queen cannot pass through pieces!"]
	return vec

def is_valid_bishop_move(board, cords, row_vec, col_vec):
	"""
		Checks if the requested move is valid for the bishop
	"""
	# Define default return
	vec = [True]

	collision = None
	# Checks the diagonal if the move is valid
	if row_vec == col_vec:
		row1 = min(cords[0], cords[2]) + 1
		col1 = min(cords[1], cords[3]) + 1
		row2 = max(cords[0], cords[2])
		while row1 < row2:
			if board.map[row1][col1].get_symbol() != " ":
				collision = "yes"
			row1 += 1
			col1 += 1
	# Checks the other diagonal if the move is valid
	elif row_vec*-1 == col_vec:
		row1 = min(cords[0], cords[2]) + 1
		col1 = max(cords[1], cords[3]) - 1
		row2 = max(cords[0], cords[2])
		while row1 < row2:
			if board.map[row1][col1].get_symbol() != " ":
				collision = "yes"
			row1 += 1
			col1 -= 1
	else:
		vec = [False, "This is not a valid move for a Bishop!"]
		return vec

	# If collisions occured, move is bad!
	if collision == "yes":
		vec = [False, "The bishop cannot pass through pieces!"]

	return vec

def is_valid_rook_move(board, cords, row_vec, col_vec):
	"""
		Checks if the requested move is valid for the rook
	"""
	# Define default return
	vec = [True]

	collision = None
	# Checks the row if the move is valid
	if row_vec == 0:
		start = min(cords[1], cords[3]) + 1
		end = max(cords[1], cords[3])
		while start < end:
			if board.map[cords[0]][start].get_symbol() != " ":
				collision = "yes"
			start += 1
	# Checks the column if the move is valid
	elif col_vec == 0:
		start = min(cords[0], cords[2]) + 1
		end = max(cords[0], cords[2])
		while start < end:
			if board.map[start][cords[1]].get_symbol() != " ":
				collision = "yes"
			start += 1
	else:
		vec = [False, "This is not a valid move for a Rook!"]
		return vec

	# If no collisions, move is good!
	if collision == "yes":
		vec = [False, "The rook cannot pass through pieces!"]

	return vec

def is_attacking_own_piece(board, cords):
	"""
		Checks if the player is attempting to attack their own piece
		Returns True 
	"""
	atk_piece_color = board.map[cords[0]][cords[1]].get_color()
	def_piece_color = board.map[cords[2]][cords[3]].get_color()
	if atk_piece_color == " " or def_piece_color == " ":
		return False
	elif atk_piece_color is def_piece_color:
		return True
	else:
		return False

def is_own_piece(board, cords, player):
	"""
		Ensures the player is moving their own piece.
		Returns True if acceptable move
	"""
	#  If player is attacking self, return true
	if board.map[cords[0]][cords[1]].get_color() == player:
		return True
	else:
		return False

