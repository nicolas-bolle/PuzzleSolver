"""Implementation of Knuth's dancing links technique for Algorithm X
https://en.wikipedia.org/wiki/Dancing_Links

Used Chat GPT for the first draft of the code
"""

# pylint: disable=invalid-name

from collections.abc import Generator

import numpy as np

from data_structures.utils import check_disjoint, check_distinct, check_subset


class Node:
    """General node for the dancing links sparse matrix
    Holds references to neighbors and the row/column nodes
    """

    def __init__(self):
        self.column = None
        self.row = None
        self.L = self
        self.R = self
        self.U = self
        self.D = self


class RootNode:
    """Root node for the dancing links sparse matrix"""

    def __init__(self):
        self.L = self
        self.R = self


class ColNode:
    """Column node for the dancing links sparse matrix
    Includes a name and number of elements in the column
    """

    def __init__(self, name):
        self.name = name
        self.size = 0
        self.L = self
        self.R = self
        self.U = self
        self.D = self


class RowNode:
    """Row node for the dancing links sparse matrix
    Just holds the name of the row
    """

    def __init__(self, name):
        self.name = name


class DLX:
    """Solves an instance of the (generalized) exact cover problem
        using the dancing links technique for implementing Algorithm X
    The problem is specified via a row-first sparse representation
    https://en.wikipedia.org/wiki/Dancing_Links
    https://arxiv.org/abs/cs/0011047
    """

    row_names: list[str]
    col_names_primary: list[str]
    col_names_secondary: list[str]
    entries: dict[str, list[str]]

    root_node: RootNode

    partial_solution: list[str]

    def __init__(
        self,
        row_names: list[str],
        col_names_primary: list[str],
        col_names_secondary: list[str],
        entries: dict[str, list[str]],
    ):
        """Parameters
        row_names: row names
        col_names_primary: primary columns (must be achieved once)
        col_names_secondary: secondary columns (can be achieved up to once)
        entries: keys are row names, values are the column names with entries

        Names can also be ints, tuples, really anything hashable
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

        # ensure distinct entries
        check_distinct(entries)

        # ensure valid entries
        check_subset(
            subset=set(entries.keys()),
            superset=set(row_names),
        )
        check_subset(
            subset={
                col_name for col_names in entries.values() for col_name in col_names
            },
            superset=set(col_names_primary + col_names_secondary),
        )

        # set fields
        self.row_names = row_names
        self.col_names_primary = col_names_primary
        self.col_names_secondary = col_names_secondary
        self.entries = entries

        # set up the DLX problem
        self.root_node = self._initialize_dlx(
            row_names, col_names_primary, col_names_secondary, entries
        )

        self._partial_solution = []

    @staticmethod
    def _initialize_dlx(
        row_names: list[str],
        col_names_primary: list[str],
        col_names_secondary: list[str],
        entries: dict[str, list[str]],
    ) -> RootNode:
        """Set up the DLX data structure of Node objects"""

        # initialize root node and all column nodes
        root_node = RootNode()
        col_nodes_dict_primary = {
            col_name: ColNode(col_name) for col_name in col_names_primary
        }
        col_nodes_dict_secondary = {
            col_name: ColNode(col_name) for col_name in col_names_secondary
        }
        col_nodes_dict = col_nodes_dict_primary | col_nodes_dict_secondary

        # insert just primary columns into the columns doubly linked list
        for col_node in col_nodes_dict_primary.values():
            root_node.L.R = col_node
            col_node.L = root_node.L
            col_node.R = root_node
            root_node.L = col_node

        # insert nodes into the system of doubly linked lists
        for row_name in row_names:
            row_node = RowNode(row_name)
            prev_node = None  # the "previous node" in the row

            # iterate through entries in the row to add nodes
            for col_name in entries[row_name]:
                col_node = col_nodes_dict[col_name]

                # create node
                new_node = Node()
                if prev_node is None:
                    prev_node = new_node

                # row and column info of the node
                new_node.row = row_node
                new_node.column = col_node
                col_node.size += 1

                # insert into the column's linked list
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

    def solutions(self) -> Generator[list[str], None, None]:
        """Generator for solutions to the specified exact cover problem"""
        assert isinstance(self.root_node, RootNode)
        self._partial_solution = []
        return self._search()

    def _search(self):
        """Recursive step in the search for solutions"""

        # if the matrix has no columns, yield the solution and stop recursing
        if self.root_node.R == self.root_node:
            yield self._partial_solution.copy()
            return

        # pick and cover the column
        col_node = self._choose_column()
        self._cover(col_node)

        # branching on the rows corresponding to this column
        node = col_node.D
        while node != col_node:
            self._partial_solution.append(node.row.name)

            # cover columns corresponding to this row
            right_node = node.R
            while right_node != node:
                self._cover(right_node.column)
                right_node = right_node.R

            # recursive step
            yield from self._search()

            # uncover columns corresponding to this row
            left_node = node.L
            while left_node != node:
                self._uncover(left_node.column)
                left_node = left_node.L

            self._partial_solution.pop()
            node = node.D

        # uncover the column
        self._uncover(col_node)

    def _choose_column(self):
        """Pick the column with the smallest number of 1s"""
        min_size = np.inf
        chosen_column = None
        col_node = self.root_node.R
        while col_node != self.root_node:
            if col_node.size < min_size:
                min_size = col_node.size
                chosen_column = col_node
            col_node = col_node.R
        return chosen_column

    def _cover(self, col_node):
        """Cover a column node"""
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

    def _uncover(self, col_node):
        """Uncover a column node"""
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


class ArrayDLX(DLX):
    """Exact cover from an array"""

    A: np.ndarray
    row_names: list[str]
    col_names: list[str]
    A_secondary: np.ndarray
    col_names_secondary: list[str]

    def __init__(
        self,
        A: np.ndarray,
        row_names: list[str] = None,
        col_names: list[str] = None,
        A_secondary: np.ndarray = None,
        col_names_secondary: np.ndarray = None,
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
        assert isinstance(A, np.ndarray)
        assert len(A.shape) == 2
        A = A.astype("bool")
        n, m = A.shape

        if row_names is None:
            row_names = [str(x) for x in range(n)]

        if col_names is None:
            col_names = [str(x) for x in range(m)]

        if A_secondary is None:
            A_secondary = np.zeros(shape=(n, 0), dtype=bool)
        assert isinstance(A_secondary, np.ndarray)
        assert len(A_secondary.shape) == 2
        A_secondary = A_secondary.astype("bool")
        n_secondary, m_secondary = A_secondary.shape

        if col_names_secondary is None:
            col_names_secondary = [str(x + m) for x in range(m_secondary)]

        # dimension checks
        assert len(row_names) == n
        assert len(col_names) == m
        assert n == n_secondary
        assert len(col_names_secondary) == m_secondary

        # set fields
        self.A = A
        self.row_names = row_names
        self.col_names = col_names
        self.A_secondary = A_secondary
        self.col_names_secondary = col_names_secondary

        # determine sparse row-first format entries
        A_combined = np.concat((self.A, self.A_secondary), axis=1)
        col_names_combined_array = np.array(self.col_names + self.col_names_secondary)
        entries = {}
        for row_name, row in zip(self.row_names, A_combined):
            col_idxs = np.where(row)[0]
            row_col_names = list(col_names_combined_array[col_idxs])
            entries[row_name] = row_col_names

        # init using the sparse format
        super().__init__(
            row_names=self.row_names,
            col_names_primary=self.col_names,
            col_names_secondary=self.col_names_secondary,
            entries=entries,
        )
