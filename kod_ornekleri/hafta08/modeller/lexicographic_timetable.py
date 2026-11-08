"""Two-stage lexicographic optimization on the same five-talk instance as
overconstrained_timetable.py. Stage 1 minimizes total violations (Unit 2's
objective, reused as-is). Stage 2 rebuilds the model, pins stage 1's
optimal violation count as a hard constraint, and only then minimizes a
second objective: the number of talks scheduled in the afternoon slot.
"""

from ortools.sat.python import cp_model

from overconstrained_timetable import (
    SLOT_NAMES,
    TALKS,
    add_violation_vars,
    build_variables,
)


def solve_stage1() -> int:
    model = cp_model.CpModel()
    slots = build_variables(model)
    violations = add_violation_vars(model, slots)
    total_violations = sum(violations.values())

    # BEGIN lex_stage1_solve
    model.Minimize(total_violations)
    solver = cp_model.CpSolver()
    solver.parameters.num_workers = 1
    solver.parameters.random_seed = 42
    solver.Solve(model)
    v1_star = solver.Value(total_violations)
    print(f"Stage 1 optimal total violations: {v1_star}")
    # END lex_stage1_solve
    return v1_star


def solve_stage2(v1_star: int) -> tuple[cp_model.CpSolver, dict[str, cp_model.IntVar], int]:
    model = cp_model.CpModel()
    slots = build_variables(model)
    violations = add_violation_vars(model, slots)
    total_violations = sum(violations.values())

    # BEGIN lex_stage2_pin
    model.Add(total_violations == v1_star)
    afternoon_count = sum(slots[talk] for talk in TALKS)
    # END lex_stage2_pin

    # BEGIN lex_stage2_solve
    model.Minimize(afternoon_count)
    solver = cp_model.CpSolver()
    solver.parameters.num_workers = 1
    solver.parameters.random_seed = 42
    solver.Solve(model)
    afternoon_star = solver.Value(afternoon_count)
    print(f"Stage 2 optimal afternoon count (violations pinned at {v1_star}): {afternoon_star}")
    for talk in TALKS:
        print(f"{talk}: {SLOT_NAMES[solver.Value(slots[talk])]}")
    # END lex_stage2_solve
    return solver, slots, afternoon_star


def solve() -> None:
    v1_star = solve_stage1()
    solve_stage2(v1_star)


if __name__ == "__main__":
    solve()
