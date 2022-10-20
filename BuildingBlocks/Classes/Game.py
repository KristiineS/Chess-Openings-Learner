import numpy as np


class Game:
    def __init__(self, player_color_name: str):
        # track board states, moves, captures and matrices
        self.board_states = np.empty(5899, dtype=np)
        self.white_moves = []
        self.black_moves = []
        self.move_number = 0
        # track player color and whose move it is
        self.player_color_name = player_color_name
        self.player = True if player_color_name == "white" else False  # True: white, False: black
        self.whose_turn = True  # True: white's turn, False: black's turn
        # track pawn promotions in progress, moves in progress and co-ordinates of the last move
        self.pawn_promotion = None  # Square
        self.move_piece = None  # Piece
        self.last_move = np.empty(0)   # Array of co-ordinates
        # sets of squares that are currently under attack by the enemy pieces
        self.fire_by_white_pieces = set()
        self.fire_by_black_pieces = set()
        self.white_in_check = False
        self.black_in_check = False

    def check_if_check(self, board):
        if self.whose_turn:  # white's turn
            self.fire_by_white_pieces = find_squares_under_attack(board, "white")
            self.black_in_check = True if find_king(board, "black") in self.fire_by_white_pieces else False
        else:  # black's turn
            self.fire_by_black_pieces = find_squares_under_attack(board, "black")
            self.white_in_check = True if find_king(board, "white") in self.fire_by_black_pieces else False


def find_squares_under_attack_by_pawn_capture(piece):
    possible_captures = []
    if piece.color == "white":
        if piece.x < 7:
            possible_captures.append((piece.x + 1, piece.y + 1))
        if piece.x > 0:
            possible_captures.append((piece.x - 1, piece.y + 1))
    else:  # black
        if piece.x < 7:
            possible_captures.append((piece.x + 1, piece.y - 1))
        if piece.x > 0:
            possible_captures.append((piece.x - 1, piece.y - 1))
    return possible_captures


def find_squares_under_attack(board, color):
    squares_under_attack = []
    for i in range(8):
        for j in range(8):
            if board[i][j].piece:
                if board[i][j].piece.color == color:
                    squares_under_attack += board[i][j].piece.possible_captures(board)
                    if board[i][j].piece.name == "Pawn":
                        squares_under_attack += find_squares_under_attack_by_pawn_capture(board[i][j].piece)
                    else:
                        squares_under_attack += board[i][j].piece.possible_moves(board)
    return set(squares_under_attack)


def find_king(board, color):
    for i in range(8):
        for j in range(8):
            if board[i][j].piece:
                if board[i][j].piece.name == "King" and board[i][j].piece.color == color:
                    return (i, j)

