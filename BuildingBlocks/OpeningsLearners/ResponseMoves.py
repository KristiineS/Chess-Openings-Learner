from copy import deepcopy
from random import randint

from BuildingBlocks.MoveLogic import drag_piece


def response_move(board, game, settings, opening_lines):
    ai_color = "black" if game.player_color else "white"
    all_possible_board_states = []

    for i in range(8):
        for j in range(8):
            if board[i][j].piece and board[i][j].piece.color == ai_color:
                # TODO - try to move it
                all_possible_moves = []
                all_possible_moves += board[i][j].piece.possible_moves(board)
                all_possible_moves += board[i][j].piece.possible_captures(board)
                for coordinates in all_possible_moves:
                    board_copy = deepcopy(board)
                    game_copy = deepcopy(game)
                    game_copy.move_piece = board[i][j].piece
                    drag_piece(game_copy, board_copy, settings, board[i][j],
                               board[coordinates[0]][coordinates[1]], coordinates[0], coordinates[1])
                    all_possible_board_states.append((game_copy, board_copy))

    random_choice = randint(0, len(all_possible_board_states))
    random_game, random_board = deepcopy(all_possible_board_states[random_choice][0]), \
                                deepcopy(all_possible_board_states[random_choice][1])

    return random_game, random_board
