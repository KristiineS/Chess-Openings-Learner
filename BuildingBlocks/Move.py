from copy import deepcopy

from BuildingBlocks.Pieces.Bishop import Bishop
from BuildingBlocks.Pieces.Knight import Knight
from BuildingBlocks.Pieces.Queen import Queen
from BuildingBlocks.Pieces.Rook import Rook


# castle the king
def castle_king(board, movement, game):
    # movement - (king new, king old, rook new, rook old)
    for (new, old) in [(movement[0], movement[1]), (movement[2], movement[3])]:
        # deepcopy the piece
        board[new[0]][new[1]].piece = deepcopy(board[old[0]][old[1]].piece)
        # set new co-ordinates
        board[new[0]][new[1]].piece.x = new[0]
        board[new[0]][new[1]].piece.y = new[1]
        # update movement status
        board[new[0]][new[1]].piece.has_not_moved = False
        board[old[0]][old[1]].piece = None

    # highlight the squares the pieces moved from and to
    game.last_move = [(movement[0][0], movement[0][1]), (movement[1][0], movement[1][1])]
    game.check_if_check(board)

    if game.move_piece.color == "white":
        if abs(movement[2][0]-movement[3][0]) == 3:
            game.white_moves.append('O-O-O')
        else:
            game.white_moves.append('O-O')
        if game.black_in_check:
            game.white_moves[-1] += "#"
    else:
        if abs(movement[2][0]-movement[3][0]) == 3:
            game.black_moves.append('O-O-O')
        else:
            game.black_moves.append('O-O')
        if game.white_in_check:
            game.black_moves[-1] += "#"

    game.board_states[game.move_number] = deepcopy(board)
    game.move_number += 1
    game.whose_turn = not game.whose_turn


# move or capture a piece
def update_board(board, selected_square, game):
    # For optimization
    selected_square_x = selected_square.x
    selected_square_y = selected_square.y
    move_piece_x = game.move_piece.x
    move_piece_y = game.move_piece.y
    game.check_if_check(board)
    # add moves to the "made moves" list with game notation
    if game.move_piece.color == "white":
        if board[selected_square_x][selected_square_y].piece:
            if game.move_piece.name == "Pawn":
                game.white_moves.append(''.join([board[game.move_piece.x][game.move_piece.y].letter,
                              'x', selected_square.letter, selected_square.number]))
            else:
                game.white_moves.append(''.join([game.move_piece.abbreviation, 'x', selected_square.letter, selected_square.number]))
        else:
            game.white_moves.append(''.join([game.move_piece.abbreviation, selected_square.letter, selected_square.number]))
        if game.black_in_check:
            game.white_moves[-1] += "#"
    else:
        if board[selected_square_x][selected_square_y].piece:
            if game.move_piece.name == "Pawn":
                game.black_moves.append(''.join([board[game.move_piece.x][game.move_piece.y].letter,
                                                 'x', selected_square.letter, selected_square.number]))
            else:
                game.black_moves.append(''.join([game.move_piece.abbreviation, 'x', selected_square.letter, selected_square.number]))
        else:
            game.black_moves.append(''.join([game.move_piece.abbreviation, selected_square.letter, selected_square.number]))
        if game.white_in_check:
            game.black_moves[-1] += "#"
    # deepcopy the piece
    board[selected_square_x][selected_square_y].piece = deepcopy(board[move_piece_x][move_piece_y].piece)
    # set new co-ordinates
    board[selected_square_x][selected_square_y].piece.x = selected_square_x
    board[selected_square_x][selected_square_y].piece.y = selected_square_y
    # update movement status for king and rook and the game
    if board[move_piece_x][move_piece_y].piece.name == "King" \
            or board[move_piece_x][move_piece_y].piece.name == "Rook":
        board[selected_square_x][selected_square_y].piece.has_not_moved = False
    board[move_piece_x][move_piece_y].piece = None
    game.board_states[game.move_number] = deepcopy(board)
    game.move_number += 1
    game.whose_turn = not game.whose_turn
    # highlight the squares the pieces moved to and from
    game.last_move = [(selected_square_x, selected_square_y), (move_piece_x, move_piece_y)]


# initialize a pawn promotion with capture or without capture
def promote(board, selected_square_x, selected_square_y, game):
    # save the square of the pawn to be moved and the destination square
    game.pawn_promotion = [deepcopy(board[game.move_piece.x][game.move_piece.y]),
                           deepcopy(board[selected_square_x][selected_square_y])]
    board[selected_square_x][selected_square_y].promotions = game.move_piece.color
    # delete the old piece (if there) and the promoted pawn
    board[selected_square_x][selected_square_y].piece = None
    board[game.move_piece.x][game.move_piece.y].piece = None


# click on the piece to be chosen for promotion
def select_promotion(square, x, y, color, tile_size, board, game):
    game.check_if_check(board)
    if square.x_coordinate <= x <= (square.x_coordinate + tile_size / 2):
        # Promote to a knight
        if square.y_coordinate <= y <= (square.y_coordinate + tile_size / 2):
            square.piece = Knight(square.x, square.y, color)
            if color == "white":
                game.white_moves.append(''.join([square.letter, square.number, '=K']))
                if game.black_in_check:
                    game.white_moves[-1] += "#"
            else:
                game.black_moves.append(''.join([square.letter, square.number, '=K']))
                if game.white_in_check:
                    game.black_moves[-1] += "#"
        # Promote to a rook
        else:
            square.piece = Rook(square.x, square.y, color)
            square.piece.has_not_moved = False
            if color == "white":
                game.white_moves.append(''.join([square.letter, square.number, '=R']))
                if game.black_in_check:
                    game.white_moves[-1] += "#"
            else:
                game.black_moves.append(''.join([square.letter, square.number, '=R']))
                if game.white_in_check:
                    game.black_moves[-1] += "#"
    else:
        # Promote to a Bishop
        if square.y_coordinate <= y <= (square.y_coordinate + tile_size / 2):
            square.piece = Bishop(square.x, square.y, color)
            if color == "white":
                game.white_moves.append(''.join([square.letter, square.number, '=B']))
                if game.black_in_check:
                    game.white_moves[-1] += "#"
            else:
                game.black_moves.append(''.join([square.letter, square.number, '=B']))
                if game.white_in_check:
                    game.black_moves[-1] += "#"
        # Promote to a Queen
        else:
            square.piece = Queen(square.x, square.y, color)
            if color == "white":
                game.white_moves.append(''.join([square.letter, square.number, '=Q']))
                if game.black_in_check:
                    game.white_moves[-1] += "#"
            else:
                game.black_moves.append(''.join([square.letter, square.number, '=Q']))
                if game.white_in_check:
                    game.black_moves[-1] += "#"


# update the board or interrupt the promotion
def update_pawn_promotion(game, board, tile_size, selected_square, x, y):
    if selected_square.promotions:
        # highlight the squares the pieces moved from and to
        game.last_move = [(selected_square.x, selected_square.y), (game.pawn_promotion[1].x, game.pawn_promotion[1].y)]
        # determine, which piece was chosen as a promotion piece
        select_promotion(selected_square, x, y, selected_square.promotions, tile_size, board, game)
        board[game.pawn_promotion[1].x][game.pawn_promotion[1].y].promotions = None
        game.pawn_promotion = False
        game.board_states[game.move_number] = deepcopy(board)
        game.move_number += 1
        game.whose_turn = not game.whose_turn
    # If clicked elsewhere, the promotion is stopped
    else:
        board[game.pawn_promotion[0].x][game.pawn_promotion[0].y].piece = game.pawn_promotion[0].piece
        board[game.pawn_promotion[1].x][game.pawn_promotion[1].y].piece = game.pawn_promotion[1].piece
        board[game.pawn_promotion[1].x][game.pawn_promotion[1].y].promotions = None
        game.pawn_promotion = False


def en_passant(game, board, selected_square):
    selected_square_x = selected_square.x
    selected_square_y = selected_square.y
    game.check_if_check(board)
    if game.move_piece.color == "white":
        board[selected_square_x][selected_square_y - 1].piece = None
        game.white_moves.append(
            ''.join([board[game.move_piece.x][game.move_piece.y].letter, 'x', selected_square.letter, selected_square.number]))
        if game.black_in_check:
            game.white_moves[-1] += "#"
    else:
        board[selected_square_x][selected_square_y + 1].piece = None
        game.black_moves.append(
            ''.join([board[game.move_piece.x][game.move_piece.y].letter, 'x', selected_square.letter, selected_square.number]))
        if game.white_in_check:
            game.black_moves[-1] += "#"
    board[selected_square_x][selected_square_y].piece = deepcopy(game.move_piece)
    board[selected_square_x][selected_square_y].piece.x = selected_square_x
    board[selected_square_x][selected_square_y].piece.y = selected_square_y
    board[game.move_piece.x][game.move_piece.y].piece = None
    game.board_states[game.move_number] = deepcopy(board)
    game.move_number += 1
    game.whose_turn = not game.whose_turn
