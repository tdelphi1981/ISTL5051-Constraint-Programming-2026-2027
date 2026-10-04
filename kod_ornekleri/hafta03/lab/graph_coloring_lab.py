"""Lab starter: re-run modeller/graph_coloring.py's Petersen-graph model
with a forced decision strategy of your own. The variables and
constraints are reused unchanged from modeller/graph_coloring.py; the
solver setup below is deliberately incomplete, marked with a TODO. Fill
in the missing line, then re-run and compare the printed statistics
against modeller/graph_coloring.py's own default and ordered runs.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "modeller"))

from ortools.sat.python import cp_model
from graph_coloring import add_constraints, build_variables
from search_stats import print_search_stats


def solve_lab() -> list[int]:
    model = cp_model.CpModel()
    colours = build_variables(model)
    add_constraints(model, colours)

    # BEGIN graph_coloring_lab_broken
    model.AddDecisionStrategy(
        colours, cp_model.CHOOSE_MIN_DOMAIN_SIZE, cp_model.SELECT_MIN_VALUE
    )
    solver = cp_model.CpSolver()
    # TODO: AddDecisionStrategy above only takes effect once CP-SAT's
    # search mode is switched away from automatic search. Set
    # solver.parameters.search_branching to the right enum value here.
    solver.parameters.num_search_workers = 1
    # END graph_coloring_lab_broken
    solver.parameters.random_seed = 42
    status = solver.Solve(model)
    print_search_stats(solver, status)
    return [solver.Value(colour) for colour in colours]


if __name__ == "__main__":
    solve_lab()
