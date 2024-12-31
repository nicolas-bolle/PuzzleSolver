"""demo_puzzle.py unit tests"""

import unittest

from data_structures.demo_puzzle import DemoBoard


class TestDemoPuzzle(unittest.TestCase):
    """DemoPuzzle unit tests"""

    def test(self):
        """Check we can solve the puzzle"""
        # TODO
        board = DemoBoard()
        board.solutions()


if __name__ == "__main__":
    unittest.main()
