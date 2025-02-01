"""Some simple demo grid puzzles"""

from data_structures.grid_puzzle import (
    GridBigLPiece,
    GridBoard,
    GridFourPiece,
    GridSmallLPiece,
    GridThreePiece,
    GridTPiece,
    GridTwoPiece,
)


class Demo1GridBoard(GridBoard):
    """3x3 demo board"""

    N = 3
    M = 3
    pieces_primary = [
        GridSmallLPiece("L", "blue"),
        GridTPiece("T", "orange"),
        GridTwoPiece("I", "black"),
    ]
    pieces_secondary = []
    pieces_tertiary = []


class Demo2GridBoard(GridBoard):
    """3x3 demo board (difficulty level impossible)"""

    N = 3
    M = 3
    pieces_primary = [
        GridSmallLPiece("L", "blue"),
        GridTPiece("T", "orange"),
        GridThreePiece("I", "black"),
    ]
    pieces_secondary = []
    pieces_tertiary = []
