"""A simple demo puzzle of fitting a few blocks into a square grid"""

import numpy as np

from data_structures.placing_puzzle import (
    PlacingAtom,
    PlacingBoard,
    PlacingPiece,
    PlacingPlacement,
    PlacingSolution,
)


class DemoSquare(PlacingAtom):
    """A square on a board"""

    def __init__(self, i: int, j: int):
        self.i = i
        self.j = j
        name = f"square_{self.i}_{self.j}"
        super().__init__(name)


ORIENTATIONS = ("U", "R", "D", "L", "FU", "FR", "FD", "FL")


class DemoPlacement(PlacingPlacement):
    """Demo piece placement given as the location plus the rotation/flip
    It's up to the piece if it wants to mod out the rotation/flip by its symmetries
    """

    def __init__(self, i: int, j: int, orientation: str):
        assert orientation in ORIENTATIONS
        self.i = i
        self.j = j
        self.orientation = orientation
        name = f"placement_{self.i}_{self.j}_{self.orientation}"
        super().__init__(name)


class DemoPiece(PlacingPiece):
    """Generic Tetris-like piece"""

    # relative coords of the parts of the piece
    coords: list[tuple[int, int]]

    # used to make sure all pieces are distinct
    piece_id: str

    @property
    def coords_array(self):
        """Numpy array of the coords, with 2 rows"""
        return np.array(self.coords, dtype=int).transpose()

    def get_placements(self, board: "DemoBoard") -> list[DemoPlacement]:
        """Given the board, return all valid placements of this piece"""
        # TODO inefficient, could be worth trying to improve this
        r = int(self.coords_array.max())

        # the atoms on the board
        expected_atoms = set(board.atoms_primary)

        # list of the placements we end up going with
        placements = []

        # a record of the atoms they use, so we don't generate duplicate ones due to symmetries
        placements_history = set()

        # iterate over potential placements
        for i in range(-r, board.N + r):
            for j in range(-r, board.N + r):
                for orientation in ORIENTATIONS:
                    placement = DemoPlacement(i, j, orientation)
                    atoms = self.get_atoms(board, placement)
                    # if the placement keeps us on the board, it's valid
                    if not set(atoms) - expected_atoms:
                        # check we haven't seen it already
                        atoms = tuple(sorted(atom.name for atom in atoms))
                        if atoms not in placements_history:
                            placements_history.add(atoms)
                            placements.append(placement)

        return placements

    def get_atoms(
        self, board: "DemoBoard", placement: DemoPlacement
    ) -> list[DemoSquare]:
        """Return a list of atoms when the piece is placed at the given Placement"""
        coords_array = self.coords_array

        # i axis flip
        if placement.orientation[0] == "F":
            coords_array = np.array([[-1, 0], [0, 1]], dtype=int) @ coords_array

        # rotations
        key = placement.orientation[-1]
        match key:
            case "U":
                pass
            case "R":
                coords_array = np.array([[0, 1], [-1, 0]], dtype=int) @ coords_array
            case "D":
                coords_array = np.array([[-1, 0], [0, -1]], dtype=int) @ coords_array
            case "L":
                coords_array = np.array([[0, -1], [1, 0]], dtype=int) @ coords_array

        # translation
        n = len(self.coords)
        coords_array = coords_array + np.array([[placement.i] * n, [placement.j] * n])

        return [DemoSquare(i, j) for i, j in coords_array.transpose()]


class DemoLPiece(DemoPiece):
    """L-shaped piece"""

    coords = [(0, 0), (1, 0), (0, 1)]

    def __init__(self, piece_id: str):
        self.piece_id = piece_id
        name = f"L-piece-{self.piece_id}"
        super().__init__(name)


class DemoTPiece(DemoPiece):
    """T-shaped piece"""

    coords = [(0, 0), (-1, 0), (1, 0), (0, -1)]

    def __init__(self, piece_id: str):
        self.piece_id = piece_id
        name = f"T-piece-{self.piece_id}"
        super().__init__(name)


class DemoIPiece(DemoPiece):
    """I-shaped piece"""

    coords = [(0, 0), (0, 1)]

    def __init__(self, piece_id: str):
        self.piece_id = piece_id
        name = f"I-piece-{self.piece_id}"
        super().__init__(name)


class DemoSolution(PlacingSolution):
    """A solution on the demo board"""

    def visualize(self):
        """Visualize the solution"""
        assert len(self.placed_pieces) == 3
        A = np.zeros(shape=(3, 3), dtype="str")
        for piece, placement in self.placed_pieces:
            assert len(piece.piece_id) == 1
            for atom in piece.get_atoms(self.board, placement):
                A[atom.i, atom.j] = piece.piece_id
        A = A.transpose()[::-1, :]
        for row in A:
            print("".join(row))


class DemoBoard(PlacingBoard):
    """A basic 3x3 board"""

    N = 3

    SolutionClass = DemoSolution
    pieces_primary = [DemoLPiece("L"), DemoTPiece("T"), DemoIPiece("I")]
    pieces_secondary = []
    pieces_tertiary = []
    atoms_primary: list[DemoSquare]
    atoms_secondary = []

    def __init__(self):
        self.atoms_primary = [
            DemoSquare(i, j) for i in range(self.N) for j in range(self.N)
        ]

    def visualize(self):
        """Visualize the board"""
        print("...")
        print("...")
        print("...")
        print()
        print([str(piece) for piece in self.pieces_primary])
