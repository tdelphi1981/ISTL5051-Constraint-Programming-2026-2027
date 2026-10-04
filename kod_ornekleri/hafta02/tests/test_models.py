"""Pytest gate for Week 2: AC-3's hand-computed fixpoint matches the real
run, the weak and strong N-queens models agree on feasibility and each
produces a valid 8-queens solution, solver statistics are recorded (not
asserted smaller -- Unit 4's honest-caveat note, a non-fabrication guard,
not a performance assertion), and every global-constraint demo solves to a
valid, constraint-respecting solution.
"""

import sys
from pathlib import Path

from ortools.sat.python import cp_model

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "modeller"))

import ac3  # noqa: E402
import global_constraints_demo as gcd  # noqa: E402
import map_coloring_models  # noqa: E402
import nqueens_models  # noqa: E402
from nqueens_propagation_compare import collect_solver_stats  # noqa: E402


def _solve(model: cp_model.CpModel) -> tuple[int, cp_model.CpSolver]:
    solver = cp_model.CpSolver()
    solver.parameters.num_workers = 1
    solver.parameters.random_seed = 42
    status = solver.Solve(model)
    return status, solver


def test_ac3_reaches_the_hand_computed_fixpoint() -> None:
    domains = ac3.run()
    assert domains == {"X": {1}, "Y": {2}, "Z": {3}}


def _assert_valid_nqueens_solution(columns: list[int]) -> None:
    n = len(columns)
    assert len(set(columns)) == n
    for i in range(n):
        for j in range(i + 1, n):
            assert abs(columns[i] - columns[j]) != abs(i - j)


def test_strong_and_weak_nqueens_models_agree_and_are_valid() -> None:
    n = 8
    strong_model, strong_queens = nqueens_models.build_strong_model(n)
    weak_model, weak_queens = nqueens_models.build_weak_model(n)

    strong_status, strong_solver = _solve(strong_model)
    weak_status, weak_solver = _solve(weak_model)

    assert strong_status in (cp_model.OPTIMAL, cp_model.FEASIBLE)
    assert weak_status in (cp_model.OPTIMAL, cp_model.FEASIBLE)

    _assert_valid_nqueens_solution([strong_solver.Value(q) for q in strong_queens])
    _assert_valid_nqueens_solution([weak_solver.Value(q) for q in weak_queens])


def test_solver_stats_are_recorded_for_both_nqueens_models() -> None:
    strong_model, _ = nqueens_models.build_strong_model(8)
    weak_model, _ = nqueens_models.build_weak_model(8)

    strong_stats = collect_solver_stats(strong_model)
    weak_stats = collect_solver_stats(weak_model)

    for stats in (strong_stats, weak_stats):
        assert stats["status"] in ("OPTIMAL", "FEASIBLE")
        assert stats["branches"] >= 0
        assert stats["conflicts"] >= 0
        assert stats["wall_time"] >= 0.0


def test_map_coloring_models_reused_from_week_one_respect_every_edge() -> None:
    assignment = map_coloring_models.solve()
    for region_a, region_b in map_coloring_models.EDGES:
        assert assignment[region_a] != assignment[region_b]


def test_element_demo_narrows_index_to_prices_at_least_twenty() -> None:
    prices = [10, 25, 40, 15]
    model = cp_model.CpModel()
    index = model.NewIntVar(0, len(prices) - 1, "index")
    target = model.NewIntVar(min(prices), max(prices), "target")
    model.AddElement(index, prices, target)
    model.Add(target >= 20)
    remaining = gcd._enumerate_values(model, index)
    assert remaining == [1, 2]


def test_table_demo_matches_the_not_equal_constraint() -> None:
    allowed = [(i, j) for i in range(3) for j in range(3) if i != j]
    model = cp_model.CpModel()
    color1 = model.NewIntVar(0, 2, "color1")
    color2 = model.NewIntVar(0, 2, "color2")
    model.AddAllowedAssignments([color1, color2], allowed)
    status, solver = _solve(model)
    assert status in (cp_model.OPTIMAL, cp_model.FEASIBLE)
    assert solver.Value(color1) != solver.Value(color2)


def test_circuit_demo_visits_every_node_exactly_once() -> None:
    n = 4
    model = cp_model.CpModel()
    literals = {
        (i, j): model.NewBoolVar(f"arc_{i}_{j}")
        for i in range(n)
        for j in range(n)
        if i != j
    }
    model.AddCircuit([(i, j, lit) for (i, j), lit in literals.items()])
    status, solver = _solve(model)
    assert status in (cp_model.OPTIMAL, cp_model.FEASIBLE)
    chosen = {(i, j) for (i, j), lit in literals.items() if solver.Value(lit)}
    cycle = gcd._extract_cycle(chosen, n)
    assert sorted(cycle) == list(range(n))


def test_cumulative_demo_never_exceeds_capacity() -> None:
    durations = [3, 2, 2]
    demands = [2, 3, 2]
    capacity = 4
    horizon = sum(durations)
    model = cp_model.CpModel()
    starts = [model.NewIntVar(0, horizon, f"start_{t}") for t in range(3)]
    intervals = [
        model.NewFixedSizeIntervalVar(starts[t], durations[t], f"task_{t}")
        for t in range(3)
    ]
    model.AddCumulative(intervals, demands, capacity)
    status, solver = _solve(model)
    assert status in (cp_model.OPTIMAL, cp_model.FEASIBLE)

    result = [solver.Value(s) for s in starts]
    for instant in range(horizon):
        load = sum(
            demands[t]
            for t in range(3)
            if result[t] <= instant < result[t] + durations[t]
        )
        assert load <= capacity
