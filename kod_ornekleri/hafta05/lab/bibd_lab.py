"""Capstone lab starter: the Fano-plane BIBD (7,7,3,3,1), reusing
modeller/bibd.py's variables, pairwise-lambda constraints and column
symmetry breaking unchanged. Your task is to add one further
lexicographic-ordering constraint, this time between adjacent point-rows,
and confirm the result is still a valid design with search statistics no
worse than the column-only symmetry-broken version.
"""

import sys
from pathlib import Path

from ortools.sat.python import cp_model

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "modeller"))

import bibd  # noqa: E402


# BEGIN bibd_lab_row_symmetry_todo
def add_row_symmetry_breaking(model: cp_model.CpModel, x) -> None:
    """TODO: force every pair of adjacent point-rows into non-decreasing
    lexicographic order -- the same recipe bibd.add_symmetry_breaking
    already applies to adjacent block-columns, reindexed to point-rows.
    """
    raise NotImplementedError("add the row lexicographic-ordering constraint here")
# END bibd_lab_row_symmetry_todo


def solve_and_report_with_row_and_column_breaking():
    model = cp_model.CpModel()
    x = bibd.build_variables(model)
    bibd.add_pairwise_lambda_constraints(model, x)
    bibd.add_symmetry_breaking(model, x)
    add_row_symmetry_breaking(model, x)

    solver = cp_model.CpSolver()
    solver.parameters.num_workers = 1
    solver.parameters.random_seed = 42
    status = solver.Solve(model)
    print(f"Status: {solver.StatusName(status)}")
    print(f"NumBranches: {solver.NumBranches()}")
    print(f"NumConflicts: {solver.NumConflicts()}")
    print(f"WallTime: {solver.WallTime():.6f}")
    design = None
    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        design = [
            [solver.Value(x[point, block]) for block in range(bibd.NUM_BLOCKS)]
            for point in range(bibd.NUM_POINTS)
        ]
    return status, design


if __name__ == "__main__":
    solve_and_report_with_row_and_column_breaking()
