"""N-queens CSP, "one queen per row" viewpoint (Unit 2's Viewpoint A):
one integer variable per row, its value is the column of that row's
queen. Domains are 0-indexed columns (0..N-1).
"""

from ortools.sat.python import cp_model


def build_model(n: int) -> tuple[cp_model.CpModel, list[cp_model.IntVar]]:
    model = cp_model.CpModel()
    # BEGIN nqueens_variables
    queens = [model.NewIntVar(0, n - 1, f"queen_{row}") for row in range(n)]
    # END nqueens_variables

    # BEGIN nqueens_constraints
    model.AddAllDifferent(queens)
    model.AddAllDifferent([queens[i] + i for i in range(n)])
    model.AddAllDifferent([queens[i] - i for i in range(n)])
    # END nqueens_constraints
    return model, queens


class SolutionCounter(cp_model.CpSolverSolutionCallback):
    """Counts every complete solution found during enumeration."""

    def __init__(self) -> None:
        super().__init__()
        self._count = 0

    def OnSolutionCallback(self) -> None:
        self._count += 1

    @property
    def count(self) -> int:
        return self._count


def solve_one(n: int) -> list[int]:
    model, queens = build_model(n)

    # BEGIN nqueens_solve_one
    solver = cp_model.CpSolver()
    solver.parameters.num_workers = 1
    solver.parameters.random_seed = 42
    status = solver.Solve(model)
    columns = [solver.Value(queen) for queen in queens]
    print(f"Status: {solver.StatusName(status)}")
    print(f"Columns per row (0-indexed) for N={n}: {columns}")
    # END nqueens_solve_one
    return columns


def enumerate_solutions(n: int) -> int:
    model, _ = build_model(n)

    # BEGIN nqueens_enumerate
    solver = cp_model.CpSolver()
    solver.parameters.num_workers = 1
    solver.parameters.enumerate_all_solutions = True
    callback = SolutionCounter()
    solver.Solve(model, callback)
    print(f"Number of solutions for N={n}: {callback.count}")
    # END nqueens_enumerate
    return callback.count


if __name__ == "__main__":
    solve_one(8)
    enumerate_solutions(6)
