# Week 1 — Constraint Satisfaction Problems: A Formal Definition

CP-SAT code examples for Week 1 (`brifler/hafta01-brif.md`). This week is
CP-SAT only (`ortools.sat.python.cp_model`); no MiniZinc, no Gurobi.

## Files

```
hafta01/
├── requirements.txt        pinned versions for this course (ortools, minizinc,
│                            pytest, gurobipy) — see ders-profili.md kod_dili
├── modeller/
│   ├── csp_basics.py        a tiny 3-region "triangle" toy CSP
│   ├── nqueens.py            N-queens ("one queen per row" viewpoint)
│   ├── sudoku.py              9x9 Sudoku with a fixed puzzle's givens
│   └── map_coloring.py        the Australia map-coloring instance
├── ciktilar/                real, captured solver output (never fabricated)
│   ├── nqueens-8-solution.txt
│   ├── nqueens-6-count.txt
│   ├── sudoku-solution.txt
│   └── mapcoloring-solution.txt
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
../.venv/bin/python modeller/csp_basics.py
../.venv/bin/python modeller/nqueens.py
../.venv/bin/python modeller/sudoku.py
../.venv/bin/python modeller/map_coloring.py
```

To regenerate the captured outputs in `ciktilar/`:

```bash
PYTHONPATH=modeller ../.venv/bin/python -c "import nqueens; nqueens.solve_one(8)" \
    > ciktilar/nqueens-8-solution.txt
PYTHONPATH=modeller ../.venv/bin/python -c "import nqueens; nqueens.enumerate_solutions(6)" \
    > ciktilar/nqueens-6-count.txt
PYTHONPATH=modeller ../.venv/bin/python -c "import sudoku; sudoku.solve()" \
    > ciktilar/sudoku-solution.txt
PYTHONPATH=modeller ../.venv/bin/python -c "import map_coloring; map_coloring.solve()" \
    > ciktilar/mapcoloring-solution.txt
```

All models use `solver.parameters.num_workers = 1` and a fixed
`random_seed`, so CP-SAT's search order — and therefore the exact
solution printed — is deterministic across runs.

## Notes

- `nqueens.py` and `map_coloring.py` are the starting point for Week 2
  (Constraint Propagation), which reuses these exact models.
- Magic square is a paper example only this week (Unit 3); its CP-SAT
  code starts in Week 3.
