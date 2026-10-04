"""SEND + MORE = MONEY: a classic CSP capstone exercise for Week 1's lab
sheet. This starter declares the eight letter variables and the
distinctness/leading-digit constraints; the arithmetic equation
SEND + MORE == MONEY is left for you to add (Lab Sheet, Step 8).
"""

from ortools.sat.python import cp_model

LETTERS = ["S", "E", "N", "D", "M", "O", "R", "Y"]


def build_model() -> tuple[cp_model.CpModel, dict[str, cp_model.IntVar]]:
    model = cp_model.CpModel()
    # BEGIN send_more_variables
    digit = {letter: model.NewIntVar(0, 9, letter) for letter in LETTERS}
    # END send_more_variables

    # BEGIN send_more_constraints
    model.AddAllDifferent(digit.values())
    model.Add(digit["S"] != 0)
    model.Add(digit["M"] != 0)
    # END send_more_constraints

    # TODO (Lab Step 8): add the constraint SEND + MORE == MONEY here,
    # as one linear expression over digit["S"], digit["E"], digit["N"], ...
    # (see the lab sheet for the positional-value pattern used by nqueens.py).

    return model, digit


def solve() -> tuple[int, dict[str, int]]:
    model, digit = build_model()
    solver = cp_model.CpSolver()
    solver.parameters.num_workers = 1
    solver.parameters.random_seed = 42
    status = solver.Solve(model)
    print(f"Status: {solver.StatusName(status)}")
    assignment = {}
    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        assignment = {letter: solver.Value(digit[letter]) for letter in LETTERS}
        print(f"Assignment: {assignment}")
    return status, assignment


if __name__ == "__main__":
    solve()
