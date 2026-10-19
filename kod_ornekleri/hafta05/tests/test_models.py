"""Pytest gate for Week 5: the tree CSP's DAC-filtered forward assignment
records zero backtracks and CP-SAT independently confirms the same
instance is validly colourable; both treewidth examples match Unit 1/2's
worked values; both social-golfer variants return a feasible, pairing-
respecting schedule; both BIBD variants return a valid (7,7,3,3,1) design.
"""

import sys
from pathlib import Path

from ortools.sat.python import cp_model

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "modeller"))

import bibd  # noqa: E402
import social_golfer  # noqa: E402
import tree_csp  # noqa: E402
import treewidth  # noqa: E402


def test_tree_csp_forward_assignment_has_zero_backtracks_and_matches_cp_sat() -> None:
    domains = tree_csp.build_domains()
    tree_csp.apply_dac(domains)
    assignment: dict[str, int] = {}
    backtracks = 0
    for region in tree_csp.ORDER:
        parent = tree_csp.PARENT.get(region)
        if parent is None:
            candidates = domains[region]
        else:
            candidates = [v for v in domains[region] if tree_csp.is_compatible(v, assignment[parent])]
        if not candidates:
            backtracks += 1
        assignment[region] = candidates[0]
    assert backtracks == 0
    for region_a, region_b in tree_csp.EDGES:
        assert assignment[region_a] != assignment[region_b]
    status, cp_sat_assignment = tree_csp.cross_check_with_cp_sat()
    assert status == "OPTIMAL"
    for region_a, region_b in tree_csp.EDGES:
        assert cp_sat_assignment[region_a] != cp_sat_assignment[region_b]


def test_tree_example_induced_width_is_one() -> None:
    assert treewidth.treewidth_tree_example() == 1


def test_cutset_example_induced_width_matches_worked_example() -> None:
    assert treewidth.treewidth_cutset_example() == 3


def _check_golfer_schedule_is_valid(schedule: list[list[int]]) -> None:
    pair_meetings: dict[tuple[int, int], int] = {}
    for week_groups in schedule:
        members_by_group: dict[int, list[int]] = {}
        for golfer, group in enumerate(week_groups):
            members_by_group.setdefault(group, []).append(golfer)
        for members in members_by_group.values():
            assert len(members) == social_golfer.GROUP_SIZE
            for i in range(len(members)):
                for j in range(i + 1, len(members)):
                    pair = (members[i], members[j])
                    pair_meetings[pair] = pair_meetings.get(pair, 0) + 1
    assert all(count <= 1 for count in pair_meetings.values())


def test_social_golfer_both_variants_are_feasible_and_valid() -> None:
    status_without, schedule_without = social_golfer.solve_and_report(False)
    status_with, schedule_with = social_golfer.solve_and_report(True)
    assert status_without == status_with == cp_model.OPTIMAL
    _check_golfer_schedule_is_valid(schedule_without)
    _check_golfer_schedule_is_valid(schedule_with)


def _check_bibd_design_is_valid(design: list[list[int]]) -> None:
    for row in design:
        assert sum(row) == bibd.BLOCKS_PER_POINT
    for block in range(bibd.NUM_BLOCKS):
        assert sum(row[block] for row in design) == bibd.POINTS_PER_BLOCK
    for point_a in range(bibd.NUM_POINTS):
        for point_b in range(point_a + 1, bibd.NUM_POINTS):
            shared = sum(
                1 for block in range(bibd.NUM_BLOCKS) if design[point_a][block] and design[point_b][block]
            )
            assert shared == bibd.PAIR_COUNT


def test_bibd_both_variants_are_valid_fano_plane_designs() -> None:
    status_without, design_without = bibd.solve_and_report(False)
    status_with, design_with = bibd.solve_and_report(True)
    assert status_without == status_with == cp_model.OPTIMAL
    _check_bibd_design_is_valid(design_without)
    _check_bibd_design_is_valid(design_with)
