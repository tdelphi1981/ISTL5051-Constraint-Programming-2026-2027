# Week 8 — Soft Constraints and Optimization

CP-SAT code examples for Week 8 (`brifler/hafta08-brif.md`). This week is
CP-SAT only (`ortools.sat.python.cp_model`); no MiniZinc, no Gurobi.

## Files

```
hafta08/
├── requirements.txt        pinned versions for this course (ortools, minizinc,
│                            pytest, gurobipy) — see ders-profili.md kod_dili
├── modeller/
│   ├── overconstrained_timetable.py   five-talk, two-slot Max-CSP/WCSP instance
│   ├── lexicographic_timetable.py     same instance, two-stage lexicographic solve
│   ├── pareto_front_demo.py           enumerates all candidates, filters Pareto front
│   ├── nurse_preferences.py           3-nurse, 2-day soft-preference roster
│   └── nurse_fairness.py              same roster, min-max penalty then total
├── ciktilar/                real, captured solver output (never fabricated)
│   ├── overconstrained-timetable-solution.txt
│   ├── lexicographic-timetable-solution.txt
│   ├── pareto-front-points.txt
│   ├── nurse-preferences-solution.txt
│   └── nurse-fairness-solution.txt
└── tests/
    └── test_models.py       pytest gate for the week
```

## Running

From this directory, using the course's shared virtual environment
(`kod_ornekleri/.venv`):

```bash
# run pytest gate
../.venv/bin/python -m pytest -q

# run a single model directly (prints to stdout)
../.venv/bin/python modeller/overconstrained_timetable.py
../.venv/bin/python modeller/lexicographic_timetable.py
../.venv/bin/python modeller/pareto_front_demo.py
../.venv/bin/python modeller/nurse_preferences.py
../.venv/bin/python modeller/nurse_fairness.py
```

To regenerate the captured outputs in `ciktilar/`:

```bash
../.venv/bin/python modeller/overconstrained_timetable.py \
    > ciktilar/overconstrained-timetable-solution.txt
../.venv/bin/python modeller/lexicographic_timetable.py \
    > ciktilar/lexicographic-timetable-solution.txt
../.venv/bin/python modeller/pareto_front_demo.py \
    > ciktilar/pareto-front-points.txt
../.venv/bin/python modeller/nurse_preferences.py \
    > ciktilar/nurse-preferences-solution.txt
../.venv/bin/python modeller/nurse_fairness.py \
    > ciktilar/nurse-fairness-solution.txt
```

All models use `solver.parameters.num_workers = 1` and a fixed
`random_seed`, so CP-SAT's search order — and therefore the exact
solution printed — is deterministic across runs.

## Model notes

- `overconstrained_timetable.py` extends Week 1 Unit 1's three-talk
  conference-scheduling CSP with T4 and T5. T1, T3 and T4 form a triangle
  of "must differ" pairs that cannot all hold with only two slots, so the
  proven optimum is exactly 1 violation.
- `lexicographic_timetable.py` imports `build_variables` and
  `add_violation_vars` from `overconstrained_timetable.py` and rebuilds a
  fresh model for stage 2 (a style choice for clarity: re-calling
  `Minimize` on the stage-1 model after adding the pin
  `total_violations == v1_star` would also work, and `nurse_fairness.py`
  does exactly that).
- `pareto_front_demo.py` reuses `build_variables` from
  `overconstrained_timetable.py` and Week 1 Unit 4's
  enumerate-all-solutions technique (`enumerate_all_solutions = True` with
  a `CpSolverSolutionCallback` subclass) to collect every one of the
  32 possible slot assignments as a `(violations, afternoon_count)` pair.
- `nurse_preferences.py` models a 3-nurse, 2-day, 2-shift roster. All
  three nurses would rather not work evenings, but both evening slots
  must be covered, so at least one preference is unavoidably violated;
  the weighted objective (`N1`=3, `N2`=2, `N3`=1) routes both evening
  shifts to `N3`, the cheapest violation, for a proven-optimal total
  penalty of 2.
- `nurse_fairness.py` reuses the same roster and builds one penalty
  expression per nurse. An auxiliary integer variable `max_penalty` is
  constrained to be at least every nurse's penalty and minimized (min-max
  fairness, optimum 2). Two schedules tie at 2 (`[0, 2, 1]`, total 3, and
  `[0, 0, 2]`, total 2), so a second stage pins `max_penalty == 2` on the
  same model and minimizes the total, returning `[0, 0, 2]`.

## Notes

- These five models are the last new CP-SAT content before Week 9's
  Midterm 1 Review; they deliberately reuse Week 1's talk-scheduling
  instance and Week 1 Unit 4's enumeration technique, plus Week 7's
  `model.Minimize()`/`model.Maximize()` vocabulary carried over from
  gurobipy into CP-SAT.
- `overconstrained_timetable.py` and `nurse_preferences.py` are the
  starting point for Week 12 (interval-variable scheduling) and Week 15
  (infeasibility diagnosis), which revisit the same two problem
  instances with different machinery.
