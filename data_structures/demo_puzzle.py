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


class Demo4GridBoard(GridBoard):
    """3x2 demo board with secondary pieces"""

    N = 3
    M = 2
    pieces_primary = []
    pieces_secondary = [
        GridBigLPiece("L", "tab:red"),
        GridTwoPiece("2", "tab:orange"),
        GridSmallLPiece("l.1", "tab:olive"),
        GridSmallLPiece("l.2", "tab:green"),
        GridThreePiece("3.1", "tab:blue"),
        GridThreePiece("3.2", "tab:purple"),
        GridFourPiece("4", "tab:pink"),
    ]
    pieces_tertiary = []


class Demo5GridBoard(GridBoard):
    """3x2 demo board with tertiary pieces"""

    N = 3
    M = 2
    pieces_primary = []
    pieces_secondary = []
    pieces_tertiary = [
        GridTwoPiece("2", "tab:blue"),
    ]
