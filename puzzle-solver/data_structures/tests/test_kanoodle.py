"""demo_puzzle.py unit tests"""

from data_structures.kanoodle import Kanoodle


def test_full():
    """Check we can generate a solution"""
    board = Kanoodle()
    next(board.solutions())
