"""Min-max fairness on the same 3-nurse, 2-day instance as
nurse_preferences.py. Each nurse's own penalty is the weighted sum of her
violated evening preferences. An auxiliary integer variable max_penalty is
constrained to be at least every nurse's penalty and is then minimized, so
the solver minimizes the worst-off nurse's penalty. Because several
schedules can share that min-max value, a second, lexicographic stage pins
it and breaks the tie by the total penalty.
"""

from ortools.sat.python import cp_model

from nurse_preferences import (
    DAYS,
    NURSES,
    PREFERENCE_WEIGHTS,
    add_hard_constraints,
    add_preference_vars,
    build_shift_vars,
)


def solve() -> tuple[int, int]:
    model = cp_model.CpModel()
    shift = build_shift_vars(model)
    add_hard_constraints(model, shift)
    pref_violated = add_preference_vars(model, shift)

    # BEGIN nurse_minmax_objective
    penalty = {
        nurse: sum(PREFERENCE_WEIGHTS[nurse] * pref_violated[nurse, day] for day in DAYS)
        for nurse in NURSES
    }
    upper = max(PREFERENCE_WEIGHTS.values()) * len(DAYS)
    max_penalty = model.NewIntVar(0, upper, "max_penalty")
    for nurse in NURSES:
        model.Add(max_penalty >= penalty[nurse])
    model.Minimize(max_penalty)
    # END nurse_minmax_objective

    solver = cp_model.CpSolver()
    solver.parameters.num_workers = 1
    solver.parameters.random_seed = 42

    # BEGIN nurse_minmax_tiebreak
    solver.Solve(model)
    m_star = solver.Value(max_penalty)
    total = sum(penalty.values())
    stage1 = [solver.Value(penalty[nurse]) for nurse in NURSES]
    print(f"Stage 1 min-max penalty: {m_star}, per nurse {stage1}")
    model.Add(max_penalty == m_star)
    model.Minimize(total)
    status = solver.Solve(model)
    print(f"Stage 2 status: {solver.StatusName(status)}")
    stage2 = [solver.Value(penalty[nurse]) for nurse in NURSES]
    print(f"Stage 2 per nurse {stage2}, total penalty {solver.Value(total)}")
    # END nurse_minmax_tiebreak
    return m_star, solver.Value(total)


if __name__ == "__main__":
    solve()
