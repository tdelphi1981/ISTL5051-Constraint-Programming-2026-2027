# Week 7 — Modeling Languages II: The Mathematical Programming View

`gurobipy` code examples for Week 7 (`brifler/hafta07-brif.md`). This week
introduces linear and integer programs and Gurobi directly; no MiniZinc,
no CP-SAT script (Unit 4's CP-SAT sketch is words and API names only, not
a new script).

## Files

```
hafta07/
├── requirements.txt        pinned versions for this course (ortools, minizinc,
│                            pytest, gurobipy) — see ders-profili.md kod_dili
├── modeller/
│   ├── knapsack.py             Unit 1's A/B/C knapsack instance, solved as a
│   │                           binary IP and as its LP relaxation
│   ├── assignment.py           the four-worker/four-task assignment problem
│   └── production_planning.py  the three-product production-planning problem
├── ciktilar/                real, captured solver output (never fabricated)
│   ├── knapsack-ip-solution.txt
│   ├── knapsack-lp-relaxation.txt
│   ├── assignment-solution.txt
│   └── production-planning-solution.txt
└── tests/
    └── test_models.py       pytest gate for the week
```

## Gurobi licence

Gurobi 12.0.3 is installed, but no `~/gurobi.lic` is present on this
machine (the academic licence expired 2026-01-08 and was renamed to
`~/gurobi.lic.expired-2026-01-08`), so every model here runs on pip's
built-in restricted licence (at most 2000 variables and 2000 constraints,
valid until 2026-11-23). None of this week's models set
`GRB_LICENSE_FILE` or any other Gurobi environment variable, and every
model stays at single-digit variable/constraint counts, far under the
restricted-licence limit — the same code keeps working unchanged once the
licence is renewed. The "Restricted license" banner Gurobi prints at the
start of `optimize()`'s log is expected, real output, captured verbatim
in `ciktilar/production-planning-solution.txt`.

## Running

From this directory, using the course's shared virtual environment
(`kod_ornekleri/.venv`):

```bash
# run pytest gate
../.venv/bin/python -m pytest -q

# run a single model directly (prints to stdout)
../.venv/bin/python modeller/knapsack.py
../.venv/bin/python modeller/assignment.py
../.venv/bin/python modeller/production_planning.py
```

To regenerate the captured outputs in `ciktilar/`:

```bash
PYTHONPATH=modeller ../.venv/bin/python -c "import knapsack; knapsack.solve_ip()" \
    > ciktilar/knapsack-ip-solution.txt
PYTHONPATH=modeller ../.venv/bin/python -c "import knapsack; knapsack.solve_lp_relaxation()" \
    > ciktilar/knapsack-lp-relaxation.txt
PYTHONPATH=modeller ../.venv/bin/python -c "import assignment; assignment.solve()" \
    > ciktilar/assignment-solution.txt
PYTHONPATH=modeller ../.venv/bin/python -c "import production_planning; production_planning.solve()" \
    > ciktilar/production-planning-solution.txt
```

## Notes

- `knapsack.py`'s IP solve reports optimal value 8 and its LP relaxation
  reports 8.25, matching Unit 1's hand-worked instance exactly (item C
  fractional at 0.25).
- `assignment.py`'s optimal total cost is 14, on the cost matrix's
  diagonal (W1-Ta, W2-Tb, W3-Tc, W4-Td), matching Unit 3's hand-verifiable
  claim.
- `production_planning.py`'s optimal plan and profit are not hand-derived
  anywhere in the brief; read them from
  `ciktilar/production-planning-solution.txt`.
- All three problems (knapsack, assignment, production planning) return in
  Week 10 for a full sensitivity report built on this same code.
