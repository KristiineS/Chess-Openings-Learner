from itertools import product

import pygame


class Settings:
    def __init__(self, player_color: bool, possible_moves_color: str, possible_captures_color: str, possible_castling_color: str,
                 tile_size: int, white_tile_color: str, black_tile_color: str):
        self.player_color = player_color    # True: white, False: black
        # colors
        self.possible_moves_color = possible_moves_color
        self.possible_captures_color = possible_captures_color
        self.possible_castling_color = possible_castling_color
        # window settings
        self.tile_size = tile_size
        self.width = 8 * tile_size
        self.height = 8 * tile_size
        # piece pictures and board colors
        self.dict_of_pictures = self.initialize_pictures()
        self.white_tile_color = white_tile_color
        self.black_tile_color = black_tile_color

    # Load pictures of the pieces from a local folder
    def initialize_pictures(self):
        dictionary = {}
        pieces = ["Rook", "Knight", "Bishop", "King", "Queen", "Pawn"]
        colors = ["white", "black"]
        for piece, color in product(pieces, colors):
            picture = pygame.image.load('Pictures/' + color + piece + '.png')
            picture = pygame.transform.scale(picture, (self.tile_size, self.tile_size))
            dictionary[str(color) + str(piece)] = picture
        return dictionary
