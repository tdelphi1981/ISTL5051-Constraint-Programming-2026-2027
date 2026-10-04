"""Pytest gate for Week 1: every model built in modeller/ actually solves,
and each solution is checked against the classic problem's known
properties (no clash, exact solution count, full validity).
"""

import sys
from pathlib import Path

from ortools.sat.python import cp_model

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "modeller"))

import csp_basics  # noqa: E402
import map_coloring  # noqa: E402
import nqueens  # noqa: E402
import sudoku  # noqa: E402


def test_toy_csp_has_a_solution() -> None:
    status, values = csp_basics.solve()
    assert status in (cp_model.OPTIMAL, cp_model.FEASIBLE)
    assert len(set(values)) == 3


def test_eight_queens_solution_has_no_clash() -> None:
    columns = nqueens.solve_one(8)
    n = len(columns)
    assert len(set(columns)) == n
    for i in range(n):
        for j in range(i + 1, n):
            assert abs(columns[i] - columns[j]) != abs(i - j)


def test_six_queens_solution_count_is_four() -> None:
    assert nqueens.enumerate_solutions(6) == 4


def test_sudoku_solution_is_fully_valid() -> None:
    solution = sudoku.solve()
    full_set = set(range(1, 10))
    for row in solution:
        assert set(row) == full_set
    for col in range(9):
        assert {solution[row][col] for row in range(9)} == full_set
    for box_row in range(3):
        for box_col in range(3):
            box = {
                solution[3 * box_row + r][3 * box_col + c]
                for r in range(3)
                for c in range(3)
            }
            assert box == full_set


def test_map_coloring_respects_every_adjacency_edge() -> None:
    assignment = map_coloring.solve()
    for region_a, region_b in map_coloring.EDGES:
        assert assignment[region_a] != assignment[region_b]
