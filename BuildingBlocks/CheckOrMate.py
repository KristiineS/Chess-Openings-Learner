def find_squares_under_attack_by_pawn_capture(piece, board):
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


def check_if_check(board, game):
    squares_under_attack = []
    for i in range(8):
        for j in range(8):
            if board[i][j].piece:
                if board[i][j].piece.color == "white" and not game.whose_turn or board[i][j].piece.color == "black" and game.whose_turn:
                    squares_under_attack += board[i][j].piece.possible_captures(board)
                    if board[i][j].piece.name == "Pawn":
                        squares_under_attack += find_squares_under_attack_by_pawn_capture(board[i][j].piece, board)
                    else:
                        squares_under_attack += board[i][j].piece.possible_moves(board)
    return set(squares_under_attack)


def find_king(board, player_color):
    for i in range(8):
        for j in range(8):
            if board[i][j].piece:
                if board[i][j].piece.name == "King" and board[i][j].piece.color == player_color:
                    print((i,j))
                    return (i, j)