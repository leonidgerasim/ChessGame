import os
import pygame

class Piece:
    colors_notations_and_values = {
        "w": {
            "p": 1,
            "n": 3,
            "b": 3,
            "r": 5,
            "q": 9,
            "k": 90
        },
        "b": {
            "p": -1,
            "n": -3,
            "b": -3,
            "r": -5,
            "q": -9,
            "k": -90
        }
    }

    def __init__(self, name, notation, color, skin_directory="skins/default", is_captured=False) -> None:
        self.name = name
        self.__notation = notation
        self.color = color
        self.skin_directory = skin_directory
        self.set_is_captured(is_captured)

        self.value = self.get_piece_value()

    def get_piece_value(self):
        return Piece.colors_notations_and_values[self.color][self.__notation.lower()]

    def get_piece_color_based_on_notation(notation) -> str:
        """
        The chess module displays black pieces' notations in lowercase and white in uppercase, so we can get the color based on this
        """
        return "w" if notation.isupper() else "b"

    def get_value_from_notation(notation: str, color: str) -> int:
        """
        A class method that gets the corresponding value for a particular notation and color
        """
        return Piece.colors_notations_and_values[color][notation.lower()]

    def set_is_captured(self, is_captured: bool):
        self.__is_captured = bool(is_captured)

    def get_image_path(self):
        """
        Gets the path to the image of the piece based on its notation and
        whether or not it has been captured
        """
        if not self.__is_captured:
            path = os.path.join(self.skin_directory, self.color, f"{self.__notation.lower()}.png")
        else:
            path = os.path.join(self.skin_directory, self.color, "captured", f"{self.__notation.lower()}.png")

        return path

    def get_image(self):
        """
        Returns a pygame image object from the piece's corresponding image path
        """
        image_path = self.get_image_path()

        if os.path.exists(image_path):
            return pygame.image.load(image_path)
        else:
            raise FileNotFoundError(f"The image was not found in the {image_path}")

    def __str__(self):
        return f"{self.__notation} {self.color}"

    def get_notation(self) -> str:
        """
        Returns the notation of the piece, (pawns' notations are empty strings)
        """
        if self.__notation != 'p':
            return self.__notation.upper()

        return ''

    def __set_notation(self, notation):
        self.__notation = notation

    def promote(self, notation: str):
        """
        Promotes this piece to a piece with the notation notation.
        It is important to note that promotion does not increase the piece's value,
        just its capabilities
        """
        if self.__notation.lower() != "p":
            raise ValueError("Cannot promote a piece other than a pawn")

        if notation not in ["q", "r", "n", "b"]:
            raise ValueError("Can only promote to queen, rook, bishop or knight pieces")
        self.__set_notation(notation)
