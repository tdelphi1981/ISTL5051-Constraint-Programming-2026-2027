"""Pure-Python induced-width calculator (no `networkx` dependency; it is
not part of this course's pinned environment) applied to two small
constraint graphs: Unit 1's tree instance (expected induced width 1) and
Unit 2's worked cutset example, a 4-cycle plus a pendant edge.
"""

Adjacency = dict[str, set[str]]

TREE_GRAPH: Adjacency = {
    "R1": {"R2", "R3"},
    "R2": {"R1", "R4", "R5"},
    "R3": {"R1"},
    "R4": {"R2"},
    "R5": {"R2"},
}
# Eliminate leaves first, then their now-isolated parent, then the root.
TREE_ORDER = ["R3", "R4", "R5", "R2", "R1"]

CUTSET_GRAPH: Adjacency = {
    "A": {"B", "D", "E"},
    "B": {"A", "C"},
    "C": {"B", "D"},
    "D": {"C", "A"},
    "E": {"A"},
}
# Cutset variable A eliminated first (Unit 2's worked example).
CUTSET_ORDER = ["A", "B", "D", "E", "C"]


# BEGIN treewidth_induced_width
def induced_width(adjacency: Adjacency, order: list[str]) -> int:
    """Simulate variable elimination in `order`: at each step, connect the
    eliminated variable's still-active neighbours into a clique (fill-in
    edges), and track the largest neighbour count seen at elimination time.
    """
    graph = {node: set(neighbours) for node, neighbours in adjacency.items()}
    width = 0
    for node in order:
        neighbours = graph[node]
        width = max(width, len(neighbours))
        for neighbour in neighbours:
            graph[neighbour].update(neighbours - {neighbour})
        for neighbour in neighbours:
            graph[neighbour].discard(node)
        del graph[node]
    return width
# END treewidth_induced_width


# BEGIN treewidth_tree_example
def treewidth_tree_example() -> int:
    """Unit 1's tree (R1..R5): a tree's treewidth is always 1."""
    width = induced_width(TREE_GRAPH, TREE_ORDER)
    print(f"Elimination order: {TREE_ORDER}")
    print(f"Induced width: {width}")
    return width
# END treewidth_tree_example


# BEGIN treewidth_cutset_example
def treewidth_cutset_example() -> int:
    """Unit 2's worked example: 4-cycle A-B-C-D-A plus pendant edge A-E;
    eliminating cutset variable A first gives induced width 3.
    """
    width = induced_width(CUTSET_GRAPH, CUTSET_ORDER)
    print(f"Cutset variable eliminated first: {CUTSET_ORDER[0]}")
    print(f"Elimination order: {CUTSET_ORDER}")
    print(f"Induced width: {width}")
    return width
# END treewidth_cutset_example


if __name__ == "__main__":
    treewidth_tree_example()
    treewidth_cutset_example()
