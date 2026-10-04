"""4x4 magic square CSP: 16 cells (values 1..16, each used exactly once)
arranged so every row, column and both diagonals sum to the magic
constant 34 = 4*(4**2+1)/2. Formulated on paper only in Week 1 Unit 3;
this is its first CP-SAT code.
"""

from ortools.sat.python import cp_model

from search_stats import print_search_stats

N = 4
MAGIC_CONSTANT = N * (N * N + 1) // 2


def build_variables(model: cp_model.CpModel) -> list[list[cp_model.IntVar]]:
    # BEGIN magicsquare_variables
    cells = [
        [model.NewIntVar(1, N * N, f"cell_{r}_{c}") for c in range(N)]
        for r in range(N)
    ]
    return cells
    # END magicsquare_variables


def add_constraints(
    model: cp_model.CpModel, cells: list[list[cp_model.IntVar]]
) -> None:
    # BEGIN magicsquare_constraints
    model.AddAllDifferent([cell for row in cells for cell in row])
    for r in range(N):
        model.Add(sum(cells[r]) == MAGIC_CONSTANT)
    for c in range(N):
        model.Add(sum(cells[r][c] for r in range(N)) == MAGIC_CONSTANT)
    model.Add(sum(cells[i][i] for i in range(N)) == MAGIC_CONSTANT)
    model.Add(sum(cells[i][N - 1 - i] for i in range(N)) == MAGIC_CONSTANT)
    # END magicsquare_constraints


def magicsquare_solve_default() -> list[list[int]]:
    model = cp_model.CpModel()
    cells = build_variables(model)
    add_constraints(model, cells)

    # BEGIN magicsquare_solve_default
    solver = cp_model.CpSolver()
    solver.parameters.num_search_workers = 1
    solver.parameters.random_seed = 42
    status = solver.Solve(model)
    print_search_stats(solver, status)
    grid = [[solver.Value(cells[r][c]) for c in range(N)] for r in range(N)]
    for row in grid:
        print(row)
    # END magicsquare_solve_default
    return grid


def magicsquare_solve_ordered() -> list[list[int]]:
    model = cp_model.CpModel()
    cells = build_variables(model)
    add_constraints(model, cells)
    flat = [cell for row in cells for cell in row]

    # BEGIN magicsquare_solve_ordered
    model.AddDecisionStrategy(
        flat, cp_model.CHOOSE_MIN_DOMAIN_SIZE, cp_model.SELECT_MIN_VALUE
    )
    solver = cp_model.CpSolver()
    solver.parameters.search_branching = cp_model.FIXED_SEARCH
    solver.parameters.num_search_workers = 1
    solver.parameters.random_seed = 42
    status = solver.Solve(model)
    print_search_stats(solver, status)
    # END magicsquare_solve_ordered
    return [[solver.Value(cells[r][c]) for c in range(N)] for r in range(N)]


if __name__ == "__main__":
    magicsquare_solve_default()
