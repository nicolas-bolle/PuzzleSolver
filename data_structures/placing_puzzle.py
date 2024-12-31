"""Classes for making an exact cover formulation of general piece placing puzzles"""

from abc import ABC, abstractmethod
from collections.abc import Generator
from functools import total_ordering
from typing import Self, Type

from data_structures.dlx import DLX
from data_structures.utils import check_disjoint, check_distinct, check_subset


@total_ordering
class Item(ABC):
    """An item with a name used as its string representation and to determine equality/ordering
    Items are identified by their names, avoiding the need to ensure "exact" object equality
    """

    def __init__(self, name: str):
        self.name = str(name)

    def __str__(self):
        return self.name

    def __eq__(self, other: Self):
        return self.name == other.name

    def __lt__(self, other: Self):
        return self.name < other.name


class PlacingBoard(ABC):
    """Generic board for a placing puzzle
    At minimum holds references to
    - Pieces
        - Primary: that must be placed exactly once
        - Secondary: that can be placed either zero or one times
        - Tertiary: that can be placed any number of times (useful for "dummy" pieces)
    - Atoms
        - Primary: that must be filled exactly once
        - Secondary: that can be filled either zero or one times
    Uses an exact cover solver to solve the puzzle
    Subclass to specify puzzle specifics

    In the exact cover problem:
    - Each row is a placed piece
    - Each column is either an atom or a piece "key" column
    """

    # must be specified by the subclass
    SolutionClass: Type["PlacingSolution"]
    pieces_primary: list["PlacingPiece"]
    pieces_secondary: list["PlacingPiece"]
    pieces_tertiary: list["PlacingPiece"]
    atoms_primary: list["PlacingAtom"]
    atoms_secondary: list["PlacingAtom"]

    # used to set up and solve the exact cover problem
    row_names: list[str]
    col_names_primary: list[str]
    col_names_secondary: list[str]
    entries: dict[str, list[str]]
    rows_dict: dict[str, ("PlacingPiece", "PlacingPlacement")]
    dlx: DLX

    @abstractmethod
    def visualize(self):
        """Visualize the board"""
        pass

    def solutions(self) -> Generator["PlacingSolution", None, None]:
        """Generator for solutions to the exact cover problem"""
        # checks
        self._check_fields()

        # initialize vars for representing the exact cover problem
        self.row_names = []
        self.col_names_primary = []
        self.col_names_secondary = []
        self.entries = {}
        self.rows_dict = {}

        # populate
        for atom in self.atoms_primary:
            self._add_atom_primary(atom)
        for atom in self.atoms_secondary:
            self._add_atom_primary(atom)
        for piece in self.atoms_primary:
            self._add_piece_primary(piece)
        for piece in self.pieces_secondary:
            self._add_piece_secondary(piece)
        for piece in self.pieces_tertiary:
            self._add_piece_tertiary(piece)

        # solve
        self.dlx = DLX(
            self.row_names,
            self.col_names_primary,
            self.col_names_secondary,
            self.entries,
        )
        for dlx_solution in self.dlx.solutions():
            # generate solution objects
            yield self._dlx_to_placing_solution(dlx_solution)

    def _check_fields(self):
        """Data checks before formulating things as an exact cover problem"""
        # things are defined
        assert isinstance(self.pieces_primary, list)
        assert isinstance(self.pieces_secondary, list)
        assert isinstance(self.pieces_tertiary, list)
        assert isinstance(self.atoms_primary, list)
        assert isinstance(self.atoms_secondary, list)

        # types
        if self.pieces_primary:
            assert isinstance(self.pieces_primary[0], PlacingPiece)
        if self.pieces_secondary:
            assert isinstance(self.pieces_secondary[0], PlacingPiece)
        if self.pieces_tertiary:
            assert isinstance(self.pieces_tertiary[0], PlacingPiece)
        if self.atoms_primary:
            assert isinstance(self.atoms_primary[0], PlacingAtom)
        if self.atoms_secondary:
            assert isinstance(self.atoms_secondary[0], PlacingAtom)

        # distinctness
        check_distinct(self.pieces_primary)
        check_distinct(self.pieces_secondary)
        check_distinct(self.pieces_tertiary)
        check_distinct(self.atoms_primary)
        check_distinct(self.atoms_secondary)

        # disjointness
        check_disjoint(self.pieces_primary, self.pieces_secondary)
        check_disjoint(self.pieces_primary, self.pieces_tertiary)
        check_disjoint(self.pieces_secondary, self.pieces_tertiary)

        # non overlap between atoms and pieces
        check_disjoint(
            self.atoms_primary + self.atoms_secondary,
            self.pieces_primary + self.pieces_secondary + self.pieces_tertiary,
        )

        # check pieces use a subset of the valid atoms
        atoms = {}
        for piece in self.pieces_primary + self.pieces_secondary + self.pieces_tertiary:
            atoms.update(piece.get_atoms())
        check_subset(atoms, self.atoms_primary + self.atoms_secondary)
        # TODO cache getting atoms? since this check is inefficient

    def _add_atom_primary(self, atom: "PlacingAtom"):
        """Add a primary atom as a primary column"""
        self.col_names_primary.append(atom.name)

    def _add_atom_secondary(self, atom: "PlacingAtom"):
        """Add a secondary atom as a secondary column"""
        self.col_names_secondary.append(atom.name)

    def _add_piece_primary(self, piece: "PlacingPiece"):
        """Add a primary piece as one row for each placement plus a primary "key" column"""
        for placement in piece.get_placements():
            row_name = f"{piece.name}_{placement.name}"
            self.entries[row_name] = [
                atom.name for atom in piece.get_atoms(self, placement)
            ] + [piece.name]
            self.rows_dict[row_name] = (piece, placement)
            self.row_names.append(row_name)
        self.col_names_primary.append(piece.name)

    def _add_piece_secondary(self, piece: "PlacingPiece"):
        """Add a secondary piece as its atoms plus a secondary "key" column"""
        for placement in piece.get_placements():
            row_name = f"{piece.name}_{placement.name}"
            self.entries[row_name] = [
                atom.name for atom in piece.get_atoms(self, placement)
            ] + [piece.name]
            self.rows_dict[row_name] = (piece, placement)
            self.row_names.append(row_name)
        self.col_names_secondary.append(piece.name)

    def _add_piece_tertiary(self, piece: "PlacingPiece"):
        """Add a tertiary piece as its atoms (without a "key" column)"""
        for placement in piece.get_placements():
            row_name = f"{piece.name}_{placement.name}"
            self.entries[row_name] = [
                atom.name for atom in piece.get_atoms(self, placement)
            ]
            self.rows_dict[row_name] = (piece, placement)
            self.row_names.append(row_name)

    def _dlx_to_placing_solution(self, row_names: list[str]) -> "PlacingSolution":
        """Convert a list of row names to a PlacingSolution object"""
        placed_pieces = [self.rows_dict[row_name] for row_name in row_names]
        return self.SolutionClass(self, placed_pieces)


class PlacingAtom(Item, ABC):
    """Generic atom for a placing puzzle
    The most basic placement puzzle element: what would be a column in an exact cover problem
    Subclass to specify puzzle specifics
    """


class PlacingPlacement(Item, ABC):
    """Generic piece placement for a placing puzzle
    Subclass to specify puzzle specifics
    """


class PlacingPiece(Item, ABC):
    """Generic piece for a placing puzzle
    Subclass to specify puzzle specifics
    """

    @abstractmethod
    def get_placements(self, board: PlacingBoard) -> list[PlacingPlacement]:
        """Return a list of valid placements"""

    @abstractmethod
    def get_atoms(
        self, board: PlacingBoard, placement: PlacingPlacement
    ) -> list[PlacingAtom]:
        """Return a list of atoms when the piece is placed at the given Placement"""


class PlacingSolution(ABC):
    """Solution for a placing puzzle
    Just a collection of pieces with placements on a board
    Subclass to implement visualization
    """

    def __init__(
        self,
        board: PlacingBoard,
        placed_pieces: list[tuple[PlacingPiece, PlacingPlacement]],
    ):
        self.board = board
        self.placed_pieces = placed_pieces
        self._check_valid()

    def _check_valid(self):
        """Check the solution is valid"""
        # check placements are valid
        for piece, placement in self.placed_pieces:
            assert placement in piece.get_placements()

        # check primary/secondary atom constraints
        atoms = []
        for piece, placement in self.placed_pieces:
            atoms.extend(piece.get_atoms())
        check_distinct(atoms)
        check_subset(atoms, self.board.atoms_primary + self.board.atoms_secondary)
        check_subset(self.board.atoms_primary, atoms)

        # check primary/secondary piece constraints
        pieces = [piece for piece, _ in self.placed_pieces]
        check_distinct(pieces)
        check_subset(pieces, self.board.pieces_primary + self.board.pieces_secondary)
        check_subset(self.board.pieces_primary, pieces)

    @abstractmethod
    def visualize(self):
        """Visualize the solution"""
