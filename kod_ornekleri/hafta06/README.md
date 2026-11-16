# Week 6 — Modeling Languages I: MiniZinc and Solver Independence

Code examples for Week 6 (`brifler/hafta06-brif.md`). This week introduces
the MiniZinc modeling language and shows the same `.mzn` model running,
unchanged, on more than one solver backend.

## Files

```
hafta06/
├── requirements.txt          same pins as Week 1 (ortools, minizinc==0.10.0,
│                              gurobipy, pytest) — no new Python package this week
├── minizinc/
│   ├── kp01.mzn/.dzn          0/1 knapsack (Unit 1's running example; not
│   │                          named knapsack.mzn, which is a stdlib global)
│   ├── nqueens.mzn/.dzn       N-queens rewritten in MiniZinc (Unit 2's flattening example)
│   └── assignment.mzn/.dzn    the assignment problem (Unit 3's solver-independence example)
├── modeller/
│   └── minizinc_python.py     Unit 4's running example: drives MiniZinc from Python
├── ciktilar/                  real, captured solver output (never fabricated)
│   ├── kp01-gecode.txt
│   ├── nqueens-flatzinc-excerpt.txt
│   ├── nqueens-flatzinc-highs-counts.txt
│   ├── assignment-gecode.txt
│   ├── assignment-coinbc.txt
│   ├── assignment-gurobi.txt
│   ├── assignment-highs.txt
│   ├── minizinc-python-run.txt
│   └── solver-runtime.csv
└── tests/
    └── test_models.py         pytest gate for the week
```

## Installing the MiniZinc CLI (macOS/Homebrew)

This week's one new dependency is the MiniZinc binary itself, not a `pip`
package:

```bash
brew install minizinc
minizinc --version   # expect: MiniZinc to FlatZinc converter, version 2.10.1
minizinc --solvers    # inventory of installed solver targets
```

The HiGHS MIP backend needs a second Homebrew package plus a one-time
MiniZinc preference pointing at its library, since MiniZinc's own HiGHS
plugin does not bundle HiGHS itself:

```bash
brew install highs   # provides /opt/homebrew/lib/libhighs.dylib
```

Add the following to `~/.minizinc/Preferences.json` (create the file if
it does not already exist):

```json
{
  "solverDefaults": [
    ["org.minizinc.mip.highs", "--highs-dll", "/opt/homebrew/lib/libhighs.dylib"]
  ]
}
```

Verify with `minizinc --solver HiGHS minizinc/assignment.mzn
minizinc/assignment.dzn` — it should report `total cost: 13`, the same
optimal cost Gecode and COIN-BC report.

## Running

From this directory, using the course's shared virtual environment
(`kod_ornekleri/.venv`):

```bash
# run pytest gate
../.venv/bin/python -m pytest -q

# run a MiniZinc model directly on Gecode
minizinc --solver Gecode minizinc/kp01.mzn minizinc/kp01.dzn

# compile (flatten) a model without solving it
minizinc --compile -o /tmp/nqueens.fzn --solver Gecode minizinc/nqueens.mzn minizinc/nqueens.dzn

# run the Unit 4 Python-driven comparison
../.venv/bin/python modeller/minizinc_python.py
```

To regenerate the captured outputs in `ciktilar/`:

```bash
minizinc --solver Gecode minizinc/kp01.mzn minizinc/kp01.dzn \
    > ciktilar/kp01-gecode.txt
minizinc --solver Gecode --statistics minizinc/assignment.mzn minizinc/assignment.dzn \
    > ciktilar/assignment-gecode.txt
minizinc --solver COIN-BC --statistics minizinc/assignment.mzn minizinc/assignment.dzn \
    > ciktilar/assignment-coinbc.txt
minizinc --solver HiGHS --statistics minizinc/assignment.mzn minizinc/assignment.dzn \
    > ciktilar/assignment-highs.txt
../.venv/bin/python modeller/minizinc_python.py > ciktilar/minizinc-python-run.txt
# Gecode vs HiGHS FlatZinc constraint counts (run in a scratch copy of minizinc/)
minizinc -c -o nqueens.fzn --solver Gecode nqueens.mzn nqueens.dzn
minizinc -c -o nqueens-highs.fzn --solver HiGHS nqueens.mzn nqueens.dzn
grep -c "^constraint" nqueens.fzn nqueens-highs.fzn
```

## Notes — solver inventory in this environment (real, verified)

`minizinc --solvers` on this machine (MiniZinc 2.10.1, Homebrew) lists
eight configurations; the four that matter are Gecode 6.5.0 plus three MIP
backend *configurations* — Gurobi, HiGHS, COIN-BC (the others are Gecode
Gist and unconfigured CPLEX/SCIP/Xpress placeholders). Three of these four
actually solve here; Gurobi does not:

| Solver | Registered? | Actually solves? | Reason if not |
|---|---|---|---|
| Gecode | yes | yes | — |
| COIN-BC | yes | yes | — |
| HiGHS | yes | yes | works after `brew install highs` plus the `~/.minizinc/Preferences.json` `--highs-dll` entry above; MiniZinc's own HiGHS plugin does not bundle the HiGHS library |
| Gurobi | yes | **no** | `No Gurobi license found` — the author's academic Gurobi license expired (`~/gurobi.lic.expired-2026-01-08`); MiniZinc's Gurobi backend needs a full license, unlike `gurobipy`'s own bundled restricted license |

Every "solver independence" comparison in this week's code and captured
`ciktilar/` output therefore exercises **Gecode + COIN-BC + HiGHS**, all
of which report the same optimal cost (`13`) for the assignment instance.
Gurobi remains unavailable and is not fabricated: `assignment-gurobi.txt`
is a real, captured error transcript documenting that failure mode, not a
solved comparison. `minizinc_python.py` and `tests/test_models.py` both
probe a MIP backend with a trivial solve before relying on it and
skip/report cleanly if it is not usable, rather than assuming any
particular backend is always available — this is why Gurobi shows up as
`unavailable` in `minizinc-python-run.txt` while COIN-BC and HiGHS solve
normally.

`nqueens.mzn` and `assignment.mzn` both `include "all_different.mzn";` —
MiniZinc never auto-includes a global constraint, so `all_different` must
be pulled in explicitly (or via the full `globals.mzn`); without it the
compiler stops with `type error: no function or predicate with name
'all_different' found`.

The knapsack model is named `kp01.mzn`/`kp01.dzn`, not `knapsack.mzn`:
the MiniZinc standard library ships its own `knapsack.mzn` global
constraint, and a model file of that name shadows it, so MiniZinc 2.10
prints a deprecation warning (`included file "knapsack.mzn" overrides a
global constraint file from the standard library. This is deprecated.`)
before every run. With the `kp01` name the run is warning-free.

The flattened `all_different(q)` constraint in `nqueens.fzn` becomes
`fzn_all_different_int(q)` (with an `fzn_` prefix, not the bare
`all_different_int` an earlier draft of the Unit 2 practice-task feedback
assumed) — read from the real compiled file in
`ciktilar/nqueens-flatzinc-excerpt.txt`.

## Previous week

`nqueens.mzn` rewrites the exact Week 1–4 N-queens CSP structure (columns
plus both diagonals as `all_different`) in MiniZinc syntax; `kp01.mzn`
and `assignment.mzn` make their first appearance this week and are reused
by Week 7's `gurobipy` models with the same cost data.
