"""
board.py - Defines and prints the board of a text-based chess game
			Moves pieces on the board and intakes coordinates.

By: Runaal Parmar
Dec 9, 2018
"""
import sys
import checks
import validate_move
from piece import Piece
from termcolor import colored
from copy import deepcopy

white_color = "blue"
black_color = "red"
board_color = "cyan"
label_color = "white"

class Board:
	"""
		Maps, prints and moves for all pieces on the board
	"""
	def __init__(self):
		"""
			Initialize board for the beginning of play
		"""
		# create null piece object
		null_piece = Piece(" ", " ", " ")

		# Create board, initialized to null pieces
		self.map = [[deepcopy(null_piece) for i in range(8)] for i in range(8)]

		# Initialize pawns for both sides
		for i in range(8):
			self.map[1][i] = Piece("pawn", "black", "\u265f")
			self.map[6][i] = Piece("pawn", "white", "\u2659")

		# Initialize major pieces for black side 
		self.map[0][0] = Piece("rook",   "black", "\u265c")
		self.map[0][1] = Piece("knight", "black", "\u265e")
		self.map[0][2] = Piece("bishop", "black", "\u265d")
		self.map[0][3] = Piece("queen",  "black", "\u265b")
		self.map[0][4] = Piece("king",   "black", "\u265a")
		self.map[0][5] = Piece("bishop", "black", "\u265d")
		self.map[0][6] = Piece("knight", "black", "\u265e")
		self.map[0][7] = Piece("rook",   "black", "\u265c")

		# Initialize major pieces for white side 
		self.map[7][0] = Piece("rook",   "white", "\u2656")
		self.map[7][1] = Piece("knight", "white", "\u2658")
		self.map[7][2] = Piece("bishop", "white", "\u2657")
		self.map[7][3] = Piece("queen",  "white", "\u2655")
		self.map[7][4] = Piece("king",   "white", "\u2654")
		self.map[7][5] = Piece("bishop", "white", "\u2657")
		self.map[7][6] = Piece("knight", "white", "\u2658")
		self.map[7][7] = Piece("rook",   "white", "\u2656")

	def map_print(self):
		"""
			Prints the current state of the entire board
		"""
		# Print top border of the chess board
		print(colored("\n ==", board_color), end="")
		for i in range(8):
			print(colored(chr(65+i), label_color), end="")
			print(colored("=", board_color), end="")
		print(colored("==", board_color))

		# Print the board side and the labels
		i = 8
		row = 0
		for rank in self.map:
			print(" " + str(i) + colored("|", board_color), end="")
			col = 0

			# Print the pieces on the board
			for square in rank:
				tile = (row + col)%2
				if square.get_symbol() is " " and tile == 0:
					print("\033[47;33m  \033[m", end="")
				elif square.get_symbol() is " " and tile == 1:
					print("\033[40;33m  \033[m", end="")
				elif square.get_color() == "white" and tile == 0:
					print(colored("\033[47;31m{} \033[m".format(square.get_symbol()), black_color), end="")
				elif square.get_color() == "white" and tile == 1:
					print(colored("\033[40;31m{} \033[m".format(square.get_symbol()), black_color), end="")
				elif square.get_color() == "black" and tile == 0:
					print(colored("\033[47;34m{} \033[m".format(square.get_symbol()), white_color), end="")
				elif square.get_color() == "black" and tile == 1:
					print(colored("\033[40;34m{} \033[m".format(square.get_symbol()), white_color), end="")
				else:
					print("Serious error printing the board")

				col += 1
			# Print the pieces on the board
			row += 1
			print(colored("|", board_color) + str(i))
			i -= 1

		# Print the bottom border and labels
		print(colored(" ==", board_color), end="")
		for i in range(8):
			print(colored(chr(65+i), label_color), end="")
			print(colored("=", board_color), end="")
		print(colored("==\n", board_color))
			
	def clean_intake(self, player): # readline
		"""
			Takes raw input from the user and parses it.
			Ensures proper formatting, and general sanitization
			Returns array with start index 1 & 2 and end index 1 & 2
		"""
		while True:
			try:
				print(player + " move.")
				intake = input("Enter start and end co-ordinates: ")
			except Exception as err: 
				print(colored("Encountered issues:" + err, "red"))
				raise 

			# special entries require seperate actions
			if intake == "undo" or intake == "exit" or intake == "quit":
				return intake

			if len(intake) != 5:
				print(colored("Please enter a valid co-ordinate pair", "red"))
			elif intake[0] not in "abcdefghABCDEFGH":
				print(colored("Please enter a valid co-ordinate pair", "red"))
			elif intake[3] not in "abcdefghABCDEFGH":
				print(colored("Please enter a valid co-ordinate pair", "red"))
			elif intake[1] not in "12345678":
				print(colored("Please enter a valid co-ordinate pair", "red"))
			elif intake[4] not in "12345678":
				print(colored("Please enter a valid co-ordinate pair", "red"))
			else:
				start1 = 8 - int(intake[1])
				start2 = int(ord(intake[0].lower())-97)
				end1 = 8 - int(intake[4])
				end2 = int(ord(intake[3].lower())-97)
				cords = [start1, start2, end1, end2]
				return cords

	def move(self, cords, player):
		"""
			Moves pieces. Calls check valid to ensure legal moves.
		"""
		# Define default return to be overwritten:
		vec = [True, "default message"]

		# Ensure input/output coordinates are in the array bounds
		if cords[0] > 7 or cords[1] > 7 or cords[0] < 0 or cords[1] < 0:
			return False

		# Ensure the player is moving their own pieces
		if not(validate_move.is_own_piece(self, cords, player)):
			vec = [False, "Not your turn! Move only your own pieces"]

		# Ensure the destination piece is not a friendly piece
		if validate_move.is_attacking_own_piece(self, cords):
			vec = [False, "Cannot attack your own piece!"]

		# Ensure a piece is being selected for the starting square
		if self.map[cords[0]][cords[1]].get_symbol == " ":
			vec = [False, "There is no piece on the starting square!"]

		# return an error message is something is wrong
		if not(vec[0]):
			return vec

		# Calculate the vectors of the movement for future use
		type_of_piece = self.map[cords[0]][cords[1]].get_type()
		row_vec = cords[2] - cords[0]
		col_vec = cords[3] - cords[1]

		# Validate the move for a rook
		if type_of_piece == "rook":
			vec = validate_move.is_valid_rook_move(self, cords, row_vec, col_vec)

		# Validate the move for a bishop
		elif type_of_piece == "bishop":
			vec = validate_move.is_valid_bishop_move(self, cords, row_vec, col_vec)

		# Validate the move for a queen
		elif type_of_piece == "queen":
			vec = validate_move.is_valid_queen_move(self, cords, row_vec, col_vec)

		# Validate the move for a knight
		elif type_of_piece == "knight":
			vec = validate_move.is_valid_knight_move(self, row_vec, col_vec)

		# Validate the move for a king
		elif type_of_piece == "king":
			vec = validate_move.is_valid_king_move(self, row_vec, col_vec)

		# return an error message is something is wrong
		if not(vec[0]):
			return vec

		# Create duplicate board
		test_board = deepcopy(self)

		# Make the desired move on duplicate board
		test_board.map[cords[2]][cords[3]] = test_board.map[cords[0]][cords[1]]
		test_board.map[cords[0]][cords[1]] = Piece(" ", " ", " ")

		# Ensure the move does not leave the king in check
		threat = checks.is_king_in_check(test_board, player)
		if threat:
			vec = [False, "Cannot leave your king in check!"]

		# Validate the move for a pawn
		elif type_of_piece == "pawn":
			vec = validate_move.is_valid_pawn_move(self, cords, player, row_vec, col_vec)

		# return an error message is something is wrong
		if vec[0]:
			self.map[cords[2]][cords[3]] = self.map[cords[0]][cords[1]]
			self.map[cords[0]][cords[1]] = Piece(" ", " ", " ")

		return vec
