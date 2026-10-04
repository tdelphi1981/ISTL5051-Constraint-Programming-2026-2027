"""Lab capstone: six review sessions each need one of six one-hour grading
slots, no two sessions sharing a slot -- a pure "everyone differs from
everyone" relation, unlike Week 1's map-coloring adjacency (see Unit 4's
Check Yourself Q4). The strong (AllDifferent) model is given; complete
the weak pairwise-!= model where the TODO says to, then run this file to
compare real solver statistics, exactly as nqueens_propagation_compare.py
did for N-queens.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "modeller"))

from ortools.sat.python import cp_model
from nqueens_propagation_compare import collect_solver_stats

N_SESSIONS = 6


def build_strong_model() -> tuple[cp_model.CpModel, list[cp_model.IntVar]]:
    model = cp_model.CpModel()
    sessions = [
        model.NewIntVar(0, N_SESSIONS - 1, f"session_{i}") for i in range(N_SESSIONS)
    ]
    model.AddAllDifferent(sessions)
    return model, sessions


def build_weak_model() -> tuple[cp_model.CpModel, list[cp_model.IntVar]]:
    model = cp_model.CpModel()
    sessions = [
        model.NewIntVar(0, N_SESSIONS - 1, f"session_{i}") for i in range(N_SESSIONS)
    ]
    # BEGIN exam_slots_weak_constraints
    # TODO: add one model.Add(sessions[i] != sessions[j]) constraint for
    # every pair i < j, the same way nqueens_weak_constraints does for
    # N-queens' column values in modeller/nqueens_models.py.
    # END exam_slots_weak_constraints
    return model, sessions


def report() -> dict[str, dict[str, object]]:
    strong_model, _ = build_strong_model()
    weak_model, _ = build_weak_model()
    stats = {
        "strong (AllDifferent)": collect_solver_stats(strong_model),
        "weak (pairwise !=)": collect_solver_stats(weak_model),
    }
    print(f"N={N_SESSIONS} exam-slot propagation-strength comparison")
    for label, s in stats.items():
        print(
            f"{label}: status={s['status']} branches={s['branches']} "
            f"conflicts={s['conflicts']} wall_time={s['wall_time']:.4f}s"
        )
    return stats


if __name__ == "__main__":
    report()
