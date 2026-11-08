"""Lab starter: re-run modeller/nurse_preferences.py's 3-nurse, 2-day
roster with one preference weight changed. The hard constraints, the
preference reification and the objective are all reused unchanged from
modeller/nurse_preferences.py; only NURSE_LAB_WEIGHTS below is meant to
be edited.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "modeller"))

from ortools.sat.python import cp_model
from nurse_preferences import (
    DAYS,
    NURSES,
    SHIFT_TYPES,
    add_hard_constraints,
    add_preference_vars,
    build_shift_vars,
)

# BEGIN nurse_lab_weight_change
# Original weights (modeller/nurse_preferences.py): {"N1": 3, "N2": 2, "N3": 1}.
# Edit N3's weight below, then re-run, to see the schedule change.
NURSE_LAB_WEIGHTS = {"N1": 3, "N2": 2, "N3": 1}
# END nurse_lab_weight_change


def solve() -> None:
    model = cp_model.CpModel()
    shift = build_shift_vars(model)
    add_hard_constraints(model, shift)
    pref_violated = add_preference_vars(model, shift)

    total_penalty = sum(
        NURSE_LAB_WEIGHTS[nurse] * violated for (nurse, _day), violated in pref_violated.items()
    )
    model.Minimize(total_penalty)

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


if __name__ == "__main__":
    solve()
