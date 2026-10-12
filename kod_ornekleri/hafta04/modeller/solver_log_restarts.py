"""Captures CP-SAT's own verbose search log for the order-9 Golomb-ruler
optimality proof (Unit 3) — a real source of restart/nogood-learning
activity, not a hand-written log excerpt. Single worker, so every restart
line in the captured log belongs to one systematic search, not a mix of
concurrent portfolio workers (Unit 4 reuses this same instance for that
contrast).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from ortools.sat.python import cp_model

from golomb_ruler import golomb_distinct_distances, golomb_variables

ORDER = 9
UPPER_BOUND = ORDER * ORDER
TIME_LIMIT_SECONDS = 30.0
SEED = 42


def verbose_model_setup(
    order: int, upper_bound: int
) -> tuple[cp_model.CpModel, list[cp_model.IntVar]]:
    model, marks = golomb_variables(order, upper_bound)
    # BEGIN verbose_model_setup
    golomb_distinct_distances(model, marks, upper_bound)
    model.Minimize(marks[-1])
    # END verbose_model_setup
    return model, marks


def verbose_solve_run(
    order: int, upper_bound: int, time_limit: float, seed: int
) -> str:
    model, marks = verbose_model_setup(order, upper_bound)
    # BEGIN verbose_solve_run
    solver = cp_model.CpSolver()
    solver.parameters.log_search_progress = True
    solver.parameters.max_time_in_seconds = time_limit
    solver.parameters.random_seed = seed
    solver.parameters.num_search_workers = 1
    status = solver.Solve(model)
    print(f"Status: {solver.StatusName(status)}")
    print(f"Length for {order} marks: {solver.Value(marks[-1])}")
    # END verbose_solve_run
    return solver.StatusName(status)


if __name__ == "__main__":
    verbose_solve_run(ORDER, UPPER_BOUND, TIME_LIMIT_SECONDS, SEED)
