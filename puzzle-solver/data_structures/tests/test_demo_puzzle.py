"""demo_puzzle.py unit tests"""

from data_structures.demo_puzzle import (
    Demo1GridBoard,
    Demo2GridBoard,
    Demo3GridBoard,
    Demo4GridBoard,
    Demo5GridBoard,
)


def test_demo1():
    """Check we can solve the puzzle"""
    board = Demo1GridBoard()
    solutions = list(board.solutions())
    assert len(solutions) == 8


def test_demo2():
    """Check we can't solve the puzzle"""
    board = Demo2GridBoard()
    solutions = list(board.solutions())
    assert len(solutions) == 0


def test_demo3():
    """Check we can solve the puzzle"""
    board = Demo3GridBoard()
    solutions = list(board.solutions())
    assert len(solutions) == 28


def test_demo4():
    """Check we can solve the puzzle"""
    board = Demo4GridBoard()
    solutions = list(board.solutions())
    assert len(solutions) == 10


def test_demo5():
    """Check we can solve the puzzle"""
    board = Demo5GridBoard()
    solutions = list(board.solutions())
    assert len(solutions) == 3
