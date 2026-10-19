# Week 5 — Tractable Structure and Symmetry

CP-SAT code examples for Week 5 (`brifler/hafta05-brif.md`). This week is
CP-SAT only (`ortools.sat.python.cp_model`); no MiniZinc, no Gurobi.

## Files

```
hafta05/
├── requirements.txt        pinned versions for this course (unchanged
│                            from Week 1's pin — see ders-profili.md kod_dili)
├── modeller/
│   ├── tree_csp.py            a genuine tree-shaped 5-region map-coloring
│   │                           instance; hand-coded directional arc
│   │                           consistency (DAC) plus a backtrack-free
│   │                           forward assignment, cross-checked against
│   │                           a plain CP-SAT solve of the same instance
│   ├── treewidth.py            pure-Python induced-width calculator (no
│   │                            networkx — not part of this course's
│   │                            pinned environment), applied to Unit 1's
│   │                            tree and Unit 2's worked cutset example
│   ├── social_golfer.py        3 groups of 3 golfers, 4 weeks, modeled
│   │                            with and without lexicographic-ordering
│   │                            symmetry-breaking constraints
│   └── bibd.py                 the Fano-plane BIBD (7,7,3,3,1), modeled
│                                with and without a column lexicographic-
│                                ordering symmetry-breaking constraint
├── ciktilar/                real, captured solver output (never fabricated)
│   ├── tree-csp-dac-trace.txt
│   ├── treewidth-tree-example.txt
│   ├── treewidth-cutset-example.txt
│   ├── golfer-no-symmetry-break.txt
│   ├── golfer-with-symmetry-break.txt
│   ├── bibd-no-symmetry-break.txt
│   └── bibd-with-symmetry-break.txt
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
../.venv/bin/python modeller/tree_csp.py
../.venv/bin/python modeller/treewidth.py
../.venv/bin/python modeller/social_golfer.py
../.venv/bin/python modeller/bibd.py
```

To regenerate the captured outputs in `ciktilar/`:

```bash
../.venv/bin/python modeller/tree_csp.py > ciktilar/tree-csp-dac-trace.txt

PYTHONPATH=modeller ../.venv/bin/python -c \
    "import treewidth; treewidth.treewidth_tree_example()" \
    > ciktilar/treewidth-tree-example.txt
PYTHONPATH=modeller ../.venv/bin/python -c \
    "import treewidth; treewidth.treewidth_cutset_example()" \
    > ciktilar/treewidth-cutset-example.txt

PYTHONPATH=modeller ../.venv/bin/python -c \
    "import social_golfer; social_golfer.solve_and_report(False)" \
    > ciktilar/golfer-no-symmetry-break.txt
PYTHONPATH=modeller ../.venv/bin/python -c \
    "import social_golfer; social_golfer.solve_and_report(True)" \
    > ciktilar/golfer-with-symmetry-break.txt

PYTHONPATH=modeller ../.venv/bin/python -c \
    "import bibd; bibd.solve_and_report(False)" \
    > ciktilar/bibd-no-symmetry-break.txt
PYTHONPATH=modeller ../.venv/bin/python -c \
    "import bibd; bibd.solve_and_report(True)" \
    > ciktilar/bibd-with-symmetry-break.txt
```

All models use `solver.parameters.num_workers = 1` and a fixed
`random_seed`, so CP-SAT's search order — and therefore the exact search
statistics printed — is deterministic across runs (wall-clock time still
varies slightly run to run; the branch/conflict counts do not).

## Design decisions

- **No `AddLexicographic`-style API in this pinned OR-Tools version.**
  Checked directly against the installed `ortools==9.14.6206`: `dir(
  cp_model.CpModel)` contains no method with `Lex` in its name. Both
  `social_golfer.py` and `bibd.py` therefore hand-roll a sequential
  lexicographic-`<=` constraint (`_add_lex_le`, private helper, duplicated
  in both files rather than adding a shared module outside the brief's
  planned file layout): for two equal-length sequences of linear
  expressions, position `i` is only forced `left[i] <= right[i]` while
  every earlier position is already forced equal (a reified `==` per
  position, chained via `OnlyEnforceIf`) — exactly the definition of
  lexicographic order, and sound/complete by construction (verified with
  the pytest gate's design-validity checks below, and by the branch/
  conflict counts in `ciktilar/` dropping between the two variants, never
  eliminating the feasible design).
- **Social golfer's symmetry breaking is intentionally partial.** Week 1's
  grouping is fully canonicalized (golfer `g` starts in group `g //
  GROUP_SIZE`); for every other week the golfer with globally smallest id
  is pinned to group 0 (one instance of "groups ordered by smallest
  golfer id"); and weeks after week 1 are lexicographically ordered
  against each other. This does not break every last redundant symmetry
  (e.g. groups 1 and 2 within a non-canonical week can still be relabeled
  against each other) — it is illustrative of the technique, not a
  competition-grade symmetry-breaking set, consistent with this week's
  scope (Unit 4: name and apply the lexicographic-ordering idea, not
  engineer an exhaustive symmetry group quotient).

## Notes

- `tree_csp.py`'s instance is deliberately tree-shaped, contrasted with
  Week 1's cyclic Australia map-coloring instance (`kod_ornekleri/hafta01/
  modeller/map_coloring.py`), which has a WA–NT–SA triangle.
- Social golfer's `3 groups of 3, 4 weeks` instance is this configuration's
  maximum: 4 weeks × 3 groups × C(3, 2) = 36 pairs meeting, exactly
  C(9, 2) = 36 total pairs, so a feasible schedule uses every pair exactly
  once (confirmed by the pytest gate).
- No later week reuses social golfer or BIBD (problem pool table, design
  doc §4); both remain in scope only this week.
