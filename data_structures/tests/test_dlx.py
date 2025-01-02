"""dlx.py unit tests"""

import unittest

import numpy as np

from data_structures.dlx import DLX, ArrayDLX


class TestDLX(unittest.TestCase):
    """DLX unit tests"""

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

        self.assertEqual(solutions_actual, solutions_desired)

    def test_checks(self):
        """Confirm data checks are working"""
        # row names
        with self.assertRaises(AssertionError) as e:
            DLX(
                row_names=["row", "row"],
                col_names_primary=["col1"],
                col_names_secondary=["col2"],
                entries={},
            )
        self.assertEqual(str(e.exception), "Expected 1 count for 'row', found 2")

        # column names
        with self.assertRaises(AssertionError) as e:
            DLX(
                row_names=["row"],
                col_names_primary=["col1", "col1"],
                col_names_secondary=["col2"],
                entries={},
            )
        self.assertEqual(str(e.exception), "Expected 1 count for 'col1', found 2")

        with self.assertRaises(AssertionError) as e:
            DLX(
                row_names=["row"],
                col_names_primary=["col1"],
                col_names_secondary=["col2", "col2"],
                entries={},
            )
        self.assertEqual(str(e.exception), "Expected 1 count for 'col2', found 2")

        with self.assertRaises(AssertionError) as e:
            DLX(
                row_names=["row"],
                col_names_primary=["col1"],
                col_names_secondary=["col1"],
                entries={},
            )
        self.assertEqual(str(e.exception), "Overlapping elements found such as 'col1'")

        # entries
        with self.assertRaises(AssertionError) as e:
            DLX(
                row_names=["row"],
                col_names_primary=["col1"],
                col_names_secondary=["col2"],
                entries={"row1": ["col1"]},
            )
        self.assertEqual(str(e.exception), "Extra elements found such as 'row1'")

        with self.assertRaises(AssertionError) as e:
            DLX(
                row_names=["row"],
                col_names_primary=["col1"],
                col_names_secondary=["col2"],
                entries={"row": ["col3"]},
            )
        self.assertEqual(str(e.exception), "Extra elements found such as 'col3'")

        # successful init
        DLX(
            row_names=["row"],
            col_names_primary=["col1"],
            col_names_secondary=["col2"],
            entries={"row": ["col1"]},
        )


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

        self.assertEqual(solutions_actual, solutions_desired)

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

        self.assertEqual(solutions_actual, solutions_desired)

    def test_checks(self):
        """Confirm data checks are working"""
        # array checks
        with self.assertRaises(AssertionError) as e:
            ArrayDLX(A=[[]], row_names=["row"])
        self.assertEqual(str(e.exception), "A must be a np.ndarray")

        with self.assertRaises(AssertionError) as e:
            ArrayDLX(A=np.array([[]]), row_names=["row"], A_secondary=[[]])
        self.assertEqual(str(e.exception), "A_secondary must be a np.ndarray")

        with self.assertRaises(AssertionError) as e:
            ArrayDLX(A=np.array([]), row_names=["row"])
        self.assertEqual(str(e.exception), "A must be two dimensional")

        with self.assertRaises(AssertionError) as e:
            ArrayDLX(A=np.array([[]]), row_names=["row"], A_secondary=np.array([]))
        self.assertEqual(str(e.exception), "A_secondary must be two dimensional")

        with self.assertRaises(AssertionError) as e:
            ArrayDLX(
                A=np.array([[0, 0], [0, 0]]),
                row_names=["row1", "row2"],
                A_secondary=np.array([[0]]),
            )
        self.assertEqual(str(e.exception), "A has 2 rows while A_secondary has 1 rows")

        # name checks
        with self.assertRaises(AssertionError) as e:
            ArrayDLX(
                A=np.array([[0, 0], [0, 0]]),
                row_names=["row"],
                A_secondary=np.array([[0], [0]]),
            )
        self.assertEqual(str(e.exception), "1 rows specified, expected 2")

        with self.assertRaises(AssertionError) as e:
            ArrayDLX(
                A=np.array([[0, 0], [0, 0]]),
                row_names=["row1", "row2"],
                col_names=["col"],
                A_secondary=np.array([[0], [0]]),
            )
        self.assertEqual(str(e.exception), "1 columns specified, expected 2")

        with self.assertRaises(AssertionError) as e:
            ArrayDLX(
                A=np.array([[0, 0], [0, 0]]),
                row_names=["row1", "row2"],
                col_names=["col1", "col2"],
                A_secondary=np.array([[0], [0]]),
                col_names_secondary=["col3", "col4"],
            )
        self.assertEqual(str(e.exception), "2 secondary columns specified, expected 1")

        # successful init
        ArrayDLX(
            A=np.array([[0, 0], [0, 0]]),
            row_names=["row1", "row2"],
            col_names=["col1", "col2"],
            A_secondary=np.array([[0], [0]]),
            col_names_secondary=["col3"],
        )

    def test_defaults(self):
        """Check defaults are as expected"""
        # column names
        dlx = ArrayDLX(
            A=np.array([[0, 0, 0]]), A_secondary=np.array([[0, 0]]), row_names=["row"]
        )
        self.assertEqual(dlx.col_names, ["primary_0", "primary_1", "primary_2"])
        self.assertEqual(dlx.col_names_secondary, ["secondary_0", "secondary_1"])

        # secondary constraints
        dlx = ArrayDLX(A=np.array([[0, 0, 0]]), row_names=["row"])
        self.assertIsInstance(dlx.A_secondary, np.ndarray)
        self.assertEqual(dlx.A_secondary.shape, (1, 0))

    def test_translation(self):
        """Confirm we define the the DLX fields correctly"""
        dlx = ArrayDLX(
            A=np.array([[1, 0], [0, 1]]),
            row_names=["row1", "row2"],
            col_names=["col1", "col2"],
            A_secondary=np.array([[1], [0]]),
            col_names_secondary=["col3"],
        )

        self.assertEqual(dlx.row_names, ["row1", "row2"])
        self.assertEqual(dlx.col_names_primary, ["col1", "col2"])
        self.assertEqual(dlx.col_names_secondary, ["col3"])

        entries_target = {"row1": ["col1", "col3"], "row2": ["col2"]}
        self.assertEqual(dlx.entries, entries_target)


if __name__ == "__main__":
    unittest.main()
