"""Classes for making puzzles on square grids"""

from abc import ABC

import numpy as np

from data_structures.placing_puzzle import (
    PlacingAtom,
    PlacingBoard,
    PlacingPiece,
    PlacingPlacement,
    PlacingSolution,
)


class GridSquare(PlacingAtom):
    """A square on a board"""

    def __init__(self, i: int, j: int):
        self.i = i
        self.j = j
        name = f"square_{self.i}_{self.j}"
        super().__init__(name)


ORIENTATIONS = ("U", "R", "D", "L", "FU", "FR", "FD", "FL")


class GridPlacement(PlacingPlacement):
    """Grid piece placement given as the location plus the rotation/flip
    It's up to the piece if it wants to mod out the rotation/flip by its symmetries
    """

    def __init__(self, i: int, j: int, orientation: str):
        assert orientation in ORIENTATIONS
        self.i = i
        self.j = j
        self.orientation = orientation
        name = f"placement_{self.i}_{self.j}_{self.orientation}"
        super().__init__(name)


class GridPiece(PlacingPiece):
    """Generic Tetris-like piece"""

    # relative coords of the parts of the piece
    coords: list[tuple[int, int]]

    # used to make sure all pieces are distinct
    piece_id: str

    # for visualizing
    piece_color: str

    coords: list[tuple]
    coords_array: np.ndarray

    def __init__(self, piece_id: str, piece_color: str, coords: list[tuple[int, int]]):
        self.piece_id = piece_id
        self.piece_color = piece_color
        self.coords = coords
        self.coords_array = np.array(self.coords, dtype=int).transpose()
        name = f"piece-{self.piece_id}"
        super().__init__(name)

    def get_placements(self, board: "GridBoard") -> list[GridPlacement]:
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
                    placement = GridPlacement(i, j, orientation)
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
        self, board: "GridBoard", placement: GridPlacement
    ) -> list[GridSquare]:
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

        return [GridSquare(i, j) for i, j in coords_array.transpose()]

    def visualize(self):
        """Print out a visualization"""
        # transform the coordinates array so i,j>=0 and i=0 is the first thing we want to print
        smallest_i = self.coords_array[0, :].min()
        largest_j = self.coords_array[1, :].max()
        coords_transformed = list(
            zip(
                largest_j - self.coords_array[1, :],
                self.coords_array[0, :] - smallest_i,
            )
        )

        # put into an array
        n = max(i for i, _ in coords_transformed)
        m = max(j for _, j in coords_transformed)
        str_array = np.full(shape=(n, m), fill_value="  ", dtype=str)
        for i, j in coords_transformed:
            str_array[i, j] = "[]"

        # print
        for row in str_array:
            print("".join(row))


class GridSmallLPiece(GridPiece):
    """Small L-shaped piece"""

    def __init__(self, piece_id: str, piece_color: str):
        coords = [(0, 0), (1, 0), (0, 1)]
        super().__init__(piece_id, piece_color, coords)


class GridBigLPiece(GridPiece):
    """Big L-shaped piece"""

    def __init__(self, piece_id: str, piece_color: str):
        coords = [(0, 0), (1, 0), (0, 1), (0, 2)]
        super().__init__(piece_id, piece_color, coords)


class GridTPiece(GridPiece):
    """T-shaped piece"""

    def __init__(self, piece_id: str, piece_color: str):
        coords = [(0, 0), (-1, 0), (1, 0), (0, -1)]
        super().__init__(piece_id, piece_color, coords)


class GridTwoPiece(GridPiece):
    """Two adjacent squares piece"""

    def __init__(self, piece_id: str, piece_color: str):
        coords = [(0, 0), (1, 0)]
        super().__init__(piece_id, piece_color, coords)


class GridThreePiece(GridPiece):
    """Three squares in a line piece"""

    def __init__(self, piece_id: str, piece_color: str):
        coords = [(-1, 0), (0, 0), (1, 0)]
        super().__init__(piece_id, piece_color, coords)


class GridFourPiece(GridPiece):
    """Four squares in a line piece"""

    def __init__(self, piece_id: str, piece_color: str):
        coords = [(-1, 0), (0, 0), (1, 0), (2, 0)]
        super().__init__(piece_id, piece_color, coords)


class GridSolution(PlacingSolution):
    """A solution on the grid board"""

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

        # TODO but how do I visualize solutions??


class GridBoard(PlacingBoard, ABC):
    """A basic n x m square board abstract class"""

    SolutionClass = GridSolution
    atoms_primary: list[GridSquare]
    atoms_secondary = []

    # must specify in subclass
    N: int
    M: int
    pieces_primary: list[GridPiece]
    pieces_secondary: list[GridPiece]
    pieces_tertiary: list[GridPiece]

    def __init__(self):
        self.atoms_primary = [
            GridSquare(i, j) for i in range(self.N) for j in range(self.M)
        ]

    def visualize(self):
        """Visualize the board"""
        print(f"{self.N} x {self.M} Grid board")
        for _ in range(self.M):
            print("." * self.N)

        print()
        if self.pieces_primary:
            print("Primary pieces")
            for piece in self.pieces_primary:
                piece.visualize()
        else:
            print("No primary pieces")

        print()
        if self.pieces_secondary:
            print("Secondary pieces")
            for piece in self.pieces_secondary:
                piece.visualize()
        else:
            print("No secondary pieces")

        print()
        if self.pieces_tertiary:
            print("Tertiary pieces")
            for piece in self.pieces_tertiary:
                piece.visualize()
        else:
            print("No tertiary pieces")
