"""The puzzle in the game Kanoodle
https://www.educationalinsights.com/shop/collections/kanoodle
"""

from data_structures.grid_puzzle import GridBoard, GridPiece


class KanoodlePieceA(GridPiece):
    """Orange piece A"""

    def __init__(self):
        piece_id = "Orange (A)"
        piece_color = "tab:orange"
        coords = [(0, 0), (1, 0), (1, 1), (1, 2)]
        super().__init__(piece_id, piece_color, coords)


class KanoodlePieceB(GridPiece):
    """Red piece B"""

    def __init__(self):
        piece_id = "Red (B)"
        piece_color = "tab:red"
        coords = [(0, 0), (0, 1), (1, 0), (1, 1), (1, 2)]
        super().__init__(piece_id, piece_color, coords)


class KanoodlePieceC(GridPiece):
    """Dark blue piece C"""

    def __init__(self):
        piece_id = "Dark blue (C)"
        piece_color = "mediumblue"
        coords = [(0, 0), (1, 0), (1, 1), (1, 2), (1, 3)]
        super().__init__(piece_id, piece_color, coords)


class KanoodlePieceD(GridPiece):
    """Light pink piece D"""

    def __init__(self):
        piece_id = "Light pink (D)"
        piece_color = "lightpink"
        coords = [(0, 1), (1, 0), (1, 1), (1, 2), (1, 3)]
        super().__init__(piece_id, piece_color, coords)


class KanoodlePieceE(GridPiece):
    """Dark green piece E"""

    def __init__(self):
        piece_id = "Dark green (E)"
        piece_color = "darkgreen"
        coords = [(0, 0), (0, 1), (1, 1), (1, 2), (1, 3)]
        super().__init__(piece_id, piece_color, coords)


class KanoodlePieceF(GridPiece):
    """White piece F"""

    def __init__(self):
        piece_id = "White (F)"
        piece_color = "whitesmoke"
        coords = [(0, 0), (1, 0), (1, 1)]
        super().__init__(piece_id, piece_color, coords)


class KanoodlePieceG(GridPiece):
    """Light blue piece G"""

    def __init__(self):
        piece_id = "Light blue (G)"
        piece_color = "lightblue"
        coords = [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)]
        super().__init__(piece_id, piece_color, coords)


class KanoodlePieceH(GridPiece):
    """Pink piece H"""

    def __init__(self):
        piece_id = "Pink (H)"
        piece_color = "hotpink"
        coords = [(0, 0), (1, 0), (1, 1), (2, 1), (2, 2)]
        super().__init__(piece_id, piece_color, coords)


class KanoodlePieceI(GridPiece):
    """Yellow piece I"""

    def __init__(self):
        piece_id = "Yellow (I)"
        piece_color = "gold"
        coords = [(0, 0), (0, 1), (1, 0), (2, 0), (2, 1)]
        super().__init__(piece_id, piece_color, coords)


class KanoodlePieceJ(GridPiece):
    """Purple piece J"""

    def __init__(self):
        piece_id = "Purple (J)"
        piece_color = "rebeccapurple"
        coords = [(0, 0), (0, 1), (0, 2), (0, 3)]
        super().__init__(piece_id, piece_color, coords)


class KanoodlePieceK(GridPiece):
    """Light green piece K"""

    def __init__(self):
        piece_id = "Light green (K)"
        piece_color = "xkcd:acid green"
        coords = [(0, 0), (0, 1), (1, 0), (1, 1)]
        super().__init__(piece_id, piece_color, coords)


class KanoodlePieceL(GridPiece):
    """Gray piece L"""

    def __init__(self):
        piece_id = "Gray (L)"
        piece_color = "darkgray"
        coords = [(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)]
        super().__init__(piece_id, piece_color, coords)


class Kanoodle(GridBoard):
    """Kanoodle board with its 12 pieces"""

    N = 11
    M = 5
    pieces_primary = [
        KanoodlePieceA(),
        KanoodlePieceB(),
        KanoodlePieceC(),
        KanoodlePieceD(),
        KanoodlePieceE(),
        KanoodlePieceF(),
        KanoodlePieceG(),
        KanoodlePieceH(),
        KanoodlePieceI(),
        KanoodlePieceJ(),
        KanoodlePieceK(),
        KanoodlePieceL(),
    ]
    pieces_secondary = []
    pieces_tertiary = []
