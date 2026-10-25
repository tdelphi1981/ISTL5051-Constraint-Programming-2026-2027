"""Unit 4's running example: load knapsack.mzn and nqueens.mzn, build one
Instance per solver (Gecode and this environment's MIP backends), solve
each, and print a comparison table (solver, status, objective/solution,
wall-clock time in milliseconds).
"""

import time
from pathlib import Path

import minizinc

MZN_DIR = Path(__file__).resolve().parent.parent / "minizinc"

# BEGIN mzn_python_model
knapsack_model = minizinc.Model(MZN_DIR / "knapsack.mzn")
knapsack_model.add_file(MZN_DIR / "knapsack.dzn")
nqueens_model = minizinc.Model(MZN_DIR / "nqueens.mzn")
nqueens_model.add_file(MZN_DIR / "nqueens.dzn")
# END mzn_python_model

# The three MIP backends `minizinc --solvers` reports as configured in this
# environment. Gecode, COIN-BC and HiGHS all solve here; Gurobi is
# registered but has no usable license (see README.md).
MIP_BACKENDS = ["coin-bc", "highs", "gurobi"]


def summarize(result: minizinc.Result) -> str:
    """One-line human-readable summary of a solved Result's solution."""
    if result.solution is None:
        return "no solution"
    if hasattr(result.solution, "objective"):
        return f"objective={result.solution.objective}"
    return "solution found"


def compare_solvers(problem_name: str, model: minizinc.Model) -> None:
    """Solve `model` on Gecode and on every MIP backend in MIP_BACKENDS,
    printing one comparison row per solver (skipping backends that raise
    a MiniZincError, with the real error reason).
    """
    rows = []

    # BEGIN mzn_python_instance_gecode
    solver = minizinc.Solver.lookup("gecode")
    instance = minizinc.Instance(solver, model)
    start = time.perf_counter()
    result = instance.solve()
    elapsed_ms = (time.perf_counter() - start) * 1000
    rows.append(("Gecode", str(result.status), elapsed_ms, summarize(result)))
    # END mzn_python_instance_gecode

    # BEGIN mzn_python_instance_mip
    for backend in MIP_BACKENDS:
        try:
            solver = minizinc.Solver.lookup(backend)
            instance = minizinc.Instance(solver, model)
            start = time.perf_counter()
            result = instance.solve()
            elapsed_ms = (time.perf_counter() - start) * 1000
            rows.append((backend, str(result.status), elapsed_ms, summarize(result)))
        except minizinc.MiniZincError as error:
            rows.append((backend, "unavailable", 0.0, str(error).splitlines()[0]))
    # END mzn_python_instance_mip

    # BEGIN mzn_python_compare
    print(f"\n{problem_name}:")
    print(f"{'solver':<10} {'status':<20} {'time_ms':>10}  summary")
    for solver_name, status, ms, summary in rows:
        print(f"{solver_name:<10} {status:<20} {ms:>10.2f}  {summary}")
    # END mzn_python_compare


if __name__ == "__main__":
    compare_solvers("knapsack (n=4, capacity=7)", knapsack_model)
    compare_solvers("nqueens (n=6)", nqueens_model)
