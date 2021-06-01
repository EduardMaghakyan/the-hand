from puzzle import Puzzle
import pytest

from typing import List


@pytest.fixture
def puzzle() -> Puzzle:
    p = Puzzle()
    p.grid = [['*', '*', '*', '*', '*', '*', '*', '*', '*'],
              ['X', 7, 'X', 2, 'X', 15, 'X', 8, 'X'],
              ['X', 1, 'X', 14, 'X', 13, 'X', 12, 'X'],
              ['X', 10, 'X', 6, 'X', 5, 'X', 0, 'X'],
              ['X', 9, 'X', 4, 'X', 3, 'X', 11, 'X'],
              ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X']]
    return p


def test_swap_top_of_two_columns(puzzle):
    expected_state = [2, 1, 10, 9, 7, 14, 6, 4, 15, 13, 5, 3, 8, 12, 0, 11]
    puzzle.swap_tops(1, 3)
    assert expected_state == puzzle.current_state
