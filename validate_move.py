"""
move_validation.py - Defines the checks which prevent non-valid moves in chess

By: Runaal Parmar 
Dec 17, 2018
"""
from copy import deepcopy
from termcolor import colored
from piece import Piece

def is_valid_pawn_move(board, cords, player, row_vec, col_vec):
	"""
		Checks if the requested move is valid for a pawn
	"""
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
		if cords[0] == 1 or cords[0] == 6:
			return True
		else:
			print(colored("Pawn can only move 2 spaces on its first move!", "red"))
			return False

	# Either color moving the pawn 1 step
	elif white_move or black_move:
		if board.map[cords[2]][cords[3]].get_symbol() == " ":
			if cords[2] == 7 or cords[2] == 0:
				board.map[cords[0]][cords[1]].promote(cords)
			return True
		else:
			print(colored("Pawn cannot walk into opposing piece!", "red"))
			return False

	# Either color attacking with the pawn
	elif white_attacking or black_attacking:
		if board.map[cords[2]][cords[3]].get_symbol() == " ":
			print(colored("No pieces for the pawn to attack!", "red"))
			return False
		elif board.map[cords[2]][cords[3]].get_color() != player:
			if cords[2] == 7 or cords[2] == 0:
				board.map[cords[0]][cords[1]].promote(cords)
			return True

	# Invalid move for the pawn
	else:
		print(colored("This is not a valid move for a pawn!", "red"))
		return False

def is_valid_king_move(board, row_vec, col_vec):
	"""
		Checks if the requested move is valid for the king
	"""
	# The King can move one step in any direction
	if abs(row_vec) > 1 or abs(col_vec) > 1:
		return False
	else:
		return True

def is_valid_knight_move(board, row_vec, col_vec):
	"""
		Checks if the requested move is valid for the knight
	"""
	# Checks all 8 moves for the knight
	if abs(row_vec) == 2:
		if abs(col_vec) == 1:
			return True
	elif abs(row_vec) == 1:
		if abs(col_vec) == 2:
			return True
	print(colored("This is not a valid move for a Knight!", "red"))
	return False

def is_valid_queen_move(board, cords, row_vec, col_vec):
	"""
		Checks if the requested move is valid for the queen
	"""
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
		print(colored("This is not a valid move for a Queen!", "red"))
		return False

	# If no collisions occured, move is good!
	if collision != "yes":
		return True
	else:
		print(colored("The Queen cannot pass through pieces!", "red"))
		return False

def is_valid_bishop_move(board, cords, row_vec, col_vec):
	"""
		Checks if the requested move is valid for the bishop
	"""
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
		print(colored("This is not a valid move for a Bishop!", "red"))
		return False

	# If no collisions, move is good!
	if collision != "yes":
		return True
	else:
		print(colored("The bishop cannot pass through pieces!", "red"))
		return False

def is_valid_rook_move(board, cords, row_vec, col_vec):
	"""
		Checks if the requested move is valid for the rook
	"""
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
		print(colored("This is not a valid move for a Rook!", "red"))
		return False

	# If no collisions, move is good!
	if collision != "yes":
		return True
	else:
		print(colored("The rook cannot pass through pieces!", "red"))
		return False

def is_attacking_own_piece(board, cords):
	"""
		Checks if the player is attempting to attack their own piece
		Returns True 
	"""
	atk_piece_color = board.map[cords[0]][cords[1]].get_color()
	def_piece_color = board.map[cords[2]][cords[3]].get_color()
	if atk_piece_color is def_piece_color:
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
