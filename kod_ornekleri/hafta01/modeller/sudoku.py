"""9x9 Sudoku CSP: one variable per cell (domain 1-9), a fixed puzzle's
givens applied by equality, and AllDifferent over every row, column and
3x3 box.
"""

from ortools.sat.python import cp_model

PUZZLE = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9],
]


def build_variables(model: cp_model.CpModel) -> list[list[cp_model.IntVar]]:
    # BEGIN sudoku_variables
    grid = [
        [model.NewIntVar(1, 9, f"cell_{row}_{col}") for col in range(9)]
        for row in range(9)
    ]
    return grid
    # END sudoku_variables


def apply_givens(model: cp_model.CpModel, grid: list[list[cp_model.IntVar]]) -> None:
    # BEGIN sudoku_givens
    for row in range(9):
        for col in range(9):
            value = PUZZLE[row][col]
            if value != 0:
                model.Add(grid[row][col] == value)
    # END sudoku_givens


def add_constraints(model: cp_model.CpModel, grid: list[list[cp_model.IntVar]]) -> None:
    # BEGIN sudoku_constraints
    for row in range(9):
        model.AddAllDifferent(grid[row])
    for col in range(9):
        model.AddAllDifferent([grid[row][col] for row in range(9)])
    for box_row in range(3):
        for box_col in range(3):
            cells = [
                grid[3 * box_row + r][3 * box_col + c]
                for r in range(3)
                for c in range(3)
            ]
            model.AddAllDifferent(cells)
    # END sudoku_constraints


def solve() -> list[list[int]]:
    model = cp_model.CpModel()
    grid = build_variables(model)
    apply_givens(model, grid)
    add_constraints(model, grid)

    # BEGIN sudoku_solve
    solver = cp_model.CpSolver()
    solver.parameters.num_workers = 1
    solver.parameters.random_seed = 42
    status = solver.Solve(model)
    solution = [[solver.Value(cell) for cell in row] for row in grid]
    print(f"Status: {solver.StatusName(status)}")
    for row in solution:
        print(" ".join(str(value) for value in row))
    # END sudoku_solve
    return solution


if __name__ == "__main__":
    solve()
