import re
import string
from copy import deepcopy

from BuildingBlocks.Classes.Game import Game
from BuildingBlocks.Initialize import initialize_board, initialize_pieces
from BuildingBlocks.MoveLogic import drag_piece


# Function to clean the file containing the opening lines.txt
def pgn_to_txt(old_location, new_location):
    memory = ""
    with open(old_location, "r", encoding="utf-8") as old_file, open(new_location, 'r+', encoding="utf-8") as new_file:
        for line in old_file:
            if "[Site" not in line.strip():
                # Write the name of the white line
                if "[White" in line.strip():
                    if memory:
                        new_file.write(memory)
                        new_file.write("\n")
                        new_file.write("\n")
                        memory = ""
                    new_file.write("White: " + re.search('"([^"]*)"', line)[1].strip())
                    new_file.write("\n")
                # Write the name of the black line
                elif "[Black" in line.strip():
                    new_file.write("Black: " + re.search('"([^"]*)"', line)[1])
                    new_file.write("\n")
                elif not re.match(r"^(\n).*$", line):
                    if memory:
                        memory = memory + " " + line.strip()
                    else:
                        memory = line.strip()
        if memory:
            new_file.write(memory)
            new_file.write("\n")


# pgn_to_txt("Lines/all_lines.txt", "Lines/clean_lines.txt")


# Returns lists of 2-3 elements: name(s), line separated by commas
def clean_lines(location):
    lines = []

    with open(location, "r", encoding="utf-8") as f:
        info = []
        for line in f:
            if line != "\n":
                info.append(line.strip())
            else:
                lines.append(info)
                info = []

    return lines


list_of_lines = clean_lines("Lines/clean_lines.txt")


# ["White: King's Indian", 'Black: Anti', '1. d4 Nf6 2. c4 g6 3. d5']
def lines_to_board_states(list_of_lines):
    print(list_of_lines)
    board_state_lines = []
    for line in list_of_lines:
        # Get line name(s)
        if len(line) == 2:
            line_name = line[0]
        else:
            line_name = (line[0], line[1])
        board_states = [state for state in line[-1].split() if "." not in state]
        print(board_states)

        # Initializations
        class Settings:
            def __init__(self):
                self.tile_size = 60
                self.player = True
                self.player_color_name = "white"

        settings = Settings()
        board = initialize_board(settings)
        initialize_pieces(board, "white")
        initialize_pieces(board, "black")
        game = Game(player_color_name=settings.player_color_name)  # playing with white
        game.board_states[0] = deepcopy(board)
        # Transfer moves to board states
        line_states = [board]
        for i in range(0, len(board_states)):
            board_state = board_states[i].strip("+").strip("#")
            color = "white" if i % 2 == 0 else "black"
            # e4, Bg5, Bxg4, 0-0, 0-0-0, h7=Q, hxg8=Q
            if re.match(r"^(R).*$", board_state):
                move_or_capture(game, board, settings, board_state, "Rook", color)
            elif re.match(r"^(N).*$", board_state):
                move_or_capture(game, board, settings, board_state, "Knight", color)
            elif re.match(r"^(B).*$", board_state):
                move_or_capture(game, board, settings, board_state, "Bishop", color)
            elif re.match(r"^(Q).*$", board_state):
                move_or_capture(game, board, settings, board_state, "Queen", color)
            elif re.match(r"^(K).*$", board_state):
                move_or_capture(game, board, settings, board_state, "King", color)
            elif re.match(r"(O-O).*$", board_state):
                castle(game, board, settings, board_state, "King", color)
            elif "=" in board_state:
                print("Promote (with capture)")
            else:
                move_or_capture(game, board, settings, board_state, "Pawn", color)
            line_states.append(board)
        print()
        board_state_lines.append((line_name, line_states))

    return board_state_lines


# TODO - en passant
def move_or_capture(game, board, settings, move_name, move_piece, move_color):
    alphabet = string.ascii_lowercase
    if "x" in move_name:
        move_name = move_name.split("x")[-1]
        done_thingy = " captured "
        captures = True
    else:
        move_name = move_name[-2:]
        done_thingy = " moved "
        captures = False
    for i in range(8):
        for j in range(8):
            if board[i][j].piece:
                if board[i][j].piece.name == move_piece and board[i][j].piece.color == move_color:
                    end_i, end_j = (alphabet.find(move_name[0]), int(move_name[1]) - 1)
                    movement = board[i][j].piece.possible_captures(board) if captures else board[i][
                        j].piece.possible_moves(board)
                    if (end_i, end_j) in movement:
                        print(str(i) + " " + str(j) + done_thingy + move_piece)
                        drag_piece(game, board, settings, board[i][j], board[end_i][end_j], 0, 0)

    return game, board


def castle(game, board, settings, board_state, move_piece, move_color):
    length = 2 if len(board_state) == 3 else 3 # short or long castles
    done_thingy = " short castles" if length == 2 else " long castles"
    for i in range(8):
        for j in range(8):
            if board[i][j].piece:
                if board[i][j].piece.name == move_piece and board[i][j].piece.color == move_color:
                    castle_to = board[i][j].piece.possible_castling(board)
                    for movement in castle_to:
                        if abs(movement[2][0] - movement[3][0]) == length:
                            end_i, end_j = movement[0][0], movement[0][1]
                            print(str(i) + " " + str(j) + done_thingy)
                            drag_piece(game, board, settings, board[i][j], board[end_i][end_j], 0, 0)
    return game, board


lines_to_board_states(list_of_lines)


# # board, move == e8=Q, move_piece_color == "white"
# def promote(board, move, move_piece_color):
#     dict_let = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}
#     dict_num = {0: '1', 1: '2', 2: '3', 3: '4', 4: '5', 5: '6', 6: '7', 7: '8'}
#     j = 6 if move_piece_color == "white" else 1
#     promotion, to_piece = move.split("=")
#     promotion = promotion.split("x")[-1] if "x" in promotion else promotion
#     for i in range(8):
#         if board[i][j].piece and board[i][j].piece.name == "Pawn" and board[i][j].piece.color == move_piece_color:
#             for (x, y) in board[i][j].piece.possible_promotions(board):
#                 if promotion == (dict_let[x] + dict_num[y]):
#                     # ("promote", move, dict_let[x] + dict_num[y] + "=" + to_piece)
#                     if to_piece == "Q":
#                         board[x][y].piece = Queen(x, y, move_piece_color)
#                     elif to_piece == "R":
#                         board[x][y].piece = Rook(x, y, move_piece_color)
#                     elif to_piece == "N":
#                         board[x][y].piece = Knight(x, y, move_piece_color)
#                     else:
#                         board[x][y].piece = Bishop(x, y, move_piece_color)
#                     board[i][j].piece = None
#                     return board
#
#