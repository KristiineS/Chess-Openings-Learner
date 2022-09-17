import numpy as np


class Game:
    def __init__(self, player_color: bool):
        # track board states, moves and captures
        self.board_states = np.empty(5899, dtype=np)
        self.white_moves = []
        self.black_moves = []
        self.move_number = 0
        # track player color and whose move it is
        self.player_color = player_color  # True: white, False: black
        self.whose_turn = player_color  # True: white's turn, False: black's turn
        # track pawn promotions in progress, moves in progress and co-ordinates of the last move
        self.pawn_promotion = None  # Square
        self.move_piece = None  # Piece
        self.last_move = np.empty(0)   # Array of co-ordinates