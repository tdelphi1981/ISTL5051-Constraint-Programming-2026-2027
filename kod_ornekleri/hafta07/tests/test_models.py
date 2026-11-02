"""Pytest gate for Week 7: every gurobipy model in modeller/ solves, and
each result is checked against the values worked out by hand in the
brief (or, for production planning, a weak solver-independent sanity
check).
"""

import sys
from pathlib import Path

import pytest

gp = pytest.importorskip("gurobipy")
from gurobipy import GRB  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "modeller"))

import assignment  # noqa: E402
import knapsack  # noqa: E402
import production_planning  # noqa: E402


def test_knapsack_ip_optimum_is_eight() -> None:
    assert knapsack.solve_ip() == pytest.approx(8.0)


def test_knapsack_lp_relaxation_optimum_is_eight_point_two_five() -> None:
    assert knapsack.solve_lp_relaxation() == pytest.approx(8.25)


def test_assignment_optimal_cost_is_fourteen_on_the_diagonal() -> None:
    cost, chosen = assignment.solve()
    assert cost == pytest.approx(14.0)
    assert chosen == {"W1": "Ta", "W2": "Tb", "W3": "Tc", "W4": "Td"}


def _single_product_plan_profit(product: str) -> float:
    max_by_labour = (
        production_planning.LABOUR_BUDGET // production_planning.LABOUR_USE[product]
    )
    max_by_machine = (
        production_planning.MACHINE_BUDGET // production_planning.MACHINE_USE[product]
    )
    units = min(max_by_labour, max_by_machine)
    return units * production_planning.PROFIT[product]


def test_production_planning_beats_every_single_product_plan() -> None:
    model, _ = production_planning.build_model()
    model.optimize()
    assert model.Status == GRB.OPTIMAL
    best_single_product_profit = max(
        _single_product_plan_profit(p) for p in production_planning.PRODUCTS
    )
    assert model.ObjVal > best_single_product_profit
