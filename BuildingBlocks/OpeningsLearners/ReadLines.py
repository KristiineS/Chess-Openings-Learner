import re
import string
from copy import deepcopy, copy

from BuildingBlocks.Classes.Game import Game
from BuildingBlocks.Initialize import initialize_board, initialize_pieces
from BuildingBlocks.MoveLogic import drag_piece


# Function to clean the file containing the opening lines.txt
def pgn_to_txt_file(old_location, new_location):
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
                    new_file.write(re.search('"([^"]*)"', line)[1].strip())
                    new_file.write("\n")
                # Write the name of the black line
                elif "[Black" in line.strip():
                    new_file.write(re.search('"([^"]*)"', line)[1])
                    new_file.write("\n")
                elif not re.match(r"^(\n).*$", line):
                    if memory:
                        memory = memory + " " + line.strip()
                    else:
                        memory = line.strip()
        if memory:
            new_file.write(memory)
            new_file.write("\n")

pgn_to_txt_file("Lines/all_lines.txt", "Lines/clean_html_lines.txt")


# Returns lists of 2-3 elements: name(s), line separated by commas
def lines_to_arrays(location):
    lines = []

    with open(location, "r", encoding="utf-8") as f:
        info = []
        for line in f:
            if line != "\n":
                info.append(line.strip())
            else:
                lines.append(info)
                info = []
    lines.append(info)
    return lines

lineArray = lines_to_arrays("Lines/clean_html_lines.txt")


# Find repeating lines (by white)
def find_repetitions(line_array):
    seen = set()
    repeated = set()
    for listike in line_array:
        if listike[0] in seen:
            repeated.add(listike[0])
        else:
            seen.add(listike[0])
    return sorted(list(repeated))

repeated = find_repetitions(lineArray)


# Find the shortest name for the opening (e.g. Vienna, not Vienna game or gambit)
def unique_line_names(repeated):
    repeats = copy(repeated)
    for i in range(len(repeated)-1):
        for j in range(i+1, len(repeated)):
            if (repeated[i] in repeated[j] or repeated[j] in repeated[i]) and (repeated[0:5] == repeated[0:5]):
                longer = repeated[i] if len(repeated[i]) > len(repeated[j]) else repeated[j]
                if longer in repeats:
                    repeats.remove(longer)
    return repeats

name_set = unique_line_names(repeated)


# def get_repeated_line_names(lines, repeated):
#     repeated_lines_names = {}
#     for line in lines:
#         for name in repeated:
#             if name in line:
#                 if name in repeated_lines_names:
#                     repeated_lines_names[name] += 1
#                 else:
#                     repeated_lines_names[name] = 1
#
#     for line in lines:
#         if line[0] in repeated_lines_names and line[1] in repeated_lines_names:
#             if repeated_lines_names[line[0]] > repeated_lines_names[line[1]]:
#                 repeated_lines_names.pop(line[1])
#             else:
#                 repeated_lines_names.pop(line[0])
#     return sorted(set(repeated_lines_names))

# name_set = get_repeated_line_names(lineArray, repeats)


def lines_to_html(new_location, lines, openings):
    with open(new_location, 'r+', encoding="utf-8") as new_file:
        counter = 0
        line_ids = []
        for line_name in openings:
            new_file.write("<li>")
            new_file.write("\n")
            new_file.write(
                '<input type="checkbox" id="' + line_name + '" name="openings" onclick="checkChildren(this)" checked>')
            new_file.write("\n")
            new_file.write('<label for="' + line_name + '">')
            new_file.write("\n")
            new_file.write("<b>" + line_name + "</b>")
            new_file.write("\n")
            new_file.write('</label>')
            new_file.write("\n")
            new_file.write('<button type="button" class="btn btn-no-outline collapsed dropdown-toggle" data-toggle="collapse" data-target="#'+ 'toggle' + str(counter) +'"></button>')
            new_file.write("\n")
            new_file.write('<ul class="collapse hide" id="'+ "toggle" + str(counter) +'">')
            new_file.write("\n")

            for line in lines:
                if line[0] in line_name or line_name in line[0]:
                    line_ids.append(line[0]+" "+line[-1])
                    new_file.write("<li>")
                    new_file.write("\n")
                    new_file.write('<input type="checkbox" id="' + line[-1] + '-of-' + line_name +
                                   '" name="openings" value="'+line[-1]+'" onclick="checkChildren(this)" checked>')
                    new_file.write("\n")
                    new_file.write('<label for="' + line[-1] + '-of-' + line_name + '">')
                    new_file.write("\n")
                    new_file.write("<b>" + str(line[0]) + "</b>")
                    if len(line) == 3:
                        new_file.write("<b>" + ", " + str(line[1]) + "</b>")
                        new_file.write("\n")
                    new_file.write('<br>')
                    new_file.write("\n")
                    new_file.write(str(line[-1]))
                    new_file.write("\n")
                    new_file.write('</label>')
                    new_file.write("\n")
                    new_file.write("</li>")
                    new_file.write("\n")

            new_file.write("</ul>")
            new_file.write("\n")
            new_file.write("</li>")
            new_file.write("\n\n")
            counter += 1
        new_thingy = []
        for line in lines:
            name = line[0]+" "+line[-1]
            if name not in line_ids:
                print(name)
        print(len(new_thingy))

lines_to_html("Lines/html_grouped.txt", lineArray, name_set)

def clean_lines_with_board_states(old_location, new_location):
    with open(old_location, "r", encoding="utf-8") as old_file, open(new_location, 'r+', encoding="utf-8") as new_file:
        for line in old_file:
            if "1. " not in line.strip():
                new_file.write(line)
            else:
                new_file.write(line)
                board_states = [state for state in line.split() if "." not in state]
                _, line_state_strings = line_to_board_state(board_states)
                new_file.write(str(line_state_strings))
                new_file.write("\n")


def line_info_into_variables(array_of_lines):
    line_names = []
    state_strings = []
    for line in array_of_lines:
        line_names.append(line[0]) if len(line) == 3 else line_names.append((line[0], line[1])) # Get line name(s)
        new_list = line[-1].strip("[]'").split("', '")
        state_strings.append(new_list) # Get the board Strings

    return line_names, state_strings


def line_to_board_state(board_states):
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
    line_state_strings = [board_to_matrix(board)]

    for i in range(0, len(board_states)):
        board_state = board_states[i].strip("+").strip("#")
        color = "white" if i % 2 == 0 else "black"
        # e4, Bg5, Bxg4, 0-0, 0-0-0, h7=Q, hxg8=Q
        if re.match(r"^(R).*$", board_state):
            game, board = move_or_capture(game, board, settings, board_state, "Rook", color)
        elif re.match(r"^(N).*$", board_state):
            game, board = move_or_capture(game, board, settings, board_state, "Knight", color)
        elif re.match(r"^(B).*$", board_state):
            game, board = move_or_capture(game, board, settings, board_state, "Bishop", color)
        elif re.match(r"^(Q).*$", board_state):
            game, board = move_or_capture(game, board, settings, board_state, "Queen", color)
        elif re.match(r"^(K).*$", board_state):
            game, board = move_or_capture(game, board, settings, board_state, "King", color)
        elif re.match(r"(O-O).*$", board_state):
            game, board = castle(game, board, settings, board_state, "King", color)
        elif "=" in board_state:
            print("Promote (with capture)")
        else:
            game, board = move_or_capture(game, board, settings, board_state, "Pawn", color)
        line_states.append(board)
        line_state_strings.append(board_to_matrix(board))

    return line_states, line_state_strings


# TODO - en passant
def move_or_capture(game, board, settings, move_name, move_piece, move_color):
    alphabet = string.ascii_lowercase
    if "x" in move_name:
        move_name = move_name.split("x")[-1]
        captures = True
    else:
        move_name = move_name[-2:]
        captures = False
    for i in range(8):
        for j in range(8):
            if board[i][j].piece:
                if board[i][j].piece.name == move_piece and board[i][j].piece.color == move_color:
                    end_i, end_j = (alphabet.find(move_name[0]), int(move_name[1]) - 1)
                    movement = board[i][j].piece.possible_captures(board) if captures else board[i][
                        j].piece.possible_moves(board)
                    if (end_i, end_j) in movement:
                        drag_piece(game, board, settings, board[i][j], board[end_i][end_j], 0, 0)

    return game, board


def castle(game, board, settings, board_state, move_piece, move_color):
    length = 2 if len(board_state) == 3 else 3  # short or long castles
    for i in range(8):
        for j in range(8):
            if board[i][j].piece:
                if board[i][j].piece.name == move_piece and board[i][j].piece.color == move_color:
                    castle_to = board[i][j].piece.possible_castling(board)
                    for movement in castle_to:
                        if abs(movement[2][0] - movement[3][0]) == length:
                            end_i, end_j = movement[0][0], movement[0][1]
                            drag_piece(game, board, settings, board[i][j], board[end_i][end_j], 0, 0)
    return game, board


# TODO - def promotion()
def promotion(game, board, settings, board_state, move_piece, move_color):
    pass


# empty = 00, piece = 1(white) or 2(black) + type = 123456 (bishop, king, knight, pawn, queen, rook)
def board_to_matrix(board):
    string = ""
    for i in range(8):
        for j in range(8):
            if board[i][j].piece:
                if board[i][j].piece.name == "Bishop":
                    string += "11" if board[i][j].piece.color == "white" else "21"
                elif board[i][j].piece.name == "King":
                    string += "12" if board[i][j].piece.color == "white" else "22"
                elif board[i][j].piece.name == "Knight":
                    string += "13" if board[i][j].piece.color == "white" else "23"
                elif board[i][j].piece.name == "Pawn":
                    string += "14" if board[i][j].piece.color == "white" else "24"
                elif board[i][j].piece.name == "Queen":
                    string += "15" if board[i][j].piece.color == "white" else "25"
                else:
                    string += "16" if board[i][j].piece.color == "white" else "26"
            else:
                string += "00"

    return string


# clean_lines_with_board_states("/Users/kristi/Documents/Programming/Chess-Openings-Learner/BuildingBlocks/OpeningsLearners/Lines/clean_lines.txt", "Lines/lines_and_board_states.txt")



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
