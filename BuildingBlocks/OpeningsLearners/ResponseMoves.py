from copy import deepcopy
from random import randint

import numpy as np

from BuildingBlocks.Move import promote
from BuildingBlocks.MoveLogic import drag_piece


def response_move(board, game, settings, opening_lines):
    ai_color = "black" if game.player else "white"
    promotion_row = 1 if game.player else 6
    en_passant_row = 3 if game.player else 4
    all_possible_board_states = []

    for i in range(8):
        for j in range(8):
            if board[i][j].piece and board[i][j].piece.color == ai_color:
                # Check all possible moves, captures, en passant and promotions
                all_possible_moves = []
                all_possible_moves += board[i][j].piece.possible_moves(board)
                all_possible_moves += board[i][j].piece.possible_captures(board)
                if board[i][j].piece.name == "Pawn":
                    if board[i][j].piece.y == promotion_row:
                        # TODO - try all possible promotions and then promote to all 4 possible options
                        possible_promotions = board[i][j].piece.possible_promotions(board)
                        if possible_promotions:
                            for promotion in possible_promotions:
                                # Get 4 possible promotion options by indexes
                                x = board[promotion[0]][promotion[1]].x * settings.tile_size
                                y = board[promotion[0]][promotion[1]].y * settings.tile_size
                                x_options = np.array([0.25, 0.25, 0.75, 0.75]) * settings.tile_size + x
                                y_options = np.array([0.25, 0.75, 0.25, 0.75]) * settings.tile_size + y
                                for k in range(4):
                                    board_copy = deepcopy(board)
                                    game_copy = deepcopy(game)
                                    promotion_square = board_copy[promotion[0]][promotion[1]]
                                    game_copy.move_piece = board_copy[i][j].piece
                                    promote(board_copy, promotion_square.x, promotion_square.y, game_copy)
                                    game_copy.move_piece = None
                                    drag_piece(game_copy, board_copy, settings, board_copy[i][j], promotion_square,
                                               x_options[k], y_options[k])
                                    all_possible_board_states.append((game_copy, board_copy))

                    elif game.move_number > 2 and board[i][j].piece.y == en_passant_row:
                        last_moved_piece = game.black_moves[game.move_number // 2 - 1] if game.whose_turn \
                            else game.white_moves[game.move_number // 2]
                        all_possible_moves += board[i][j].piece.possible_en_passant(last_moved_piece,
                                                                                    game.board_states[
                                                                                        game.move_number - 2])
                for coordinates in all_possible_moves:
                    board_copy = deepcopy(board)
                    game_copy = deepcopy(game)
                    game_copy.move_piece = board[i][j].piece
                    drag_piece(game_copy, board_copy, settings, board[i][j], board[coordinates[0]][coordinates[1]], 0,
                               0)
                    all_possible_board_states.append((game_copy, board_copy))

                # Check both possible castling moves
                if board[i][j].piece.name == "King":
                    all_possible_castling = []
                    all_possible_castling += board[i][j].piece.possible_castling(board)
                    for coordinates in all_possible_castling:
                        board_copy = deepcopy(board)
                        game_copy = deepcopy(game)
                        game_copy.move_piece = board[i][j].piece
                        drag_piece(game_copy, board_copy, settings, board[coordinates[1][0]][coordinates[1][1]],
                                   board[coordinates[0][0]][coordinates[0][1]], 0, 0)
                        all_possible_board_states.append((game_copy, board_copy))

    if len(all_possible_board_states) != 0:
        random_choice = randint(0, len(all_possible_board_states) - 1)
        random_game, random_board = deepcopy(all_possible_board_states[random_choice][0]), \
                                    deepcopy(all_possible_board_states[random_choice][1])
        return random_game, random_board
    else:
        print("Finished!")
