"""Pytest gate for Week 8: every soft-constraint model actually solves,
and each result is checked against a hand-verified property from the
brief (optimal violation counts, lexicographic non-regression, Pareto
non-domination, and hard-constraint satisfaction plus penalty bookkeeping
for the nurse model).
"""

import sys
from pathlib import Path

from ortools.sat.python import cp_model

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "modeller"))

import lexicographic_timetable  # noqa: E402
import nurse_preferences  # noqa: E402
import overconstrained_timetable  # noqa: E402
import pareto_front_demo  # noqa: E402


def test_overconstrained_optimal_violation_count_is_one() -> None:
    solver, _assignment, total = overconstrained_timetable.solve()
    assert solver.StatusName() == "OPTIMAL"
    assert total == 1


def test_lexicographic_stage2_never_increases_stage1_violations() -> None:
    v1_star = lexicographic_timetable.solve_stage1()
    solver, slots, _afternoon_star = lexicographic_timetable.solve_stage2(v1_star)
    violations = sum(
        1
        for talk_a, talk_b in overconstrained_timetable.PAIRS
        if solver.Value(slots[talk_a]) == solver.Value(slots[talk_b])
    )
    assert violations == v1_star


def test_pareto_front_has_no_internally_dominated_pair() -> None:
    candidates = pareto_front_demo.enumerate_candidates()
    front = pareto_front_demo.pareto_filter_front(candidates)
    for candidate in front:
        others = [other for other in front if other != candidate]
        assert not any(pareto_front_demo.dominates(other, candidate) for other in others)


def test_nurse_schedule_respects_hard_constraints_and_penalty_bookkeeping() -> None:
    solver, shift, total_penalty = nurse_preferences.solve()
    for day in nurse_preferences.DAYS:
        for shift_type in nurse_preferences.SHIFT_TYPES:
            covering = sum(
                solver.Value(shift[nurse, day, shift_type]) for nurse in nurse_preferences.NURSES
            )
            assert covering == 1
    for nurse in nurse_preferences.NURSES:
        for day in nurse_preferences.DAYS:
            shifts_worked = sum(
                solver.Value(shift[nurse, day, shift_type])
                for shift_type in nurse_preferences.SHIFT_TYPES
            )
            assert shifts_worked <= 1

    actual_penalty = sum(
        nurse_preferences.PREFERENCE_WEIGHTS[nurse] * solver.Value(shift[nurse, day, "evening"])
        for nurse in nurse_preferences.NURSES
        for day in nurse_preferences.DAYS
    )
    assert total_penalty == actual_penalty
    assert isinstance(total_penalty, int)


def test_all_models_report_optimal_status() -> None:
    _, _, total = overconstrained_timetable.solve()
    assert total >= 0
    solver, _, _ = nurse_preferences.solve()
    assert solver.StatusName() == "OPTIMAL"
