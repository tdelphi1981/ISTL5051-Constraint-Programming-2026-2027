"""Pytest gate for Week 4: local search, LNS, restarts/nogood learning and
portfolio search all produce real, non-fabricated evidence.

The two timing/log-sensitive scripts (`solver_log_restarts.py`,
`portfolio_search.py`) are not re-run here — they are only re-run once to
produce `ciktilar/`, and this gate reads those real captured files, the
same way the Unit 3/4 practice tasks in the brief point students at
`ciktilar/solver-log-restarts.txt` and `ciktilar/portfolio-timing.txt`
rather than at a freshly re-timed run.
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "modeller"))

import golomb_ruler  # noqa: E402
import large_nqueens_lns  # noqa: E402
import min_conflicts  # noqa: E402

CIKTILAR = Path(__file__).resolve().parent.parent / "ciktilar"


def test_min_conflicts_reaches_zero_conflicts_for_2000_queens() -> None:
    _columns, steps = min_conflicts.min_conflicts_loop(
        min_conflicts.N, min_conflicts.SEED, min_conflicts.MAX_STEPS
    )
    assert steps < min_conflicts.MAX_STEPS


def test_large_nqueens_lns_conflict_count_never_increases() -> None:
    columns = large_nqueens_lns.lns_initial_assignment(
        large_nqueens_lns.N, large_nqueens_lns.SEED
    )
    import random

    rng = random.Random(large_nqueens_lns.SEED + 1)
    previous = large_nqueens_lns.count_conflicts(columns)
    for _ in range(large_nqueens_lns.ROUNDS):
        relaxed_rows = large_nqueens_lns.lns_destroy(
            large_nqueens_lns.N, large_nqueens_lns.NEIGHBOURHOOD_SIZE, rng
        )
        columns = large_nqueens_lns.lns_repair(columns, relaxed_rows, large_nqueens_lns.N)
        current = large_nqueens_lns.count_conflicts(columns)
        assert current <= previous
        previous = current


def test_golomb_order_8_optimal_length_is_34() -> None:
    length, marks = golomb_ruler.golomb_objective_solve(
        golomb_ruler.ORDER, golomb_ruler.UPPER_BOUND
    )
    assert length == 34
    assert marks[0] == 0
    assert marks[-1] == length
    assert marks == sorted(marks)


def test_golomb_lns_improves_on_the_greedy_start() -> None:
    greedy = golomb_ruler.golomb_greedy_start(golomb_ruler.ORDER)
    assert greedy[-1] > 34

    improved = golomb_ruler.golomb_lns_destroy_repair(
        golomb_ruler.ORDER,
        golomb_ruler.UPPER_BOUND,
        golomb_ruler.NEIGHBOURHOOD_SIZE,
        golomb_ruler.ROUNDS,
        golomb_ruler.SEED,
    )
    assert improved[-1] < greedy[-1]


def test_solver_log_restarts_captured_log_has_a_restart_line() -> None:
    log_text = (CIKTILAR / "solver-log-restarts.txt").read_text()
    assert log_text.strip() != ""
    assert re.search(r"restarts?:?\s*\d+", log_text, re.IGNORECASE)


def test_portfolio_single_and_multi_worker_agree_on_the_proven_length() -> None:
    timing_text = (CIKTILAR / "portfolio-timing.txt").read_text()
    lengths = re.findall(r"length=(\d+)", timing_text)
    statuses = re.findall(r"status=(\w+)", timing_text)
    assert len(lengths) == 2
    assert lengths[0] == lengths[1] == "44"
    assert all(status == "OPTIMAL" for status in statuses)
