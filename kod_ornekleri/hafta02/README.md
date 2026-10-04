# Week 2 — Constraint Propagation

CP-SAT code examples for Week 2 (`brifler/hafta02-brif.md`). This week is
still CP-SAT only (`ortools.sat.python.cp_model`); no MiniZinc, no Gurobi.
`ac3.py` is pure Python (no solver) — it implements AC-3 by hand to make
Unit 2's worked trace independently checkable.

## Files

```
hafta02/
├── requirements.txt                 pinned versions for this course, unchanged
│                                      from Week 1 — see ders-profili.md kod_dili
├── modeller/
│   ├── ac3.py                        pure-Python AC-3 on Unit 2's X<Y<Z chain CSP
│   ├── nqueens_models.py             strong (AllDifferent) and weak (pairwise !=)
│   │                                  N-queens models, variables/diagonals carried
│   │                                  over unchanged from hafta01/modeller/nqueens.py
│   ├── nqueens_propagation_compare.py  solves both models, compares solver stats
│   ├── map_coloring_models.py        Australia map coloring, carried over
│   │                                  unchanged from hafta01/modeller/map_coloring.py
│   └── global_constraints_demo.py    Element/Table/Circuit/Cumulative toy demos
├── ciktilar/                         real, captured solver output (never fabricated)
│   ├── ac3-trace.txt
│   ├── nqueens-propagation-stats.txt
│   ├── element-demo.txt
│   ├── table-demo.txt
│   ├── circuit-demo.txt
│   └── cumulative-demo.txt
└── tests/
    └── test_models.py                pytest gate for the week
```

## Running

From this directory, using the course's shared virtual environment
(`kod_ornekleri/.venv`):

```bash
# run pytest gate
../.venv/bin/python -m pytest -q

# run a single model directly (prints to stdout)
PYTHONPATH=modeller ../.venv/bin/python -c "import ac3; ac3.run()"
PYTHONPATH=modeller ../.venv/bin/python -c \
    "from nqueens_propagation_compare import propagation_comparison_report as r; r(8); r(20)"
PYTHONPATH=modeller ../.venv/bin/python -c "import global_constraints_demo as g; g.element_demo()"
PYTHONPATH=modeller ../.venv/bin/python -c "import global_constraints_demo as g; g.table_demo()"
PYTHONPATH=modeller ../.venv/bin/python -c "import global_constraints_demo as g; g.circuit_demo()"
PYTHONPATH=modeller ../.venv/bin/python -c "import global_constraints_demo as g; g.cumulative_demo()"
```

To regenerate the captured outputs in `ciktilar/`:

```bash
PYTHONPATH=modeller ../.venv/bin/python -c "import ac3; ac3.run()" \
    > ciktilar/ac3-trace.txt
PYTHONPATH=modeller ../.venv/bin/python -c \
    "from nqueens_propagation_compare import propagation_comparison_report as r; r(8); r(20)" \
    > ciktilar/nqueens-propagation-stats.txt
PYTHONPATH=modeller ../.venv/bin/python -c "import global_constraints_demo as g; g.element_demo()" \
    > ciktilar/element-demo.txt
PYTHONPATH=modeller ../.venv/bin/python -c "import global_constraints_demo as g; g.table_demo()" \
    > ciktilar/table-demo.txt
PYTHONPATH=modeller ../.venv/bin/python -c "import global_constraints_demo as g; g.circuit_demo()" \
    > ciktilar/circuit-demo.txt
PYTHONPATH=modeller ../.venv/bin/python -c "import global_constraints_demo as g; g.cumulative_demo()" \
    > ciktilar/cumulative-demo.txt
```

All CP-SAT solves use `solver.parameters.num_workers = 1` and a fixed
`random_seed`, so search order — and therefore the exact statistics and
solutions printed — is deterministic across runs.

## Notes

- `nqueens_models.py` and `map_coloring_models.py` start from Week 1's
  `nqueens.py` and `map_coloring.py`: variable declarations and diagonal
  transforms are carried over unchanged; only the constraint layer differs
  (`nqueens_models.py` adds a new weak pairwise-`!=` decomposition
  alongside the unchanged strong `AllDifferent` model).
- `nqueens-propagation-stats.txt` reports both `N=8` and `N=20`: at `N=8`
  the gap between the strong and weak model is already real but modest
  (475 vs. 518 branches); `N=20` is included per the brief's honest-caveat
  note to show the same direction at larger scale, not because the `N=8`
  gap was negligible.
- `map_coloring_models.py` is not re-solved with a new propagation
  comparison this week (map coloring's adjacency relation is not an
  "all-different-from-everyone" relation, so it is not a valid
  `AllDifferent`-vs-pairwise comparison); it is reused only as Unit 4's
  Check Yourself Q4 scenario.
- `nqueens_models.py` and `nqueens_propagation_compare.py` are the starting
  point for Week 3 (Search I), which reuses the strong model unchanged and
  the weak model as a deliberate contrast.
