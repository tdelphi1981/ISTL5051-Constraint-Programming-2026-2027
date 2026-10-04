# ISTL5051 Constraint Programming — 2026-2027

**Modeling and solving combinatorial problems with OR-Tools, Gurobi and MiniZinc**

Karadeniz Technical University | Faculty of Science, Department of Computer Science | 2026-2027 Fall Semester

Instructor: Assoc. Prof. Tolga Berber

Materials are added every week. Each week is pinned by a `weekNN` tag; select a tag to see the content up to that week only.

## Weekly Plan

| Week | Topic | Lecture Notes | Slides | Lab | Code |
|---|---|---|---|---|---|
| 1 | Constraint Satisfaction Problems: A Formal Definition | [PDF](lecture-notes/Week01_Constraint_Satisfaction_Problems.pdf) | [Slides](slides/Week01_Constraint_Satisfaction_Problems.pdf) | [Lab](labs/Lab01_Constraint_Satisfaction_Problems.pdf) | [Code](kod_ornekleri/hafta01) |

## Folders

| Folder | Contents |
|---|---|
| `lecture-notes/` | Weekly chapters of the course book |
| `slides/` | Weekly lecture slides |
| `labs/` | Lab sheets |
| `kod_ornekleri/` | Working code examples used in the notes and lab sheets; each week's `README.md` gives the run instructions |

## Running the Code Examples

All examples use Python 3.12. Each week's `README.md` assumes a shared virtual environment at `kod_ornekleri/.venv`. Create it once:

```bash
cd kod_ornekleri
python3.12 -m venv .venv
.venv/bin/python -m pip install -r hafta01/requirements.txt
```

On Windows, use `py -3.12 -m venv .venv` and `.venv\Scripts\python` instead of `.venv/bin/python`.

```bash
# Week 1: run the tests and one model
cd kod_ornekleri/hafta01
../.venv/bin/python -m pytest -q
../.venv/bin/python modeller/nqueens.py
```

Weeks 1–3 use only OR-Tools CP-SAT. MiniZinc and Gurobi enter in later weeks; Gurobi needs a free academic license from gurobi.com.

## License

These materials are prepared for academic use. See [LICENSE](LICENSE) for details.
