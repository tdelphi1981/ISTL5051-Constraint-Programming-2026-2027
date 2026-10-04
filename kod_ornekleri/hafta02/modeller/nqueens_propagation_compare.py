"""Solve N-queens with both nqueens_models.py models and compare CP-SAT's
own search statistics -- the empirical stand-in for propagation strength
(Unit 4). Reports the real numbers from real runs; no fabricated output.
"""

from ortools.sat.python import cp_model

from nqueens_models import build_strong_model, build_weak_model


def collect_solver_stats(model: cp_model.CpModel) -> dict[str, object]:
    # BEGIN collect_solver_stats
    solver = cp_model.CpSolver()
    solver.parameters.num_workers = 1
    solver.parameters.random_seed = 42
    status = solver.Solve(model)
    return {
        "status": solver.StatusName(status),
        "branches": solver.NumBranches(),
        "conflicts": solver.NumConflicts(),
        "wall_time": solver.WallTime(),
    }
    # END collect_solver_stats


def propagation_comparison_report(n: int) -> dict[str, dict[str, object]]:
    # BEGIN propagation_comparison_report
    strong_model, _ = build_strong_model(n)
    weak_model, _ = build_weak_model(n)
    stats = {
        "strong (AllDifferent)": collect_solver_stats(strong_model),
        "weak (pairwise !=)": collect_solver_stats(weak_model),
    }
    print(f"N={n} propagation-strength comparison")
    for label, s in stats.items():
        print(
            f"{label}: status={s['status']} branches={s['branches']} "
            f"conflicts={s['conflicts']} wall_time={s['wall_time']:.4f}s"
        )
    return stats
    # END propagation_comparison_report


if __name__ == "__main__":
    propagation_comparison_report(8)
    propagation_comparison_report(20)
