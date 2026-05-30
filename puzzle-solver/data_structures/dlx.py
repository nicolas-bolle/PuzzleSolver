"""Implementation of Knuth's dancing links for Algorithm X
https://en.wikipedia.org/wiki/Dancing_Links
https://arxiv.org/abs/cs/0011047
"""

from abc import ABC, abstractmethod
from collections.abc import Iterator

import numpy as np

from data_structures.utils import (
    check_disjoint,
    check_distinct,
    check_overlap,
    check_subset,
)


class Node:
    """General node for the dancing links sparse matrix.
    Holds references to neighbors and the row/column nodes.
    """

    column: "ColNode"
    row: "RowNode"
    L: "Node"
    R: "Node"
    U: "Node"
    D: "Node"

    def __init__(self):
        self.column = None
        self.row = None
        self.L = self
        self.R = self
        self.U = self
        self.D = self


class RootNode:
    """Root node for the dancing links sparse matrix."""

    L: "ColNode"
    R: "ColNode"

    def __init__(self):
        self.L = self
        self.R = self


class ColNode:
    """Column node for the dancing links sparse matrix.
    Includes a name and number of elements in the column.
    """

    name: str
    size: int
    L: "ColNode"

    def __init__(self, name: str):
        self.name = name
        self.size = 0
        self.L = self
        self.R = self
        self.U = self
        self.D = self


class RowNode:
    """Row node for the dancing links sparse matrix.
    Just holds the name of the row.
    """

    name: str

    def __init__(self, name: str):
        self.name = name


class DLX(ABC):
    """Abstract class for dancing links solvers."""

    @abstractmethod
    def generate_solutions(self) -> Iterator[list[str]]:
        """Generate solutions to the dancing links problem as lists of row names."""
        pass


def _cover_col_node(col_node: ColNode):
    """Cover a column node by removing it from the columns linked list
    and removing each of its nodes from their row's linked list.
    """
    # cover in the column linked list
    col_node.R.L = col_node.L
    col_node.L.R = col_node.R

    # iterate through nodes in the column
    node = col_node.D
    while node != col_node:
        right_node = node.R

        # cover nodes in the row
        while right_node != node:
            right_node.D.U = right_node.U
            right_node.U.D = right_node.D
            right_node.column.size -= 1
            right_node = right_node.R

        node = node.D


def _uncover_col_node(col_node: ColNode):
    """Uncover a column node (inverse of _cover_col_node)."""
    # iterate through nodes in the column
    node = col_node.U
    while node != col_node:
        left_node = node.L

        # uncover nodes in the row
        while left_node != node:
            left_node.column.size += 1
            left_node.U.D = left_node
            left_node.D.U = left_node
            left_node = left_node.L

        node = node.U

    # uncover in the column linked list
    col_node.L.R = col_node
    col_node.R.L = col_node


class RowSparseGeneralizedDLX(DLX):
    """Core dancing links class.
    An instance and solver for the (generalized) exact cover problem.
    """

    # user dlx specification
    row_names: list[str]
    col_names_primary: list[str]
    col_names_secondary: list[str]
    entries: dict[str, list[str]]

    # internal vars for solving the problem
    _root_node: RootNode
    _partial_solution: list[str]

    def __init__(
        self,
        row_names: list[str],
        col_names_primary: list[str],
        col_names_secondary: list[str],
        entries: dict[str, list[str]],
    ):
        """Parameters
        row_names: row names
        col_names_primary: primary columns (must be achieved exactly once)
        col_names_secondary: secondary columns (can be achieved up to once)
        entries: row sparse specification of 1s in the matrix (keys are row names, values are lists of column names)
        """
        # types
        row_names = list(row_names)
        col_names_primary = list(col_names_primary)
        col_names_secondary = list(col_names_secondary)

        # ensure distinct names
        check_distinct(row_names)
        check_distinct(col_names_primary)
        check_distinct(col_names_secondary)

        # ensure primary and secondary cols don't overlap
        check_disjoint(col_names_primary, col_names_secondary)

        # ensure valid entries
        check_subset(
            subset=set(entries.keys()),
            superset=set(row_names),
        )
        check_subset(
            subset={
                col_name for col_names in entries.values() for col_name in col_names
            },
            superset=col_names_primary + col_names_secondary,
        )

        # ensure nontrivial rows (every row has at least one primary column)
        for col_names in entries.values():
            check_overlap(col_names, col_names_primary)

        self.row_names = row_names
        self.col_names_primary = col_names_primary
        self.col_names_secondary = col_names_secondary
        self.entries = entries

        self._root_node = None
        self._partial_solution = None

    def generate_solutions(self) -> Iterator[list[str]]:
        """Generate solutions to the specified exact cover problem.
        Solutions are lists of row names.
        """
        self._root_node = self._initialize_dlx(
            self.row_names,
            self.col_names_primary,
            self.col_names_secondary,
            self.entries,
        )
        self._partial_solution = []
        return self._search()

    @staticmethod
    def _initialize_dlx(
        row_names: list[str],
        col_names_primary: list[str],
        col_names_secondary: list[str],
        entries: dict[str, list[str]],
    ) -> RootNode:
        """Set up the DLX data structure of linked node objects."""
        # initialize root node and column nodes
        root_node = RootNode()
        col_nodes_primary_dict = {
            col_name: ColNode(col_name) for col_name in col_names_primary
        }
        col_nodes_secondary_dict = {
            col_name: ColNode(col_name) for col_name in col_names_secondary
        }
        col_nodes_dict = col_nodes_primary_dict | col_nodes_secondary_dict

        # insert just primary columns into the columns doubly linked list
        for col_node in col_nodes_primary_dict.values():
            root_node.L.R = col_node
            col_node.L = root_node.L
            col_node.R = root_node
            root_node.L = col_node

        # insert rows and nodes to create the system of doubly linked lists
        # note that rows are just labels and not included in any linked lists
        for row_name in row_names:
            row_node = RowNode(row_name)
            prev_node = None  # the most recent node added in this row

            # add a node for each entry in the row
            for col_name in entries[row_name]:
                col_node = col_nodes_dict[col_name]

                # create the node
                new_node = Node()
                if prev_node is None:
                    prev_node = new_node

                # row and column info of the node
                new_node.row = row_node
                new_node.column = col_node
                col_node.size += 1

                # insert the node into the column's linked list
                col_node.U.D = new_node
                new_node.U = col_node.U
                new_node.D = col_node
                col_node.U = new_node

                # insert into the row's linked list
                prev_node.L.R = new_node
                new_node.L = prev_node.L
                new_node.R = prev_node
                prev_node.L = new_node

                prev_node = new_node

        return root_node

    def _search(self):
        """Recursive step in the search for solutions."""

        # if the matrix has no columns then we have a solution
        # yield the solution and exit this leaf of the search
        if self.root_node.R == self.root_node:
            yield sorted(self._partial_solution.copy())
            return

        # pick and cover a column
        col_node = self._pick_column()
        _cover_col_node(col_node)

        # branch on the rows corresponding to this column
        node = col_node.D
        while node != col_node:
            self._partial_solution.append(node.row.name)

            # cover columns corresponding to this row
            right_node = node.R
            while right_node != node:
                _cover_col_node(right_node.column)
                right_node = right_node.R

            # recursive step
            yield from self._search()

            # uncover columns corresponding to this row
            left_node = node.L
            while left_node != node:
                _uncover_col_node(left_node.column)
                left_node = left_node.L

            # undo one step in the partial solution
            self._partial_solution.pop()

            # move on to the next node in the column
            node = node.D

        # uncover the column
        _uncover_col_node(col_node)

    def _pick_column(self):
        """Pick a column with the smallest number of 1s."""
        min_size = np.inf
        chosen_column = None
        col_node = self.root_node.R
        while col_node != self.root_node:
            if col_node.size < min_size:
                min_size = col_node.size
                chosen_column = col_node
            col_node = col_node.R
        return chosen_column


class ArrayDLX(RowSparseGeneralizedDLX):
    """Exact cover from an array."""

    A: np.ndarray
    row_names: list[str]
    col_names: list[str]
    A_secondary: np.ndarray
    col_names_secondary: list[str]

    def __init__(
        self,
        A: np.ndarray,
        row_names: list[str],
        col_names: list[str] = None,
        A_secondary: np.ndarray = None,
        col_names_secondary: list[str] = None,
    ):
        """Initialize the dancing links problem instance
        Parameters:
            A (np.ndarray): specifies (primary) constraints
            row_names (list[str]): optional list of strings for the row names
            col_names (list[str]): optional list of strings for the column names
            A_secondary (np.ndarray): optional secondary constraints
            col_names_secondary (list[str]): optional secondary column names
        """
        # defaults and types
        assert isinstance(A, np.ndarray), "A must be a np.ndarray"
        assert len(A.shape) == 2, "A must be two dimensional"
        A = A.astype("bool")
        n, m = A.shape

        if col_names is None:
            col_names = [f"primary_{i}" for i in range(m)]

        if A_secondary is None:
            A_secondary = np.zeros(shape=(n, 0), dtype=bool)
        assert isinstance(A_secondary, np.ndarray), "A_secondary must be a np.ndarray"
        assert len(A_secondary.shape) == 2, "A_secondary must be two dimensional"
        A_secondary = A_secondary.astype("bool")
        n_secondary, m_secondary = A_secondary.shape

        if col_names_secondary is None:
            col_names_secondary = [f"secondary_{i}" for i in range(m_secondary)]

        # dimension checks
        assert n == n_secondary, (
            f"A has {n} rows while A_secondary has {n_secondary} rows"
        )
        assert len(row_names) == n, f"{len(row_names)} rows specified, expected {n}"
        assert len(col_names) == m, f"{len(col_names)} columns specified, expected {m}"
        assert len(col_names_secondary) == m_secondary, (
            f"{len(col_names_secondary)} secondary columns specified, expected {m_secondary}"
        )

        self.A = A
        self.row_names = row_names
        self.col_names = col_names
        self.A_secondary = A_secondary
        self.col_names_secondary = col_names_secondary

        # convert to row sparse
        A_combined = np.concat((self.A, self.A_secondary), axis=1)
        col_names_combined_array = np.array(self.col_names + self.col_names_secondary)
        entries = {}
        for row_name, row in zip(self.row_names, A_combined, strict=True):
            col_idxs = np.where(row)[0]
            row_col_names = list(col_names_combined_array[col_idxs])
            entries[row_name] = row_col_names

        # parent init
        super().__init__(
            row_names=self.row_names,
            col_names_primary=self.col_names,
            col_names_secondary=self.col_names_secondary,
            entries=entries,
        )
