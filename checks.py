"""
checks.py - Defines the checks which prevent non-valid moves in chess

By: Runaal Parmar 
Dec 13, 2018
"""
from copy import deepcopy
from termcolor import colored

k_m = [
	(1,2),(2,1),(-1,2),(-2,1),(1,-2),(2,-1),(-1,-2),(-2,-1)
]

def is_valid_pawn_move(board, cords, player, row_vec, col_vec):
	"""
		Checks if the requested move is valid for a pawn
	"""
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
		if board.map[cords[2]][cords[3]] == " ":
			if cords[2] == 7 or cords[2] == 0:
				board.map[cords[0]][cords[1]].promote(cords)
			return True
		else:
			print(colored("Pawn cannot walk into opposing piece!", "red"))
			return False

	# Either color attacking with the pawn
	elif white_attacking or black_attacking:
		if board.map[cords[2]][cords[3]] == " ":
			print(colored("No pieces for the pawn to attack!", "red"))
			return False
		elif board.map[cords[2]][cords[3]].get_color() != board.map[cords[0]][cords[1]].get_color():
			if cords[2] == 7 or cords[2] == 0:
				board.map[cords[0]][cords[1]].promote(cords)
			return True
		else:
			print(colored("Pawn only moves diagonally while attacking!", "red"))
			return False

	# Invalid move for the pawn
	else:
		print(colored("This is not a valid move for a pawn!", "red"))
		return False

def is_valid_king_move(board, row_vec, col_vec):
	"""
		Checks if the requested move is valid for the king
	"""
	if abs(row_vec) > 1 or abs(col_vec) > 1:
		return False
	else:
		return True

def is_valid_knight_move(board, row_vec, col_vec):
	"""
		Checks if the requested move is valid for the knight
	"""
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
	if row_vec == col_vec:
		row1 = min(cords[0], cords[2]) + 1
		col1 = min(cords[1], cords[3]) + 1
		row2 = max(cords[0], cords[2])
		while row1 < row2:
			if board.map[row1][col1] != " ":
				collision = "yes"
			row1 += 1
			col1 += 1
	elif row_vec*-1 == col_vec:
		row1 = min(cords[0], cords[2]) + 1
		col1 = max(cords[1], cords[3]) - 1
		row2 = max(cords[0], cords[2])
		while row1 < row2:
			if board.map[row1][col1] != " ":
				collision = "yes"
			row1 += 1
			col1 -= 1
	elif row_vec == 0:
		start = min(cords[1], cords[3]) + 1
		end = max(cords[1], cords[3])
		while start < end:
			if board.map[cords[0]][start] != " ":
				collision = "yes"
			start += 1
	elif col_vec == 0:
		start = min(cords[0], cords[2]) + 1
		end = max(cords[0], cords[2])
		while start < end:
			if board.map[start][cords[1]] != " ":
				collision = "yes"
			start += 1
	else:
		print(colored("This is not a valid move for a Queen!", "red"))
		return False

	if collision != "yes":
		return True

	print(colored("The Queen cannot pass through pieces!", "red"))
	return False

def is_valid_bishop_move(board, cords, row_vec, col_vec):
	"""
		Checks if the requested move is valid for the bishop
	"""
	collision = None
	if row_vec == col_vec:
		row1 = min(cords[0], cords[2]) + 1
		col1 = min(cords[1], cords[3]) + 1
		row2 = max(cords[0], cords[2])
		while row1 < row2:
			if board.map[row1][col1] != " ":
				collision = "yes"
			row1 += 1
			col1 += 1
	elif row_vec*-1 == col_vec:
		row1 = min(cords[0], cords[2]) + 1
		col1 = max(cords[1], cords[3]) - 1
		row2 = max(cords[0], cords[2])
		while row1 < row2:
			if board.map[row1][col1] != " ":
				collision = "yes"
			row1 += 1
			col1 -= 1
	else:
		print(colored("This is not a valid move for a Bishop!", "red"))
		return False

	if collision != "yes":
		return True

	print(colored("The bishop cannot pass through pieces!", "red"))
	return False

def is_valid_rook_move(board, cords, row_vec, col_vec):
	"""
		Checks if the requested move is valid for the rook
	"""
	collision = None
	if row_vec == 0:
		start = min(cords[1], cords[3]) + 1
		end = max(cords[1], cords[3])
		while start < end:
			if board.map[cords[0]][start] != " ":
				collision = "yes"
			start += 1
	elif col_vec == 0:
		start = min(cords[0], cords[2]) + 1
		end = max(cords[0], cords[2])
		while start < end:
			if board.map[start][cords[1]] != " ":
				collision = "yes"
			start += 1
	else:
		print(colored("This is not a valid move for a Rook!", "red"))
		return False

	if collision != "yes":
		return True

	print(colored("The rook cannot pass through pieces!", "red"))
	return False

def is_attacking_own_piece(board, cords):
	"""
		Checks if the player is attempting to attack their own piece
		Returns True 
	"""
	if board.map[cords[2]][cords[3]] is " ":
		return False
	else:
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
	if board.map[cords[0]][cords[1]].get_color() and player is "white":
		return True
	elif not(board.map[cords[0]][cords[1]].get_color()) and player is "black":
		return True
	else:
		return False

def find_king(board):
	k_cords = [9, 9, 9, 9]
	for row in range(8):
		for col in range(8):
			if board.map[row][col] != " ":
				if board.map[row][col].get_type() == "king":
					if board.map[row][col].color:
						k_cords[0] = row
						k_cords[1] = col
					if not(board.map[row][col].get_color()):
						k_cords[2] = row
						k_cords[3] = col
	return k_cords

def puts_king_in_check(board, cords, player):
	"""
		Ensures the player does not place their own king in check.
	"""
	test_board = deepcopy(board)

	test_board.map[cords[0]][cords[1]].set_loc(str(cords[2]) + str(cords[3]))
	test_board.map[cords[2]][cords[3]] = test_board.map[cords[0]][cords[1]]
	test_board.map[cords[0]][cords[1]] = " "

	k_cords = find_king(test_board)

	if player == "white":
		pk_cords = [k_cords[0], k_cords[1]]
		player = True
	else:
		pk_cords = [k_cords[2], k_cords[3]]
		player = False

	for move in k_m:
		row = pk_cords[0] + move[0]
		col = pk_cords[1] + move[1]
		if row < 8 and row >= 0 and col < 8 and col >= 0:
			if test_board.map[row][col] != " ":
				if test_board.map[row][col].get_type() == "knight":
					print(str(test_board.map[row][col].get_color()) + str(player))
					if (test_board.map[row][col].get_color() != player):
						print(colored("In check from the Knight!", "red"))
						return True

	if player:
		if test_board.map[pk_cords[0]-1][pk_cords[1]+1] != " ":
			if test_board.map[pk_cords[0]-1][pk_cords[1]+1].get_type == "pawn":
				if not(test_board.map[pk_cords[0]-1][pk_cords[1]+1].get_color):
					print(colored("In check from the Pawn!", "red"))
					return True
		if test_board.map[pk_cords[0]-1][pk_cords[1]-1] != " ":
			if test_board.map[pk_cords[0]-1][pk_cords[1]-1].get_type == "pawn":
				if not(test_board.map[pk_cords[0]-1][pk_cords[1]-1].get_color):
					print(colored("In check from the Pawn!", "red"))
					return True
	else:
		if test_board.map[pk_cords[0]+1][pk_cords[1]+1] != " ":
			if test_board.map[pk_cords[0]+1][pk_cords[1]+1].get_type == "pawn":
				if test_board.map[pk_cords[0]+1][pk_cords[1]+1].get_color:
					print(colored("In check from the Pawn!", "red"))
					return True
		if test_board.map[pk_cords[0]+1][pk_cords[1]-1] != " ":
			if test_board.map[pk_cords[0]+1][pk_cords[1]-1].get_type == "pawn":
				if test_board.map[pk_cords[0]+1][pk_cords[1]-1].get_color:
					print(colored("In check from the Pawn!", "red"))
					return True
	print("king not in check")
	return False 

