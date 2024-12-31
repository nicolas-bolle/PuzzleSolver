"""dlx.py unit tests"""

import unittest

import numpy as np

from data_structures.dlx import ArrayDLX


# TODO DLX test class
class TestArrayDLX(unittest.TestCase):
    """ArrayDLX unit tests"""

    def test_problem_1(self):
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
        dlx = ArrayDLX(A, row_names)

        solutions_desired = {"ADG", "BDFG"}
        solutions_actual = {"".join(sorted(soln)) for soln in dlx.solutions()}

        assert solutions_actual == solutions_desired


if __name__ == "__main__":
    unittest.main()
