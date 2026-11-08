"""3-nurse, 2-day, 2-shift-per-day (morning/evening) nurse-preference
instance. Hard rules stay hard: every shift-slot needs exactly one nurse,
and no nurse works two shifts on the same day. All three nurses would
rather not work evenings (N1 strongly, N2 mildly, N3 barely), but the two
evening slots must be covered by someone, so at least one nurse's
preference is unavoidably violated. Each stated preference becomes a
reified penalty term, and the weighted objective picks the cheapest
nurse(s) to carry that unavoidable violation.
"""

from ortools.sat.python import cp_model

NURSES = ["N1", "N2", "N3"]
DAYS = ["Mon", "Tue"]
SHIFT_TYPES = ["morning", "evening"]
PREFERENCE_WEIGHTS = {"N1": 3, "N2": 2, "N3": 1}


def build_shift_vars(model: cp_model.CpModel) -> dict[tuple[str, str, str], cp_model.IntVar]:
    return {
        (nurse, day, shift): model.NewBoolVar(f"shift_{nurse}_{day}_{shift}")
        for nurse in NURSES
        for day in DAYS
        for shift in SHIFT_TYPES
    }


def add_hard_constraints(
    model: cp_model.CpModel, shift: dict[tuple[str, str, str], cp_model.IntVar]
) -> None:
    # BEGIN nurse_hard_constraints
    for day in DAYS:
        for shift_type in SHIFT_TYPES:
            model.Add(sum(shift[nurse, day, shift_type] for nurse in NURSES) == 1)
    for nurse in NURSES:
        for day in DAYS:
            model.Add(sum(shift[nurse, day, shift_type] for shift_type in SHIFT_TYPES) <= 1)
    # END nurse_hard_constraints


def add_preference_vars(
    model: cp_model.CpModel, shift: dict[tuple[str, str, str], cp_model.IntVar]
) -> dict[tuple[str, str], cp_model.IntVar]:
    # BEGIN nurse_preference_vars
    pref_violated = {}
    for nurse in NURSES:
        for day in DAYS:
            violated = model.NewBoolVar(f"pref_violated_{nurse}_{day}")
            model.Add(shift[nurse, day, "evening"] == 1).OnlyEnforceIf(violated)
            model.Add(shift[nurse, day, "evening"] == 0).OnlyEnforceIf(violated.Not())
            pref_violated[(nurse, day)] = violated
    return pref_violated
    # END nurse_preference_vars


def add_objective(
    model: cp_model.CpModel, pref_violated: dict[tuple[str, str], cp_model.IntVar]
) -> cp_model.LinearExpr:
    # BEGIN nurse_objective
    total_penalty = sum(
        PREFERENCE_WEIGHTS[nurse] * violated for (nurse, _day), violated in pref_violated.items()
    )
    model.Minimize(total_penalty)
    return total_penalty
    # END nurse_objective


def solve() -> tuple[cp_model.CpSolver, dict[tuple[str, str, str], cp_model.IntVar], int]:
    model = cp_model.CpModel()
    shift = build_shift_vars(model)
    add_hard_constraints(model, shift)
    pref_violated = add_preference_vars(model, shift)
    total_penalty = add_objective(model, pref_violated)

    # BEGIN nurse_solve
    solver = cp_model.CpSolver()
    solver.parameters.num_workers = 1
    solver.parameters.random_seed = 42
    status = solver.Solve(model)
    print(f"Status: {solver.StatusName(status)}")
    for nurse in NURSES:
        row = []
        for day in DAYS:
            worked = [s for s in SHIFT_TYPES if solver.Value(shift[nurse, day, s])]
            row.append(f"{day}:{worked[0] if worked else 'off'}")
        print(f"{nurse}: {'  '.join(row)}")
    print(f"Total penalty: {solver.Value(total_penalty)}")
    # END nurse_solve
    return solver, shift, solver.Value(total_penalty)


if __name__ == "__main__":
    solve()
