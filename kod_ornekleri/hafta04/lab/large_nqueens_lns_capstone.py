"""Lab capstone (Unit 2 + Unit 4 combined): an LNS repair loop for a
harder large-N-queens instance, N=200, than modeller/large_nqueens_lns.py's
N=50 reference. `lns_destroy` below is still that reference script's plain
random destroy rule; `REPAIR_WORKERS` is still 1. Run the script once as
given, then complete the TODOs -- switch the destroy rule to a targeted
("worst-first") one and raise REPAIR_WORKERS -- and run it again, checking
the final conflict count and the elapsed time against TIME_BUDGET_SECONDS.
"""

import random
import time

from ortools.sat.python import cp_model

N = 200
NEIGHBOURHOOD_SIZE = 10
ROUNDS = 25
SEED = 5
TIME_BUDGET_SECONDS = 5.0
REPAIR_WORKERS = 1  # TODO: raise this (e.g. to 4) once lns_destroy is targeted


def count_conflicts(columns: list[int]) -> int:
    """Number of attacking row pairs in the "one queen per row" viewpoint."""
    n = len(columns)
    conflicts = 0
    for i in range(n):
        for j in range(i + 1, n):
            if columns[i] == columns[j] or abs(columns[i] - columns[j]) == j - i:
                conflicts += 1
    return conflicts


def conflicted_rows(columns: list[int]) -> list[int]:
    """Rows currently involved in at least one attacking pair."""
    n = len(columns)
    rows = set()
    for i in range(n):
        for j in range(i + 1, n):
            if columns[i] == columns[j] or abs(columns[i] - columns[j]) == j - i:
                rows.add(i)
                rows.add(j)
    return sorted(rows)


def lns_initial_assignment(n: int, seed: int) -> list[int]:
    rng = random.Random(seed)
    return [rng.randrange(n) for _ in range(n)]


def lns_destroy(columns: list[int], n: int, k: int, rng: random.Random) -> list[int]:
    # TODO: this is still large_nqueens_lns.py's plain random destroy rule
    # -- every round relaxes k rows chosen uniformly at random, ignoring
    # which rows are actually in conflict. Replace the line below with a
    # targeted rule: call conflicted_rows(columns) first, shuffle it, take
    # up to k rows from it, and -- only if fewer than k rows are
    # conflicted -- top the neighbourhood up with randomly chosen extra
    # rows so it still has exactly k rows.
    return rng.sample(range(n), k)


def lns_repair(
    columns: list[int], relaxed_rows: list[int], n: int, workers: int
) -> list[int]:
    fixed_rows = [row for row in range(n) if row not in relaxed_rows]
    model = cp_model.CpModel()
    relaxed_vars = {row: model.NewIntVar(0, n - 1, f"row_{row}") for row in relaxed_rows}
    model.AddAllDifferent([relaxed_vars[r] for r in relaxed_rows])
    model.AddAllDifferent([relaxed_vars[r] + r for r in relaxed_rows])
    model.AddAllDifferent([relaxed_vars[r] - r for r in relaxed_rows])
    for row in relaxed_rows:
        for fixed_row in fixed_rows:
            fixed_col = columns[fixed_row]
            model.Add(relaxed_vars[row] != fixed_col)
            model.Add(relaxed_vars[row] + row != fixed_col + fixed_row)
            model.Add(relaxed_vars[row] - row != fixed_col - fixed_row)
    solver = cp_model.CpSolver()
    solver.parameters.num_search_workers = workers
    solver.parameters.random_seed = 42
    status = solver.Solve(model)
    if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return columns
    proposal = list(columns)
    for row in relaxed_rows:
        proposal[row] = solver.Value(relaxed_vars[row])
    return proposal if count_conflicts(proposal) <= count_conflicts(columns) else columns


def lns_loop(n: int, k: int, rounds: int, seed: int, workers: int) -> tuple[list[int], int]:
    columns = lns_initial_assignment(n, seed)
    rng = random.Random(seed + 1)
    conflicts = count_conflicts(columns)
    print(f"Round 0: {conflicts} conflicts")
    for round_number in range(1, rounds + 1):
        relaxed_rows = lns_destroy(columns, n, k, rng)
        columns = lns_repair(columns, relaxed_rows, n, workers)
        conflicts = count_conflicts(columns)
        print(f"Round {round_number}: {conflicts} conflicts")
    return columns, conflicts


if __name__ == "__main__":
    start = time.perf_counter()
    _columns, final_conflicts = lns_loop(N, NEIGHBOURHOOD_SIZE, ROUNDS, SEED, REPAIR_WORKERS)
    elapsed = time.perf_counter() - start
    print(f"Elapsed: {elapsed:.2f}s (budget {TIME_BUDGET_SECONDS}s), final conflicts={final_conflicts}")
