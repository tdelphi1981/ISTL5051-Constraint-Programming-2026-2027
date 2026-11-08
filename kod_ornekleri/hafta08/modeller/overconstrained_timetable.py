"""Five-talk, two-slot over-constrained timetabling instance (Max-CSP/WCSP):
extends Week 1 Unit 1's three-talk conference-scheduling CSP with two more
talks, T4 and T5. Slot 0 = morning, slot 1 = afternoon. Every listed pair
shares an author and should ideally land in different slots, but T1, T3
and T4 form a triangle of "must differ" pairs that cannot all be satisfied
with only two slots, so at least one pair is unavoidably violated.
"""

from ortools.sat.python import cp_model

TALKS = ["T1", "T2", "T3", "T4", "T5"]
PAIRS = [("T1", "T3"), ("T1", "T4"), ("T3", "T4"), ("T2", "T5")]
SLOT_NAMES = ["morning", "afternoon"]


def build_variables(model: cp_model.CpModel) -> dict[str, cp_model.IntVar]:
    # BEGIN overconstrained_variables
    slots = {talk: model.NewIntVar(0, 1, f"slot_{talk}") for talk in TALKS}
    return slots
    # END overconstrained_variables


def add_violation_vars(
    model: cp_model.CpModel, slots: dict[str, cp_model.IntVar]
) -> dict[tuple[str, str], cp_model.IntVar]:
    # BEGIN overconstrained_violation_vars
    violations = {}
    for talk_a, talk_b in PAIRS:
        viol = model.NewBoolVar(f"viol_{talk_a}_{talk_b}")
        model.Add(slots[talk_a] == slots[talk_b]).OnlyEnforceIf(viol)
        model.Add(slots[talk_a] != slots[talk_b]).OnlyEnforceIf(viol.Not())
        violations[(talk_a, talk_b)] = viol
    return violations
    # END overconstrained_violation_vars


def add_objective(
    model: cp_model.CpModel, violations: dict[tuple[str, str], cp_model.IntVar]
) -> cp_model.LinearExpr:
    # BEGIN overconstrained_objective
    weight = 1
    total_violations = sum(weight * viol for viol in violations.values())
    model.Minimize(total_violations)
    return total_violations
    # END overconstrained_objective


def solve() -> tuple[cp_model.CpSolver, dict[str, int], int]:
    model = cp_model.CpModel()
    slots = build_variables(model)
    violations = add_violation_vars(model, slots)
    total_violations = add_objective(model, violations)

    # BEGIN overconstrained_solve
    solver = cp_model.CpSolver()
    solver.parameters.num_workers = 1
    solver.parameters.random_seed = 42
    status = solver.Solve(model)
    assignment = {talk: solver.Value(slots[talk]) for talk in TALKS}
    total = solver.Value(total_violations)
    print(f"Status: {solver.StatusName(status)}")
    for talk in TALKS:
        print(f"{talk}: {SLOT_NAMES[assignment[talk]]}")
    print(f"Total violations: {total}")
    # END overconstrained_solve
    return solver, assignment, total


if __name__ == "__main__":
    solve()
