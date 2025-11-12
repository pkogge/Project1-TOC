import pytest
from typing import List, Tuple, Optional, Dict

from src.helpers.graph_coloring_helper import GraphColoringAbstractClass
from src.graph_coloring import GraphColoring 

def is_valid_coloring_representation(coloring) -> Dict[int, int]:
    if coloring == []:
        return coloring
    if isinstance(coloring, list):
        return {i: c for i, c in enumerate(coloring)}


def check_coloring_validity(coloring_rep: Dict[int, int], edges: List[Tuple[int]], k: int):
    for u, v in edges:
        assert coloring_rep[u] != coloring_rep[v], f"edge {(u,v)} has same color"

@pytest.mark.parametrize(
    "n_vertices, edges, k, expected_possible",
    [
        # trivial: no edges -> always 1-colorable
        (1, [], 1, True),
        # simple edge (0-1) is 2-colorable
        (2, [(0, 1)], 2, True),
        # triangle (3-cycle) is not 2-colorable
        (3, [(0, 1), (1, 2), (2, 0)], 2, False),
        # triangle is 3-colorable
        (3, [(0, 1), (1, 2), (2, 0)], 3, True),
        # path of length 2 is 2-colorable
        (3, [(0,1), (1,2)], 2, True),
    ],
)
def test_coloring_bruteforce_examples(n_vertices, edges, k, expected_possible):
    solver = GraphColoring(cnf_file_input_path="input/graph_input.cnf")

    # call the brute force method; adapt name/signature if necessary
    result = solver.coloring_bruteforce(n_vertices, edges, k)

    # result should be a tuple (bool, coloring_or_none) by spec
    assert isinstance(result, tuple) and len(result) == 2

    possible, coloring = result
    assert possible == expected_possible

    if expected_possible:
        # coloring must exist and be valid
        coloring_dict = is_valid_coloring_representation(coloring)
        assert coloring_dict is not None
        check_coloring_validity(coloring_dict, edges, k)
    else:
        # If impossible, the second return may be None or empty — accept either
        assert coloring is None or coloring == [] or isinstance(coloring, (list))


