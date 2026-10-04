"""Shared helper, imported by every problem file this week: prints CP-SAT's
own search statistics after a solve, so each problem file only calls one
function instead of repeating the same four print statements.
"""

from ortools.sat.python import cp_model


def print_search_stats(solver: cp_model.CpSolver, status: int) -> None:
    # BEGIN print_search_stats
    print(f"Status: {solver.StatusName(status)}")
    print(f"NumBranches: {solver.NumBranches()}")
    print(f"NumConflicts: {solver.NumConflicts()}")
    print(f"WallTime: {solver.WallTime():.4f}")
    # END print_search_stats
