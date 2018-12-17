"""
piece.py - Defines the pieces for a text-based chess game

By: Runaal Parmar
Dec 9, 2018
"""

valid_promote = {
    "bishop", "knight", "rook", "queen"
}

class Piece:
	"""
		Standard piece definition
	"""
	def __init__(self, piece_type, color, symbol):
		"""
			Piece constructor
		"""
		self.piece_type = piece_type
		self.color = color # Black = False, White = True
		self.symbol = symbol

	def get_symbol(self):
		"""
			Get alphabetic symbol of piece
		"""
		return self.symbol

	def get_color(self):
		"""
			Get color of piece
		"""
		return self.color

	def get_type(self):
		"""
			Get type of piece
		"""
		return self.piece_type

	def set_type(self, req_type):
		"""
			Set type of piece
		"""
		self.piece_type = req_type

	def set_symbol(self, new_symbol):
		"""
			Sets new symbol for the piece
		"""
		self.symbol = new_symbol

	def promote(self, cords, player):
		"""
			Promotes a pawn
		"""
		while (self.get_type() == "pawn"):
			req_type = input("What do you want to promote your pawn to?: ")
			req_type = req_type.lower()

			if (req_type not in valid_promote):
				print("Invalid Input")
			else:
				self.set_type(req_type)
				if self.get_color() == "white":
					if req_type == "queen":
						self.set_symbol("\u2655")
					elif req_type == "rook":
						self.set_symbol("\u2656")
					elif req_type == "bishop":
						self.set_symbol("\u2657")
					elif req_type == "knight":
						self.set_symbol("\u2658")
				else:
					if req_type == "queen":
						self.set_symbol("\u265b")
					elif req_type == "rook":
						self.set_symbol("\u265c")
					elif req_type == "bishop":
						self.set_symbol("\u265d")
					elif req_type == "knight":
						self.set_symbol("\u265e")
