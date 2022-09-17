import string
import pygame

from Settings import Settings


class Square:
    def __init__(self, x: int, y: int, tile_color: str, settings: Settings):
        self.x = x  # index
        self.y = y  # index
        self.tile_color = tile_color
        self.piece = None
        # top left pixel from the top of the board
        self.x_coordinate = (7 - x) * settings.tile_size if settings.player_color else x * settings.tile_size
        # top left pixel from the left side of the board
        self.y_coordinate = (7 - y) * settings.tile_size if settings.player_color else y * settings.tile_size
        self.letter = list(string.ascii_uppercase)[x]  # A-H tile letter
        self.number = y + 1  # 1-8 tile number

    def __str__(self) -> str:
        if self.piece is not None:
            return str(self.letter) + str(self.number) + ", " + \
                   str(self.tile_color) + " tile with " + self.piece.color + " " + self.piece.name
        else:
            return str(self.letter) + str(self.number) + ", " + str(self.tile_color) + " tile, empty"

    # Display or refresh the tile
    def display_tile(self, screen, settings):
        if self.tile_color == "white":
            pygame.draw.rect(screen, pygame.Color(252, 230, 201),
                             (self.x_coordinate, self.y_coordinate, settings.tile_size, settings.tile_size),
                             # left, top, width, height
                             border_radius=0)
        else:
            pygame.draw.rect(screen, pygame.Color(138, 54, 15),
                             (self.x_coordinate, self.y_coordinate, settings.tile_size, settings.tile_size),
                             # left, top, width, height
                             border_radius=0)

    # Display or refresh the pieces
    def display_piece(self, screen, settings):
        screen.blit(settings.dict_of_pictures[str(self.piece.color) + str(self.piece.name)], (self.x_coordinate, self.y_coordinate))
