from copy import deepcopy

import pygame


# Draw a circle indicating the square to move to or the piece to capture
def draw_circle(screen, el, tile_size, color, player_color):
    if player_color:    # if the player is playing with white
        pygame.draw.circle(screen, color, (tile_size * (7 - el[0]) + tile_size / 2,
                                           tile_size * (7 - el[1]) + tile_size / 2), tile_size / 12)
    else:
        pygame.draw.circle(screen, color, (tile_size * el[0] + tile_size / 2,
                                           tile_size * el[1] + tile_size / 2), tile_size / 12)


def show_possible_moves(board, move_piece, screen, settings):
    # color the possible moves (squares)
    possible_moves = move_piece.possible_moves(board)
    if possible_moves:
        for el in possible_moves:
            draw_circle(screen, el, settings.tile_size, settings.possible_moves_color, settings.player_color)


def show_possible_captures(board, move_piece, screen, settings):
    # color the possible captures
    possible_captures = move_piece.possible_captures(board)
    if possible_captures:
        for el in possible_captures:
            draw_circle(screen, el, settings.tile_size, settings.possible_captures_color, settings.player_color)


def show_possible_castling(board, move_piece, screen, settings):
    # color the possible castling
    if move_piece.name == "King":
        possible_castling = move_piece.possible_castling(board)
        if possible_castling:
            for el in possible_castling:
                draw_circle(screen, el[0], settings.tile_size, settings.possible_castling_color, settings.player_color)


def castle_king(board, screen, movement, settings):
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
    update_screen(board, screen, settings)


# move or capture a piece
def update_board(board, selected_square, move_piece, screen, settings):
    # deepcopy the piece
    board[selected_square.x][selected_square.y].piece = deepcopy(board[move_piece.x][move_piece.y].piece)
    # set new co-ordinates
    board[selected_square.x][selected_square.y].piece.x = selected_square.x
    board[selected_square.x][selected_square.y].piece.y = selected_square.y
    # update movement status for king and rook
    if board[move_piece.x][move_piece.y].piece.name == "King" or board[move_piece.x][move_piece.y].piece.name == "Rook":
        board[selected_square.x][selected_square.y].piece.has_not_moved = False
    board[move_piece.x][move_piece.y].piece = None
    update_screen(board, screen, settings)


# Refresh the screen
def update_screen(board, screen, settings):
    for i in range(8):
        for j in range(8):
            board[i][j].display_tile(tile_size=settings.tile_size, white_tile_color=settings.white_tile_color,
                                     black_tile_color=settings.black_tile_color)
            if board[i][j].piece:
                board[i][j].display_piece(tile_size=settings.tile_size, dict_of_pictures=settings.dict_of_pictures)
