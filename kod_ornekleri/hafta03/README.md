# Week 3 — Search I: Systematic Search

CP-SAT code examples for Week 3 (`brifler/hafta03-brif.md`). Units 1-3 of
this week's ders notu stay on paper (hand-worked backtracking traces and
figures); all code below belongs to Unit 4 — the CP-SAT search parameters
(decision strategies, worker count, time limit) that let a modeler observe
and steer the search loop Units 1-3 describe by hand. This week is CP-SAT
only (`ortools.sat.python.cp_model`); no MiniZinc, no Gurobi.

## Files

```
hafta03/
├── requirements.txt        unchanged from Week 1's pinned versions
├── modeller/
│   ├── search_stats.py      shared print_search_stats helper (all three
│   │                        problem files import it)
│   ├── graph_coloring.py    Petersen graph 3-colouring (10 nodes, 15 edges)
│   ├── magic_square.py      4x4 magic square (16 cells, magic constant 34)
│   └── langford.py          Langford pairs, n=7
├── ciktilar/                real, captured solver output (never fabricated)
│   ├── petersen-default-stats.txt
│   ├── petersen-ordered-stats.txt
│   ├── petersen-workers-stats.txt
│   ├── magicsquare4-default-stats.txt
│   ├── magicsquare4-ordered-stats.txt
│   ├── magicsquare4-solution.txt
│   ├── langford7-default-stats.txt
│   ├── langford7-ordered-stats.txt
│   ├── langford7-time-limited-stats.txt
│   └── langford7-solution.txt
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
../.venv/bin/python modeller/graph_coloring.py
../.venv/bin/python modeller/magic_square.py
../.venv/bin/python modeller/langford.py
```

To regenerate the captured outputs in `ciktilar/`:

```bash
PYTHONPATH=modeller ../.venv/bin/python -c \
    "import graph_coloring; graph_coloring.petersen_solve_default()" \
    > ciktilar/petersen-default-stats.txt
PYTHONPATH=modeller ../.venv/bin/python -c \
    "import graph_coloring; graph_coloring.petersen_solve_ordered()" \
    > ciktilar/petersen-ordered-stats.txt
PYTHONPATH=modeller ../.venv/bin/python -c "
import graph_coloring
print('num_search_workers=1'); graph_coloring.petersen_solve_workers(1)
print(); print('num_search_workers=8'); graph_coloring.petersen_solve_workers(8)
" > ciktilar/petersen-workers-stats.txt

PYTHONPATH=modeller ../.venv/bin/python -c \
    "import magic_square; magic_square.magicsquare_solve_default()" \
    > ciktilar/magicsquare4-default-stats.txt
PYTHONPATH=modeller ../.venv/bin/python -c \
    "import magic_square; magic_square.magicsquare_solve_ordered()" \
    > ciktilar/magicsquare4-ordered-stats.txt
PYTHONPATH=modeller ../.venv/bin/python -c \
    "import magic_square; magic_square.magicsquare_solve_default()" \
    > ciktilar/magicsquare4-solution.txt

PYTHONPATH=modeller ../.venv/bin/python -c \
    "import langford; langford.langford_solve_default()" \
    > ciktilar/langford7-default-stats.txt
PYTHONPATH=modeller ../.venv/bin/python -c \
    "import langford; langford.langford_solve_ordered()" \
    > ciktilar/langford7-ordered-stats.txt
PYTHONPATH=modeller ../.venv/bin/python -c \
    "import langford; langford.langford_time_limited()" \
    > ciktilar/langford7-time-limited-stats.txt
PYTHONPATH=modeller ../.venv/bin/python -c "
import langford
print('Sequence:', langford.langford_solve_default())
" > ciktilar/langford7-solution.txt
```

All `*_solve_default` / `*_solve_ordered` runs use `num_search_workers = 1`
and `random_seed = 42`, so CP-SAT's search order — and therefore the exact
branch/conflict counts printed — is deterministic across runs on the same
machine. The one deliberate exception is `petersen_solve_workers`, whose
whole point is to vary `num_search_workers` itself (1 vs 8) as a light
preview of CP-SAT's parallel portfolio (*why* it helps is Week 4's job);
its `WallTime` line is real wall-clock timing and can vary slightly run to
run.

`langford_time_limited` deliberately caps `max_time_in_seconds` far below
the ~2 ms this instance normally needs to solve to completion (see
`langford7-default-stats.txt`), so that the captured run is genuinely cut
short (`Status: UNKNOWN`). At this problem's tiny scale, model transfer and
presolve alone can consume the whole budget before the search even takes
its first branch — the captured `NumBranches: 0` is a real, honest result
of that, not an error.

`AddDecisionStrategy` only takes effect once
`solver.parameters.search_branching = cp_model.FIXED_SEARCH` is also set —
otherwise CP-SAT's automatic search silently ignores the forced strategy.
Every `*_solve_ordered` function below sets both.

## Notes

- `search_stats.py` is this week's contribution to next week's models —
  Week 4's brief reuses it as-is for reading search statistics, rather
  than re-deriving a printer helper from scratch.
- Graph coloring, magic square and Langford pairs are this week's first
  code; magic square was formulated on paper only in Week 1 Unit 3.
- Units 1-3 (backtracking, variable/value ordering, forward
  checking/MAC) are paper-only this week — no corresponding code files.
