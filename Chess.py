import pygame

from BuildingBlocks.Initialize import initialize_board, initialize_pieces
from BuildingBlocks.Classes.Settings import Settings
from Visualize import show_possible_moves, show_possible_captures, show_possible_castling, update_screen, update_board, castle_king


# TODO
# [King] castling - check if in check, check if does not move through fire (check, pin, fire line)
# + [Pawn] promotion - 4 options, empty square
# [Pawn] en passant
# + [King] Check, Check-Mate
# [King] Pin - check if the king can move
# + [Game] Implement dragging for moving
# + [Game] Left-click for drawing
# + [Game] Add letters and numbers
# [Game] Choose the colors for the board and the dots (settings menu)
# [Game] Better dragging for castling
# [Game] Make size dynamic


# Select a piece via a mouse click
def click_square(board, x, y, settings):
    for i in range((board.shape[0])):
        for j in range((board.shape[1])):
            # checking if the position of the mouse is inside the selected square
            if board[i][j].x_coordinate <= x <= (board[i][j].x_coordinate + settings.tile_size) \
                    and board[i][j].y_coordinate <= y <= (board[i][j].y_coordinate + settings.tile_size):
                return board[i][j]
    return False


def main():
    # General settings
    settings = Settings(player_color=True, possible_moves_color="dark grey", possible_captures_color="dark red",
                        possible_castling_color="black", tile_size=70, white_tile_color="white", black_tile_color="black")

    # Set the Pygame frame
    pygame.init()
    pygame.display.set_caption('Chess')
    pygame.event.set_allowed(pygame.QUIT)
    pygame.event.set_allowed(pygame.MOUSEBUTTONUP)
    screen = pygame.display.set_mode((settings.width, settings.height))

    # Initializations for one game
    board = initialize_board(settings)
    initialize_pieces(board, "white")
    initialize_pieces(board, "black")
    update_screen(board, screen, settings)
    move_piece = None  # save the piece to move

    running = True
    while running:
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # moving the pieces or visualizing the possibilities
            if event.type == pygame.MOUSEBUTTONUP:
                (mouseX, mouseY) = pygame.mouse.get_pos()
                selected_square = click_square(board, mouseX, mouseY, settings)  # False or Square
                # if the click is not on the border
                if selected_square is not None:
                    # if a piece has been selected and there is a piece on the clicked square,
                    # unselect, capture or re-choose & visualize
                    if selected_square.piece is not None:
                        # if a piece has been selected before
                        if move_piece:
                            # unselect the piece
                            if selected_square.piece == move_piece:
                                move_piece = None
                                update_screen(board, screen, settings)
                            # re-choose & visualize possible moves
                            elif selected_square.piece.color == move_piece.color:
                                move_piece = selected_square.piece
                                update_screen(board, screen, settings)
                                # color the possible moves
                                show_possible_moves(board, move_piece, screen, settings)
                                # color the possible captures
                                show_possible_captures(board, move_piece, screen, settings)
                                # color the possible castling
                                show_possible_castling(board, move_piece, screen, settings)
                            # capture or re-select
                            else:
                                possible_captures = move_piece.possible_captures(board)
                                # capture
                                if possible_captures and (selected_square.piece.x, selected_square.piece.y) in possible_captures:
                                    update_board(board, selected_square, move_piece, screen, settings)
                                    move_piece = None
                                # re-select
                                else:
                                    update_screen(board, screen, settings)
                                    move_piece = selected_square.piece
                                    # color the possible moves
                                    show_possible_moves(board, move_piece, screen, settings)
                                    # color the possible captures
                                    show_possible_captures(board, move_piece, screen, settings)
                                    # color the possible castling
                                    show_possible_castling(board, move_piece, screen, settings)
                        # if no piece has been selected, choose the piece & visualize possible movements
                        else:
                            update_screen(board, screen, settings)
                            move_piece = selected_square.piece
                            # color the possible moves
                            show_possible_moves(board, move_piece, screen, settings)
                            # color the possible captures
                            show_possible_captures(board, move_piece, screen, settings)
                            # color the possible castling
                            show_possible_castling(board, move_piece, screen, settings)
                    # if there is not a piece on the clicked square, move there or unselect
                    else:
                        # move to a new square
                        if move_piece:
                            update_screen(board, screen, settings)
                            if (selected_square.x, selected_square.y) in move_piece.possible_moves(board):
                                update_board(board, selected_square, move_piece, screen, settings)
                                move_piece = None
                            elif move_piece.name == "King":
                                castle_to = move_piece.possible_castling(board)
                                for movement in castle_to:
                                    if (selected_square.x, selected_square.y) == movement[0]:
                                        castle_king(board, screen, movement, settings)
                                        move_piece = None
                        # when clicked on an empty square, unselect
                        else:
                            move_piece = None
                            update_screen(board, screen, settings)

            pygame.event.clear()

    pygame.quit()


if __name__ == '__main__':
    main()
