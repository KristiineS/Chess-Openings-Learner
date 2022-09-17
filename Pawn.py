class Pawn:
    def __init__(self, x: int, y: int, color: str):
        self.x = x
        self.y = y
        self.color = color
        self.name = "Pawn"

    def possible_moves(self, board):
        possible_new_squares = []
        if self.color == "white" and board[self.x][self.y + 1].piece is None:
            # starting with 2 steps
            if self.y == 1 and board[self.x][self.y + 2].piece is None:
                possible_new_squares.append((self.x, self.y + 2))
            # 1 step forward
            if self.y < 6:
                possible_new_squares.append((self.x, self.y + 1))
        if self.color == "black" and board[self.x][self.y - 1].piece is None:
            # black starting with 2 steps
            if self.y == 6 and board[self.x][self.y - 2].piece is None:
                possible_new_squares.append((self.x, self.y - 2))
            # 1 step forward
            if self.y > 1:
                possible_new_squares.append((self.x, self.y - 1))

        return possible_new_squares

    def possible_captures(self, board):
        possible_captures = []

        # regular capturing
        if self.color == "white":
            if self.y < 6:
                if self.x < 7:
                    if board[self.x + 1][self.y + 1].piece and board[self.x + 1][self.y + 1].piece.color != self.color:
                        possible_captures.append((self.x + 1, self.y + 1))
                if self.x > 0:
                    if board[self.x - 1][self.y + 1].piece and board[self.x - 1][self.y + 1].piece.color != self.color:
                        possible_captures.append((self.x - 1, self.y + 1))
        if self.color == "black":
            if self.y > 1:
                if self.x < 7:
                    if board[self.x + 1][self.y - 1].piece and board[self.x + 1][self.y - 1].piece.color != self.color:
                        possible_captures.append((self.x + 1, self.y - 1))
                if self.x > 0:
                    if board[self.x - 1][self.y - 1].piece and board[self.x - 1][self.y - 1].piece.color != self.color:
                        possible_captures.append((self.x - 1, self.y - 1))

        return possible_captures
