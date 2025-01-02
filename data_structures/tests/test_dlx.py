"""dlx.py unit tests"""

import unittest

import numpy as np

from data_structures.dlx import DLX, ArrayDLX


class TestDLX(unittest.TestCase):
    """DLX unit tests
    The test problems will mostly be in the ArrayDLX tests since that class is easier to specify for testing
    """

    def test_basic_problem(self):
        """Basic exact cover problem"""
        row_names = ["A", "B", "C", "D", "E", "F", "G"]
        col_names = list(range(len(row_names)))
        entries = {
            "A": [0, 3, 6],
            "B": [0, 3],
            "C": [3, 4, 6],
            "D": [2, 4, 5],
            "E": [1, 2, 5, 6],
            "F": [6],
            "G": [1],
        }

        dlx = DLX(
            row_names=row_names,
            col_names_primary=col_names,
            col_names_secondary=[],
            entries=entries,
        )

        solutions_desired = {"ADG", "BDFG"}
        solutions_actual = {"".join(sorted(soln)) for soln in dlx.solutions()}

        assert solutions_actual == solutions_desired


class TestArrayDLX(unittest.TestCase):
    """ArrayDLX unit tests"""

    def test_basic_problem(self):
        """Basic exact cover problem"""
        A = [
            [1, 0, 0, 1, 0, 0, 1],  # A
            [1, 0, 0, 1, 0, 0, 0],  # B
            [0, 0, 0, 1, 1, 0, 1],  # C
            [0, 0, 1, 0, 1, 1, 0],  # D
            [0, 1, 1, 0, 0, 1, 1],  # E
            [0, 0, 0, 0, 0, 0, 1],  # F
            [0, 1, 0, 0, 0, 0, 0],  # G
        ]
        A = np.array(A)

        row_names = ["A", "B", "C", "D", "E", "F", "G"]
        dlx = ArrayDLX(A=A, row_names=row_names)

        solutions_desired = {"ADG", "BDFG"}
        solutions_actual = {"".join(sorted(soln)) for soln in dlx.solutions()}

        assert solutions_actual == solutions_desired

    def test_secondary_problem(self):
        """Exact problem with secondary constraints
        The secondary columns are optional to cover, and won't be covered if not necessary
        Thus H is never in any solutions since it only covers secondary columns
        And CFG is not a solution since it would double cover a secondary cover
        """
        A = [
            [1, 1, 0, 0],
            [0, 0, 1, 1],
            [0, 1, 1, 0],
            [1, 0, 0, 1],
            [1, 0, 0, 1],
            [1, 0, 0, 0],
            [0, 0, 0, 1],
            [0, 0, 0, 0],
        ]
        A_secondary = [
            [0],
            [0],
            [0],
            [0],
            [1],
            [1],
            [1],
            [1],
        ]
        A = np.array(A)
        A_secondary = np.array(A_secondary)

        row_names = ["A", "B", "C", "D", "E", "F", "G", "H"]

        dlx = ArrayDLX(A=A, row_names=row_names, A_secondary=A_secondary)

        solutions_desired = {"AB", "CD", "CE"}
        solutions_actual = {"".join(sorted(soln)) for soln in dlx.solutions()}

        assert solutions_actual == solutions_desired


# TODO how default column names are set, defaults other stuff, that checks work as intended, etc.

if __name__ == "__main__":
    unittest.main()
