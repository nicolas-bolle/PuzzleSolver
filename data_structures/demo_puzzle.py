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
        GridSmallLPiece("L", "tab:blue"),
        GridTPiece("T", "tab:orange"),
        GridTwoPiece("I", "tab:gray"),
    ]
    pieces_secondary = []
    pieces_tertiary = []


class Demo2GridBoard(GridBoard):
    """3x3 demo board (difficulty level impossible)"""

    N = 3
    M = 3
    pieces_primary = [
        GridSmallLPiece("L", "tab:blue"),
        GridTPiece("T", "tab:orange"),
        GridThreePiece("I", "tab:gray"),
    ]
    pieces_secondary = []
    pieces_tertiary = []


class Demo3GridBoard(GridBoard):
    """4x3 demo board"""

    N = 4
    M = 3
    pieces_primary = [
        GridSmallLPiece("L", "tab:blue"),
        GridTPiece("T", "tab:orange"),
        GridTwoPiece("2", "tab:gray"),
        GridThreePiece("3", "tab:green"),
    ]
    pieces_secondary = []
    pieces_tertiary = []
