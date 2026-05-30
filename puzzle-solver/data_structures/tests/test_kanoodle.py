"""demo_puzzle.py unit tests"""

import unittest

from data_structures.kanoodle import Kanoodle


class TestKanoodle(unittest.TestCase):
    """Kanoodle unit tests"""

    def test_full(self):
        """Check we can generate a solution"""
        board = Kanoodle()
        next(board.solutions())


if __name__ == "__main__":
    unittest.main()
