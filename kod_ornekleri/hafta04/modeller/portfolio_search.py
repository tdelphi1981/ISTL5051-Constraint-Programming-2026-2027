"""Portfolio/parallel search (Unit 4): solves the same order-9 Golomb-
ruler optimality proof used in `solver_log_restarts.py`, once with
`num_search_workers=1` and once with a larger worker count, recording
real wall-clock time and proof status for each — no assumed speed-up.
"""

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from ortools.sat.python import cp_model

from golomb_ruler import golomb_distinct_distances, golomb_variables

ORDER = 9
UPPER_BOUND = ORDER * ORDER
SEED = 42
MULTI_WORKERS = 8


def portfolio_build_model(
    order: int, upper_bound: int
) -> tuple[cp_model.CpModel, list[cp_model.IntVar]]:
    model, marks = golomb_variables(order, upper_bound)
    # BEGIN portfolio_build_model
    golomb_distinct_distances(model, marks, upper_bound)
    model.Minimize(marks[-1])
    # END portfolio_build_model
    return model, marks


def portfolio_single_worker(
    order: int, upper_bound: int, seed: int
) -> tuple[float, str, int]:
    model, marks = portfolio_build_model(order, upper_bound)
    # BEGIN portfolio_single_worker
    solver = cp_model.CpSolver()
    solver.parameters.num_search_workers = 1
    solver.parameters.random_seed = seed
    start = time.perf_counter()
    status = solver.Solve(model)
    wall_time = time.perf_counter() - start
    # END portfolio_single_worker
    return wall_time, solver.StatusName(status), solver.Value(marks[-1])


def portfolio_multi_worker(
    order: int, upper_bound: int, seed: int, workers: int
) -> tuple[float, str, int]:
    model, marks = portfolio_build_model(order, upper_bound)
    # BEGIN portfolio_multi_worker
    solver = cp_model.CpSolver()
    solver.parameters.num_search_workers = workers
    solver.parameters.random_seed = seed
    start = time.perf_counter()
    status = solver.Solve(model)
    wall_time = time.perf_counter() - start
    # END portfolio_multi_worker
    return wall_time, solver.StatusName(status), solver.Value(marks[-1])


def portfolio_report(
    order: int, upper_bound: int, seed: int, workers: int
) -> None:
    single_time, single_status, single_length = portfolio_single_worker(order, upper_bound, seed)
    multi_time, multi_status, multi_length = portfolio_multi_worker(order, upper_bound, seed, workers)
    # BEGIN portfolio_report
    speedup = single_time / multi_time if multi_time > 0 else float("inf")
    print(f"num_search_workers=1        wall_time={single_time:.4f}s  "
          f"length={single_length}  status={single_status}")
    print(f"num_search_workers={workers}        wall_time={multi_time:.4f}s  "
          f"length={multi_length}  status={multi_status}")
    print(f"speed-up (1-worker time / {workers}-worker time): {speedup:.2f}x")
    # END portfolio_report


if __name__ == "__main__":
    portfolio_report(ORDER, UPPER_BOUND, SEED, MULTI_WORKERS)
