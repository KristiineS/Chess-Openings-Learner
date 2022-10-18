from BuildingBlocks.Move import update_board, promote, castle_king, update_pawn_promotion, en_passant
from BuildingBlocks.ShowPossibleMoves import show_possible_moves, show_possible_captures, show_possible_castling, \
    show_possible_promotion, show_possible_en_passant


def drag_piece(game, board, settings, start_piece_square, end_piece_square, x, y):
    move_number = game.move_number
    promotion_row = 6 if game.player_color else 1
    en_passant_row = 4 if game.player_color else 3
    # If a promotion is in process, select the chosen piece
    if game.pawn_promotion:
        update_pawn_promotion(game, board, settings.tile_size, end_piece_square, x, y)
    else:
        game.move_piece = start_piece_square.piece
        # if there is an enemy's piece on the final square, capture the piece
        if end_piece_square.piece is not None:
            if end_piece_square.piece.color != game.move_piece.color:
                possible_captures = game.move_piece.possible_captures(board)
                if possible_captures and (end_piece_square.piece.x, end_piece_square.piece.y) in possible_captures:
                    update_board(board, end_piece_square, game)
                elif game.move_piece.name == "Pawn":
                    promotions = game.move_piece.possible_promotions(board)
                    for movement in promotions:
                        if (end_piece_square.x, end_piece_square.y) == movement:
                            promote(board, end_piece_square.x, end_piece_square.y, game)
                            game.move_piece = None
        # if there is not a piece on the clicked square, move there or en passant a pawn
        else:
            # move to a new square
            if game.move_piece is not None:
                if (end_piece_square.x, end_piece_square.y) in game.move_piece.possible_moves(board):
                    update_board(board, end_piece_square, game)
                # Castle the king
                elif game.move_piece.name == "King":
                    castle_to = game.move_piece.possible_castling(board)
                    for movement in castle_to:
                        if (end_piece_square.x, end_piece_square.y) == movement[0]:
                            castle_king(board, movement, game)
                # Promote a pawn or en passant
                elif game.move_piece.name == "Pawn":
                    if move_number > 2 and game.move_piece.y == en_passant_row:
                        last_moved_piece = game.black_moves[move_number // 2 - 1] if game.whose_turn \
                            else game.white_moves[move_number // 2]
                        possible_en_passant = \
                            game.move_piece.possible_en_passant(last_moved_piece, game.board_states[move_number - 2])[0]
                        if possible_en_passant and end_piece_square.x == possible_en_passant[
                            0] and end_piece_square.y == \
                                possible_en_passant[1]:
                            en_passant(game, board, end_piece_square)
                            game.move_piece = None
                    elif game.move_piece.y == promotion_row:
                        promotions = game.move_piece.possible_promotions(board)
                        for movement in promotions:
                            if (end_piece_square.x, end_piece_square.y) == movement:
                                promote(board, end_piece_square.x, end_piece_square.y, game)
                                game.move_piece = None
    game.move_piece = None


def click_piece(game, board, settings, selected_square, x, y):
    move_number = game.move_number
    promotion_row = 6 if game.player_color else 1
    en_passant_row = 4 if game.player_color else 3
    # If a promotion is in process, select the chosen piece
    if game.pawn_promotion:
        update_pawn_promotion(game, board, settings.tile_size, selected_square, x, y)
    else:
        # if a piece has been selected before
        if game.move_piece:
            # Capture
            if selected_square.piece:
                possible_captures = game.move_piece.possible_captures(board)
                if (selected_square.piece.x, selected_square.piece.y) in possible_captures:
                    update_board(board, selected_square, game)
                    game.move_piece = None
                # Unselect
                elif selected_square.piece == game.move_piece:
                    game.move_piece = None
                # Choose new piece and visualize
                else:
                    if selected_square.piece.color == game.move_piece.color and selected_square.piece != game.move_piece:
                        game.move_piece = selected_square.piece
                        show_possible_moves(board, game.move_piece, settings.possible_moves_color)
                        show_possible_captures(board, game.move_piece, settings.possible_captures_color)
                        if game.move_piece.name == "King":
                            show_possible_castling(board, game.move_piece, settings.possible_castling_color)
                        if game.move_piece.name == "Pawn":
                            show_possible_promotion(board, game.move_piece, settings.possible_promotions_color)
                            # get the pgn code of the last move
                            if move_number > 2:
                                last_moved_piece = game.black_moves[move_number // 2 - 1] if game.whose_turn else \
                                game.white_moves[move_number // 2]
                                show_possible_en_passant(board, game.move_piece, settings.possible_en_passant_color,
                                                         last_moved_piece, game.board_states[move_number - 2])
            # Move
            elif (selected_square.x, selected_square.y) in game.move_piece.possible_moves(board):
                update_board(board, selected_square, game)
                game.move_piece = None
            # Promote or en passant
            elif game.move_piece.name == "Pawn":
                if game.move_piece.y == promotion_row:
                    promotions = game.move_piece.possible_promotions(board)
                    # Promote
                    if promotions:
                        for movement in promotions:
                            if (selected_square.x, selected_square.y) == movement:
                                promote(board, selected_square.x, selected_square.y, game)
                                game.move_piece = None
                # Data for en passant
                if move_number > 2 and game.move_piece.y == en_passant_row:
                    last_moved_piece = game.black_moves[move_number // 2 - 1] if game.whose_turn else game.white_moves[
                        move_number // 2]
                    possible_en_passant = game.move_piece.possible_en_passant(last_moved_piece, game.board_states[move_number - 2])[0]
                    # En passant
                    if possible_en_passant and selected_square.x == possible_en_passant[0] and selected_square.y == possible_en_passant[1]:
                        en_passant(game, board, selected_square)
                        game.move_piece = None
            # Castle the king
            elif game.move_piece.name == "King":
                castle_to = game.move_piece.possible_castling(board)
                for movement in castle_to:
                    if (selected_square.x, selected_square.y) == movement[0]:
                        castle_king(board, movement, game)
                        game.move_piece = None
            # In other cases unselect
            else:
                game.move_piece = None
        else:
            if selected_square.piece:
                if selected_square.piece.color == game.player_color_name:
                    game.move_piece = selected_square.piece
                    show_possible_moves(board, game.move_piece, settings.possible_moves_color)
                    show_possible_captures(board, game.move_piece, settings.possible_captures_color)
                    if game.move_piece.name == "King":
                        show_possible_castling(board, game.move_piece, settings.possible_castling_color)
                    if game.move_piece.name == "Pawn":
                        show_possible_promotion(board, game.move_piece, settings.possible_promotions_color)
                        # get the pgn code of the last move
                        if move_number > 2:
                            last_moved_piece = game.black_moves[move_number // 2 - 1] if game.whose_turn else game.white_moves[move_number // 2]
                            show_possible_en_passant(board, game.move_piece, settings.possible_en_passant_color,
                                                     last_moved_piece, game.board_states[move_number - 2])
                else:
                    game.move_piece = None

            else:
                game.move_piece = None
