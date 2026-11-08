"""Lab starter: extend overconstrained_timetable.py's five-talk instance
with one more shared-author pair, T2 and T4. The original four pairs are
reified exactly as in modeller/overconstrained_timetable.py (reused
unchanged); the new pair's reification below is deliberately incomplete —
only the forward direction is wired up, and the reverse direction is left
as a TODO. Fill in the missing call, then re-run and compare both the
reported total and the diagnostic lines at the bottom of the output.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "modeller"))

from ortools.sat.python import cp_model
from overconstrained_timetable import PAIRS, SLOT_NAMES, TALKS, build_variables


def add_original_violation_vars(
    model: cp_model.CpModel, slots: dict[str, cp_model.IntVar]
) -> dict[tuple[str, str], cp_model.IntVar]:
    # BEGIN extra_pair_setup
    violations = {}
    for talk_a, talk_b in PAIRS:
        viol = model.NewBoolVar(f"viol_{talk_a}_{talk_b}")
        model.Add(slots[talk_a] == slots[talk_b]).OnlyEnforceIf(viol)
        model.Add(slots[talk_a] != slots[talk_b]).OnlyEnforceIf(viol.Not())
        violations[(talk_a, talk_b)] = viol
    return violations
    # END extra_pair_setup


def add_new_pair_violation_var(
    model: cp_model.CpModel, slots: dict[str, cp_model.IntVar]
) -> cp_model.IntVar:
    # BEGIN extra_pair_broken
    viol_t2_t4 = model.NewBoolVar("viol_T2_T4")
    model.Add(slots["T2"] == slots["T4"]).OnlyEnforceIf(viol_t2_t4)
    # TODO: add the missing reverse direction, the same way
    # add_original_violation_vars does for every other pair above:
    # model.Add(slots["T2"] != slots["T4"]).OnlyEnforceIf(viol_t2_t4.Not())
    return viol_t2_t4
    # END extra_pair_broken


def solve() -> None:
    model = cp_model.CpModel()
    slots = build_variables(model)
    violations = add_original_violation_vars(model, slots)
    viol_t2_t4 = add_new_pair_violation_var(model, slots)
    violations[("T2", "T4")] = viol_t2_t4

    total_violations = sum(violations.values())
    model.Minimize(total_violations)

    # BEGIN extra_pair_solve
    solver = cp_model.CpSolver()
    solver.parameters.num_workers = 1
    solver.parameters.random_seed = 42
    status = solver.Solve(model)
    print(f"Status: {solver.StatusName(status)}")
    for talk in TALKS:
        print(f"{talk}: {SLOT_NAMES[solver.Value(slots[talk])]}")
    print(f"Total violations (reported): {solver.Value(total_violations)}")
    actual_clash = solver.Value(slots["T2"]) == solver.Value(slots["T4"])
    print(f"T2, T4 actually in the same slot: {actual_clash}")
    print(f"viol_T2_T4 recorded by the solver: {solver.Value(viol_t2_t4)}")
    # END extra_pair_solve


if __name__ == "__main__":
    solve()
