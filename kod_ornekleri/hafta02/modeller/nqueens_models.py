"""N-queens CSP, two constraint layers over the same "one queen per row"
variables and diagonal transforms carried over unchanged from
hafta01/modeller/nqueens.py: a strong AllDifferent model (unchanged) and a
new weak pairwise-!= decomposition of the identical relation, for Unit 4's
propagation-strength comparison.
"""

from ortools.sat.python import cp_model


def nqueens_variables(model: cp_model.CpModel, n: int) -> list[cp_model.IntVar]:
    # BEGIN nqueens_variables
    queens = [model.NewIntVar(0, n - 1, f"queen_{row}") for row in range(n)]
    return queens
    # END nqueens_variables


def nqueens_strong_constraints(
    model: cp_model.CpModel, queens: list[cp_model.IntVar]
) -> None:
    n = len(queens)
    # BEGIN nqueens_strong_constraints
    model.AddAllDifferent(queens)
    model.AddAllDifferent([queens[i] + i for i in range(n)])
    model.AddAllDifferent([queens[i] - i for i in range(n)])
    # END nqueens_strong_constraints


def nqueens_weak_constraints(
    model: cp_model.CpModel, queens: list[cp_model.IntVar]
) -> None:
    n = len(queens)
    # BEGIN nqueens_weak_constraints
    for i in range(n):
        for j in range(i + 1, n):
            model.Add(queens[i] != queens[j])
            model.Add(queens[i] + i != queens[j] + j)
            model.Add(queens[i] - i != queens[j] - j)
    # END nqueens_weak_constraints


def build_strong_model(n: int) -> tuple[cp_model.CpModel, list[cp_model.IntVar]]:
    model = cp_model.CpModel()
    queens = nqueens_variables(model, n)
    nqueens_strong_constraints(model, queens)
    return model, queens


def build_weak_model(n: int) -> tuple[cp_model.CpModel, list[cp_model.IntVar]]:
    model = cp_model.CpModel()
    queens = nqueens_variables(model, n)
    nqueens_weak_constraints(model, queens)
    return model, queens


if __name__ == "__main__":
    strong_model, strong_queens = build_strong_model(8)
    solver = cp_model.CpSolver()
    solver.parameters.num_workers = 1
    solver.parameters.random_seed = 42
    solver.Solve(strong_model)
    print([solver.Value(q) for q in strong_queens])
