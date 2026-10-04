"""Pytest gate for Week 3: every model built in modeller/ actually solves,
and each solution is checked against the classic problem's known
properties (edge respect, magic-square sums, Langford spacing).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "modeller"))

import graph_coloring  # noqa: E402
import langford  # noqa: E402
import magic_square  # noqa: E402


def test_petersen_solution_uses_at_most_three_colours_and_respects_edges() -> None:
    colours = graph_coloring.petersen_solve_default()
    assert len(colours) == graph_coloring.NUM_NODES
    assert set(colours).issubset({0, 1, 2})
    for node_a, node_b in graph_coloring.EDGES:
        assert colours[node_a] != colours[node_b]


def test_magic_square_solution_is_valid() -> None:
    grid = magic_square.magicsquare_solve_default()
    n = magic_square.N
    constant = magic_square.MAGIC_CONSTANT
    flat = [cell for row in grid for cell in row]
    assert sorted(flat) == list(range(1, n * n + 1))
    for row in grid:
        assert sum(row) == constant
    for c in range(n):
        assert sum(grid[r][c] for r in range(n)) == constant
    assert sum(grid[i][i] for i in range(n)) == constant
    assert sum(grid[i][n - 1 - i] for i in range(n)) == constant


def test_langford_seven_solution_has_correct_spacing() -> None:
    sequence = langford.langford_solve_default()
    n = langford.N
    assert len(sequence) == 2 * n
    assert sorted(sequence) == sorted(list(range(1, n + 1)) * 2)
    for k in range(1, n + 1):
        first = sequence.index(k)
        second = first + 1 + sequence[first + 1 :].index(k)
        assert second - first == k + 1
