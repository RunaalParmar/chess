"""
board.py - Defines and prints the board of a text-based chess game
			Moves pieces on the board and intakes coordinates.

By: Runaal Parmar
Dec 9, 2018
"""
import sys
from piece import Piece
import checks
from termcolor import colored

white_color = "blue"
black_color = "red"
board_color = "cyan"
label_color = "white"

class Board:
	"""
		Maps, prints and determines the legal moves for all 
		pieces on the board
	"""
	def __init__(self):
		"""
			Initialize board for the beginning of play
		"""
		# Create board, initialized to blank spaces
		self.map = [[" " for i in range(8)] for i in range(8)]

		# Initialize pawns for both sides
		for i in range(8):
			self.map[1][i] = Piece("pawn", False, "\u265f", "1" + str(i))
			self.map[6][i] = Piece("pawn", True, "\u2659", "6" + str(i))

		# Initialize major pieces for black side 
		self.map[0][0] = Piece("rook",   False, "\u265c", "00")
		self.map[0][1] = Piece("knight", False, "\u265e", "01")
		self.map[0][2] = Piece("bishop", False, "\u265d", "02")
		self.map[0][3] = Piece("queen",  False, "\u265b", "03")
		self.map[0][4] = Piece("king",   False, "\u265a", "04")
		self.map[0][5] = Piece("bishop", False, "\u265d", "05")
		self.map[0][6] = Piece("knight", False, "\u265e", "06")
		self.map[0][7] = Piece("rook",   False, "\u265c", "07")

		# Initialize major pieces for white side 
		self.map[7][0] = Piece("rook",   True, "\u2656", "70")
		self.map[7][1] = Piece("knight", True, "\u2658", "71")
		self.map[7][2] = Piece("bishop", True, "\u2657", "72")
		self.map[7][3] = Piece("queen",  True, "\u2655", "73")
		self.map[7][4] = Piece("king",   True, "\u2654", "74")
		self.map[7][5] = Piece("bishop", True, "\u2657", "75")
		self.map[7][6] = Piece("knight", True, "\u2658", "76")
		self.map[7][7] = Piece("rook",   True, "\u2656", "77")

	def map_print(self):
		"""
			Prints the current state of the entire board
		"""
		print(colored("\n ==", board_color), end="")
		for i in range(8):
			print(colored(chr(65+i), label_color), end="")
			print(colored("=", board_color), end="")
		print(colored("==", board_color))

		i = 8
		row = 0
		for rank in self.map:
			print(" " + str(i) + colored("|", board_color), end="")
			col = 0

			for square in rank:
				tile = (row + col)%2
				if square is " " and tile == 0:
					print("\033[47;33m  \033[m", end="")
				elif square is " " and tile == 1:
					print("\033[40;33m  \033[m", end="")
				elif square.get_color() and tile == 0:
					print(colored("\033[47;31m{} \033[m".format(square.get_symbol()), black_color), end="")
				elif square.get_color() and tile == 1:
					print(colored("\033[40;31m{} \033[m".format(square.get_symbol()), black_color), end="")
				elif not square.get_color() and tile == 0:
					print(colored("\033[47;31m{} \033[m".format(square.get_symbol()), white_color), end="")
				elif not square.get_color() and tile == 1:
					print(colored("\033[40;31m{} \033[m".format(square.get_symbol()), white_color), end="")
				else:
					print("Serious error")

				col += 1
			row += 1
			print(colored("|", board_color) + str(i))
			i -= 1

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
		# collisions, valid for type, checks, etc

		if self.map[cords[0]][cords[1]] == " ":
			print(colored("There is no piece on the starting square!", "red"))
			return False

		if not(checks.is_own_piece(self, cords, player)):
			print(colored("Not your turn! Move only your own pieces", "red"))
			return False

		if checks.is_attacking_own_piece(self, cords):
			print(colored("Cannot attack your own piece!", "red"))
			return False

		type_of_piece = self.map[cords[0]][cords[1]].get_type()
		row_vec = cords[2] - cords[0]
		col_vec = cords[3] - cords[1]

		if type_of_piece == "rook":
			if not checks.is_valid_rook_move(self, cords, row_vec, col_vec):
				return False

		elif type_of_piece == "bishop":
			if not checks.is_valid_bishop_move(self, cords, row_vec, col_vec):
				return False

		elif type_of_piece == "queen":
			if not checks.is_valid_queen_move(self, cords, row_vec, col_vec):
				return False

		elif type_of_piece == "knight":
			if not checks.is_valid_knight_move(self, row_vec, col_vec):
				return False

		elif type_of_piece == "king":
			if not checks.is_valid_king_move(self, row_vec, col_vec):
				print(colored("This is not a valid move for a King!", "red"))
				return False

		elif type_of_piece == "pawn":
			if not checks.is_valid_pawn_move(self, cords, player, row_vec, col_vec):
				return False

		if checks.puts_king_in_check(self, cords, player):
			print(colored("Cannot put your king into check!", "red"))
			return False

		self.map[cords[0]][cords[1]].set_loc(str(cords[2]) + str(cords[3]))
		self.map[cords[2]][cords[3]] = self.map[cords[0]][cords[1]]
		self.map[cords[0]][cords[1]] = " "
		return True

