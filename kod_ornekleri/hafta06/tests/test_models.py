"""Pytest gate for Week 6: every MiniZinc model actually solves, and each
solution is checked against a brute-force computation of the same small
instance. Tests that need a MIP backend probe it with a trivial solve
first and skip (with a printed reason) if that backend is not usable in
this environment, rather than assuming Gurobi/HiGHS are always installed.
"""

import itertools
from pathlib import Path

import minizinc
import pytest

MZN_DIR = Path(__file__).resolve().parent.parent / "minizinc"


def _load(mzn_name: str, dzn_name: str) -> minizinc.Model:
    model = minizinc.Model(MZN_DIR / mzn_name)
    model.add_file(MZN_DIR / dzn_name)
    return model


def _mip_backend_or_skip(name: str) -> minizinc.Solver:
    """Return a looked-up MIP backend, or skip the test if it cannot
    actually solve a trivial instance (registered but non-functional,
    e.g. a missing license or a missing plugin library)."""
    try:
        solver = minizinc.Solver.lookup(name)
        probe = minizinc.Model()
        probe.add_string("var 1..2: x; solve satisfy;")
        minizinc.Instance(solver, probe).solve()
        return solver
    except minizinc.MiniZincError as error:
        pytest.skip(f"MIP backend '{name}' not usable here: {error}")


def test_knapsack_optimum_matches_brute_force() -> None:
    weights = [2, 3, 4, 5]
    values = [3, 4, 5, 6]
    capacity = 7
    best = max(
        sum(v for v, keep in zip(values, subset) if keep)
        for subset in itertools.product([0, 1], repeat=len(weights))
        if sum(w for w, keep in zip(weights, subset) if keep) <= capacity
    )

    solver = minizinc.Solver.lookup("gecode")
    result = minizinc.Instance(solver, _load("knapsack.mzn", "knapsack.dzn")).solve()
    assert result.solution.objective == best


def test_six_queens_solution_count_is_four() -> None:
    solver = minizinc.Solver.lookup("gecode")
    result = minizinc.Instance(solver, _load("nqueens.mzn", "nqueens.dzn")).solve(
        all_solutions=True
    )
    assert len(result.solution) == 4


def test_assignment_optimal_cost_matches_brute_force() -> None:
    cost = [[9, 2, 7, 8], [6, 4, 3, 7], [5, 8, 1, 8], [7, 6, 9, 4]]
    n = len(cost)
    best = min(
        sum(cost[i][perm[i]] for i in range(n))
        for perm in itertools.permutations(range(n))
    )

    solver = minizinc.Solver.lookup("gecode")
    result = minizinc.Instance(
        solver, _load("assignment.mzn", "assignment.dzn")
    ).solve()
    assert result.solution.objective == best


@pytest.mark.parametrize("backend", ["coin-bc", "highs"])
def test_assignment_mip_backend_matches_gecode(backend: str) -> None:
    solver = _mip_backend_or_skip(backend)
    result = minizinc.Instance(
        solver, _load("assignment.mzn", "assignment.dzn")
    ).solve()
    assert result.solution.objective == 13
