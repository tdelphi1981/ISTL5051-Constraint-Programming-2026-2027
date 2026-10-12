"""Large neighbourhood search (LNS) repair loop for large N-queens (Unit 2).
Unlike Unit 1's min-conflicts, each repair step relaxes several rows at
once and hands the freed sub-problem to CP-SAT, keeping the full-board
conflict count as the informal objective this week's LNS drives toward
zero (formal soft-constraint vocabulary is Week 8's job, not this week's).
"""

import random

from ortools.sat.python import cp_model

N = 50
NEIGHBOURHOOD_SIZE = 8
ROUNDS = 30
SEED = 7


def count_conflicts(columns: list[int]) -> int:
    """Number of attacking row pairs in the "one queen per row" viewpoint."""
    n = len(columns)
    conflicts = 0
    for i in range(n):
        for j in range(i + 1, n):
            if columns[i] == columns[j] or abs(columns[i] - columns[j]) == j - i:
                conflicts += 1
    return conflicts


def lns_initial_assignment(n: int, seed: int) -> list[int]:
    # BEGIN lns_initial_assignment
    rng = random.Random(seed)
    columns = [rng.randrange(n) for _ in range(n)]
    # END lns_initial_assignment
    return columns


def lns_destroy(n: int, k: int, rng: random.Random) -> list[int]:
    # BEGIN lns_destroy
    relaxed_rows = rng.sample(range(n), k)
    # END lns_destroy
    return relaxed_rows


def lns_repair(columns: list[int], relaxed_rows: list[int], n: int) -> list[int]:
    fixed_rows = [row for row in range(n) if row not in relaxed_rows]
    model = cp_model.CpModel()
    relaxed_vars = {row: model.NewIntVar(0, n - 1, f"row_{row}") for row in relaxed_rows}
    # BEGIN lns_repair
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
    solver.parameters.num_search_workers = 1
    solver.parameters.random_seed = 42
    status = solver.Solve(model)
    if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return columns
    proposal = list(columns)
    for row in relaxed_rows:
        proposal[row] = solver.Value(relaxed_vars[row])
    return proposal if count_conflicts(proposal) <= count_conflicts(columns) else columns
    # END lns_repair


def lns_loop(n: int, k: int, rounds: int, seed: int) -> tuple[list[int], int]:
    columns = lns_initial_assignment(n, seed)
    rng = random.Random(seed + 1)
    conflicts = count_conflicts(columns)
    print(f"Round 0: {conflicts} conflicts")
    # BEGIN lns_loop
    for round_number in range(1, rounds + 1):
        relaxed_rows = lns_destroy(n, k, rng)
        columns = lns_repair(columns, relaxed_rows, n)
        conflicts = count_conflicts(columns)
        print(f"Round {round_number}: {conflicts} conflicts")
    # END lns_loop
    return columns, conflicts


if __name__ == "__main__":
    lns_loop(N, NEIGHBOURHOOD_SIZE, ROUNDS, SEED)
