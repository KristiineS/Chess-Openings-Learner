import random
import numpy as np

from BuildingBlocks.CheckOrMate import check_if_check
from BuildingBlocks.MoveLogic import drag_piece


def response_move(board, game, settings, opening_lines_unflattened):
    if game.player_color != game.whose_turn:
        if game.move_number == 0:
            # A randomly chosen opening line with the first move played
            current_matrix = random.choice(opening_lines_unflattened)[1][1]
            # The differences in the matrices between the start and the first move
            x_values, y_values = np.where((game.matrices[0]-current_matrix) != 0)
            x, y = 0, 0     # not important here
            for i in range(len(x_values)):
                if board[x_values[i]][y_values[i]].piece and \
                        game.player_color != board[x_values[i]][y_values[i]].piece.color:
                    start_piece = board[x_values[i]][y_values[i]]
                else:
                    selected_square = board[x_values[i]][y_values[i]]
            drag_piece(game, board, settings, start_piece, selected_square, x, y)
            game.under_fire = check_if_check(board, game)
        else:
            for el in opening_lines_unflattened: # to-do opening_lines
                if np.array_equal(game.matrices[game.move_number], el):
                    print("j")
                    # start_piece = click_square(board, start_pos_x, start_pos_y, settings.tile_size)
                    # selected_square = click_square(board, stop_pos_x, stop_pos_y, settings.tile_size)
                    # drag_piece(game, board, settings, start_piece, selected_square, x, y)
