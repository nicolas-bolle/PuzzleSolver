"""Implementation of Knuth's dancing links technique for Algorithm X
https://en.wikipedia.org/wiki/Dancing_Links

Used Chat GPT for the first draft of the code
See the end of the file for a sample run
"""

# TODO make requirements.txt (and venv)

import numpy as np


class Node:
    """General node for the dancing links sparse matrix
    Holds references to neighbors and the row/column nodes
    """
    def __init__(self):
        self.L = self
        self.R = self
        self.U = self
        self.D = self
        self.column = None
        self.row = None


class RootNode:
    """Root node for the dancing links sparse matrix"""
    def __init__(self):
        self.L = self
        self.R = self


class ColumnNode(Node):
    """Column node for the dancing links sparse matrix
    Includes a name and number of elements in the column
    """
    def __init__(self, name):
        super().__init__()
        self.column = self
        self.name = name
        self.size = 0


class RowNode:
    """Row node for the dancing links sparse matrix
    Just holds the name of the row
    """
    def __init__(self, name):
        self.name = name


class DLX:
    """Creates and solves an instance of the (generalized) exact cover problem
        using the dancing links technique for implementing Algorithm X
    https://en.wikipedia.org/wiki/Dancing_Links
    https://arxiv.org/abs/cs/0011047
    """

    root: RootNode
    
    def __init__(
            self,
            A_primary: np.array,
            A_secondary: np.array,
            row_names: list = None,
            column_names: list = None,
        ):
        """Initialize the dancing links problem instance
            Parameters:
                A_primary (np.ndarray): specifies primary constraints
                A_secondary (np.ndarray): specifies secondary constraints
                row_names (list[str]): optional list of strings for the row names
                column_names (list[str]): optional list of strings for the column names
        TODO ensure we can initialize with a sparse array, maybe use scipy sparse stuff to do the math
        """
        # clean and check inputs
        assert isinstance(A_primary, np.ndarray)
        assert len(A_primary.shape) == 2
        A_primary = A_primary.astype('bool')
        assert isinstance(A_secondary, np.ndarray)
        assert len(A_secondary.shape) == 2
        A_secondary = A_secondary.astype('bool')
        assert len(A_primary) == len(A_secondary)
        A = np.concat((A_primary, A_secondary), axis=1)
        n, m = A.shape
        if row_names is None:
            row_names = [str(x) for x in range(n)]
        if column_names is None:
            column_names = [str(x) for x in range(m)]
        assert len(row_names) == n, 'Length of row_names does not match the array dimensions'
        assert len(column_names) == m, 'Length of column_names does not match the array dimensions'
        num_primary = A_primary.shape[1]

        # create the sparse linked array
        self.root = self._create_linked_array(A, num_primary, row_names, column_names)

    def _create_linked_array(self, A: np.ndarray, num_primary: int, row_names: list[str], column_names: list[str]) -> RootNode:
        """Utility to create the linked array using Node objects"""
        
        # initialize root node and column nodes
        root = RootNode()
        column_nodes = [ColumnNode(column_name) for column_name in column_names]

        # insert just primary columns into the columns doubly linked list
        for column_node in column_nodes[:num_primary]:
            root.L.R = column_node
            column_node.L = root.L
            column_node.R = root
            root.L = column_node

        # insert nodes into the system of doubly linked lists
        for i, row_name in enumerate(row_names):
            row_node = RowNode(row_name)
            prev_node = None  # the "previous node" in the row
            for j, column_node in enumerate(column_nodes):
                # only add a node if the corresponding matrix entry is "1"
                if A[i,j]:
                    new_node = Node()
                    if prev_node is None:
                        prev_node = new_node

                    # row and column info of the node
                    new_node.row = row_node
                    new_node.column = column_node
                    column_node.size += 1

                    # insert into the column's linked list
                    column_node.U.D = new_node
                    new_node.U = column_node.U
                    new_node.D = column_node
                    column_node.U = new_node

                    # insert into the row's linked list
                    prev_node.L.R = new_node
                    new_node.L = prev_node.L
                    new_node.R = prev_node
                    prev_node.L = new_node
                    
                    prev_node = new_node
        
        return root

    def solve(self):
        """Generator for solutions to the specified exact cover problem"""
        self.partial_solution = []
        return self._search()

    def _search(self):
        """Recursive step in the search for solutions"""

        # if the matrix has no columns, yield the solution and stop recursing
        if self.root.R == self.root:
            yield self.partial_solution.copy()
            return

        # pick and cover the column
        column_node = self._choose_column()
        self._cover(column_node)

        # branching on the rows corresponding to this column
        node = column_node.D
        while node != column_node:
            self.partial_solution.append(node.row.name)

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
                
            self.partial_solution.pop()
            node = node.D

        # uncover the column
        self._uncover(column_node)

    def _choose_column(self):
        """Pick the column with the smallest number of 1s"""
        min_size = np.inf
        chosen_column = None
        column_node = self.root.R
        while column_node != self.root:
            if column_node.size < min_size:
                min_size = column_node.size
                chosen_column = column_node
            column_node = column_node.R
        return chosen_column

    def _cover(self, column_node):
        """Cover a column node"""
        # cover in the column linked list
        column_node.R.L = column_node.L
        column_node.L.R = column_node.R

        # iterate through nodes in the column
        node = column_node.D
        while node != column_node:
            right_node = node.R
            
            # cover nodes in the row
            while right_node != node:
                right_node.D.U = right_node.U
                right_node.U.D = right_node.D
                right_node.column.size -= 1
                right_node = right_node.R
                
            node = node.D

    def _uncover(self, column_node):
        """Uncover a column node"""
        # iterate through nodes in the column
        node = column_node.U
        while node != column_node:
            left_node = node.L

            # uncover nodes in the row
            while left_node != node:
                left_node.column.size += 1
                left_node.U.D = left_node
                left_node.D.U = left_node
                left_node = left_node.L
                
            node = node.U

        # uncover in the column linked list
        column_node.L.R = column_node
        column_node.R.L = column_node


# Sample run: returns the covers A D G and B D F G
if __name__ == '__main__':
    matrix = [
        [1, 0, 0, 1, 0, 0, 1], #A
        [1, 0, 0, 1, 0, 0, 0], #B
        [0, 0, 0, 1, 1, 0, 1], #C
        [0, 0, 1, 0, 1, 1, 0], #D
        [0, 1, 1, 0, 0, 1, 1], #E
        [0, 0, 0, 0, 0, 0, 1], #F
        [0, 1, 0, 0, 0, 0, 0]  #G
    ]
    matrix = np.array(matrix)
    
    row_names = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
    dlx = DLX(matrix, row_names)
    
    for sol in dlx.solve():
        print(sol)