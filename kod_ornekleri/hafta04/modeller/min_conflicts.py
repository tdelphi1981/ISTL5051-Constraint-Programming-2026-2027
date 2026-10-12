"""Pure-Python min-conflicts local search for N-queens (Unit 1). No CP-SAT
here: local search starts from a complete assignment and repairs it, one
row at a time, using row/diagonal occupancy counters for an O(1)-per-
candidate conflict count (not a full O(N) recount per candidate value).
"""

import random

N = 2000
MAX_STEPS = 100_000
SEED = 1


def min_conflicts_state(
    n: int, seed: int
) -> tuple[list[int], list[int], list[int], list[int]]:
    # BEGIN min_conflicts_state
    rng = random.Random(seed)
    columns = [rng.randrange(n) for _ in range(n)]
    col_count = [0] * n
    diag1_count = [0] * (2 * n - 1)  # index: row - col + (n - 1)
    diag2_count = [0] * (2 * n - 1)  # index: row + col
    for row, col in enumerate(columns):
        col_count[col] += 1
        diag1_count[row - col + n - 1] += 1
        diag2_count[row + col] += 1
    # END min_conflicts_state
    return columns, col_count, diag1_count, diag2_count


def _conflicted_rows(
    n: int,
    columns: list[int],
    col_count: list[int],
    diag1_count: list[int],
    diag2_count: list[int],
) -> list[int]:
    rows = []
    for row, col in enumerate(columns):
        total = col_count[col] + diag1_count[row - col + n - 1] + diag2_count[row + col]
        if total > 3:  # each of the three counters includes this queen itself
            rows.append(row)
    return rows


def min_conflicts_step(
    row: int,
    n: int,
    columns: list[int],
    col_count: list[int],
    diag1_count: list[int],
    diag2_count: list[int],
    rng: random.Random,
) -> int:
    # BEGIN min_conflicts_step
    col_count[columns[row]] -= 1
    diag1_count[row - columns[row] + n - 1] -= 1
    diag2_count[row + columns[row]] -= 1

    best_columns, best_conflicts = [], n + 1
    for col in range(n):
        conflicts = col_count[col] + diag1_count[row - col + n - 1] + diag2_count[row + col]
        if conflicts < best_conflicts:
            best_columns, best_conflicts = [col], conflicts
        elif conflicts == best_conflicts:
            best_columns.append(col)
    new_col = rng.choice(best_columns)

    columns[row] = new_col
    col_count[new_col] += 1
    diag1_count[row - new_col + n - 1] += 1
    diag2_count[row + new_col] += 1
    # END min_conflicts_step
    return best_conflicts


def min_conflicts_loop(n: int, seed: int, max_steps: int) -> tuple[list[int], int]:
    columns, col_count, diag1_count, diag2_count = min_conflicts_state(n, seed)
    rng = random.Random(seed + 1)
    # BEGIN min_conflicts_loop
    for step in range(1, max_steps + 1):
        conflicted = _conflicted_rows(n, columns, col_count, diag1_count, diag2_count)
        if not conflicted:
            print(f"Solved N={n}: 0 conflicts remaining after {step - 1} steps.")
            return columns, step - 1
        row = rng.choice(conflicted)
        min_conflicts_step(row, n, columns, col_count, diag1_count, diag2_count, rng)
    remaining = len(_conflicted_rows(n, columns, col_count, diag1_count, diag2_count))
    print(f"Stopped N={n}: {remaining} conflicted rows remain after {max_steps} steps.")
    # END min_conflicts_loop
    return columns, max_steps


if __name__ == "__main__":
    min_conflicts_loop(N, SEED, MAX_STEPS)
