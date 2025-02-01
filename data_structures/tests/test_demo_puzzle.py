"""demo_puzzle.py unit tests"""

import unittest

from data_structures.demo_puzzle import (
    Demo1GridBoard,
    Demo2GridBoard,
    Demo3GridBoard,
    Demo4GridBoard,
    Demo5GridBoard,
)


class TestDemoPuzzles(unittest.TestCase):
    """DemoPuzzle unit tests"""

    def test_demo1(self):
        """Check we can solve the puzzle"""
        board = Demo1GridBoard()
        solutions = list(board.solutions())
        assert len(solutions) == 8

    def test_demo2(self):
        """Check we can't solve the puzzle"""
        board = Demo2GridBoard()
        solutions = list(board.solutions())
        assert len(solutions) == 0

    def test_demo3(self):
        """Check we can solve the puzzle"""
        board = Demo3GridBoard()
        solutions = list(board.solutions())
        assert len(solutions) == 28

    def test_demo4(self):
        """Check we can solve the puzzle"""
        board = Demo4GridBoard()
        solutions = list(board.solutions())
        assert len(solutions) == 10

    def test_demo5(self):
        """Check we can solve the puzzle"""
        board = Demo5GridBoard()
        solutions = list(board.solutions())
        assert len(solutions) == 3


if __name__ == "__main__":
    unittest.main()
