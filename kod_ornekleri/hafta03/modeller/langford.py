"""Langford pairs, n=7: arrange 1..7, each value appearing twice, into a
length-14 sequence such that the two occurrences of value k have exactly
k other entries between them (equivalently, their positions differ by
k+1). A solution exists only when n = 0 or 3 (mod 4); n=7 (7 = 3 mod 4)
has one. Chosen because its search-tree size is dramatically sensitive to
variable/value order.
"""

from ortools.sat.python import cp_model

from search_stats import print_search_stats

N = 7
NUM_POSITIONS = 2 * N


def build_variables(model: cp_model.CpModel) -> list[list[cp_model.IntVar]]:
    # BEGIN langford_variables
    positions = [
        [model.NewIntVar(0, NUM_POSITIONS - 1, f"pos_{k}_{i}") for i in range(2)]
        for k in range(1, N + 1)
    ]
    return positions
    # END langford_variables


def add_constraints(
    model: cp_model.CpModel, positions: list[list[cp_model.IntVar]]
) -> None:
    # BEGIN langford_constraints
    model.AddAllDifferent([entry for pair in positions for entry in pair])
    for k in range(1, N + 1):
        first, second = positions[k - 1]
        model.Add(second - first == k + 1)
    # END langford_constraints


def _sequence_from_positions(
    positions: list[list[cp_model.IntVar]], solver: cp_model.CpSolver
) -> list[int]:
    sequence = [0] * NUM_POSITIONS
    for k in range(1, N + 1):
        first, second = positions[k - 1]
        sequence[solver.Value(first)] = k
        sequence[solver.Value(second)] = k
    return sequence


def langford_solve_default() -> list[int]:
    model = cp_model.CpModel()
    positions = build_variables(model)
    add_constraints(model, positions)

    # BEGIN langford_solve_default
    solver = cp_model.CpSolver()
    solver.parameters.num_search_workers = 1
    solver.parameters.random_seed = 42
    solver.parameters.max_time_in_seconds = 10
    status = solver.Solve(model)
    print_search_stats(solver, status)
    # END langford_solve_default
    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return _sequence_from_positions(positions, solver)
    return []


def langford_solve_ordered() -> list[int]:
    model = cp_model.CpModel()
    positions = build_variables(model)
    add_constraints(model, positions)
    flat = [entry for pair in positions for entry in pair]

    # BEGIN langford_solve_ordered
    model.AddDecisionStrategy(
        flat, cp_model.CHOOSE_MIN_DOMAIN_SIZE, cp_model.SELECT_MIN_VALUE
    )
    solver = cp_model.CpSolver()
    solver.parameters.search_branching = cp_model.FIXED_SEARCH
    solver.parameters.num_search_workers = 1
    solver.parameters.random_seed = 42
    solver.parameters.max_time_in_seconds = 10
    status = solver.Solve(model)
    print_search_stats(solver, status)
    # END langford_solve_ordered
    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return _sequence_from_positions(positions, solver)
    return []


def langford_time_limited(time_limit_seconds: float = 0.001) -> list[int]:
    model = cp_model.CpModel()
    positions = build_variables(model)
    add_constraints(model, positions)

    # BEGIN langford_time_limited
    solver = cp_model.CpSolver()
    solver.parameters.num_search_workers = 1
    solver.parameters.random_seed = 42
    solver.parameters.max_time_in_seconds = time_limit_seconds
    status = solver.Solve(model)
    print_search_stats(solver, status)
    # END langford_time_limited
    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return _sequence_from_positions(positions, solver)
    return []


if __name__ == "__main__":
    langford_solve_default()
