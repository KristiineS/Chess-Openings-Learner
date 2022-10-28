from copy import deepcopy

import pyglet

from BuildingBlocks.Classes.Game import Game
from BuildingBlocks.Initialize import initialize_board, initialize_pieces
from BuildingBlocks.OpeningsLearners.ResponseMoves import response_move
from BuildingBlocks.OpeningsLearners.ReadLines import clean_lines, lines_to_board_states, board_to_matrix
from BuildingBlocks.Screen import update_screen, click_square
from BuildingBlocks.Classes.Settings import Settings
from BuildingBlocks.MoveLogic import drag_piece, click_piece

# General settings
settings = Settings(player=True ,
                    possible_moves_color="grey", possible_captures_color="red", possible_castling_color="black",
                    possible_promotions_color="green", possible_en_passant_color="red", last_move_color="yellow",
                    tile_size=60, white_tile_color="white", black_tile_color="Sienna")

# Define Pyglet window
game_window = pyglet.window.Window(width=settings.width, height=settings.height, caption="Chess", resizable=True)
game_window.set_minimum_size(480, 480)

# Initialization of the board
board = initialize_board(settings)
initialize_pieces(board, "white")
initialize_pieces(board, "black")
start_pos_x, start_pos_y, stop_pos_x, stop_pos_y = 0, 0, 0, 0

# Initialize the game
game = Game(player_color_name=settings.player_color_name)  # playing with white
game.board_states[0] = deepcopy(board)
lines = clean_lines("BuildingBlocks/OpeningsLearners/Lines/clean_lines.txt")
# Line names, board state matrices, board state strings
names, opening_lines_unflattened, board_state_strings = lines_to_board_states(lines)
board_state_strings_flattened = [item for sublist in board_state_strings for item in sublist]
opening_lines = set(board_state_strings_flattened)


@game_window.event
def on_draw():
    global game, board
    if game.player != game.whose_turn:
        game, board = response_move(board, game, settings, opening_lines)
    game_window.clear()
    update_screen(board, game, settings)


@game_window.event
def on_mouse_press(x, y, button, modifiers):
    global start_pos_x, start_pos_y
    start_pos_x, start_pos_y = x, y


@game_window.event
def on_mouse_release(x, y, button, modifiers):
    global start_pos_x, start_pos_y, stop_pos_x, stop_pos_y, game, board

    if game.player == game.whose_turn:
        stop_pos_x, stop_pos_y = x, y
        # right the button is clicked/dragged
        if button == 1:
            # dragged, not clicked
            if start_pos_x != stop_pos_x and start_pos_y != stop_pos_y:
                # check if valid movement
                start_piece_square = click_square(board, start_pos_x, start_pos_y, settings.tile_size)
                if start_piece_square:
                    # check that the player clicked their own piece
                    if game.whose_turn and start_piece_square.piece and start_piece_square.piece.color == "white" \
                            or not game.whose_turn and start_piece_square.piece and start_piece_square.piece.color == "black":
                        selected_square = click_square(board, stop_pos_x, stop_pos_y,
                                                       settings.tile_size)  # False or Square
                        if selected_square:
                            drag_piece(game, board, settings, start_piece_square, selected_square, x, y)
            # clicked, not dragged
            else:
                selected_square = click_square(board, stop_pos_x, stop_pos_y, settings.tile_size)  # False or Square
                # check if legal move
                if selected_square:
                    if not selected_square.piece:
                        click_piece(game, board, settings, selected_square, x, y)
                    else:
                        if game.move_piece:
                            click_piece(game, board, settings, selected_square, x, y)
                        else:
                            if selected_square.piece.color == "white" and game.whose_turn \
                                    or selected_square.piece.color == "black" and not game.whose_turn:
                                click_piece(game, board, settings, selected_square, x, y)


@game_window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    pass


@game_window.event
def on_resize(width, height):
    global settings
    settings.set_new_size(width, height)
    for i in range((board.shape[0])):
        for j in range((board.shape[1])):
            board[i][j].set_new_tile_size(settings.tile_size, settings.player)


if __name__ == '__main__':
    pyglet.app.run()
