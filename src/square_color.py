from enum import Enum


class SquareColor(Enum):
    WHITE = 0
    BLACK = 1
    EMPTY = 2


class PieceColor(Enum):
    WHITE = SquareColor.WHITE
    BLACK = SquareColor.BLACK
