import pytest

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from src.sat import SatSolver


@pytest.fixture
def solver(tmp_path):
    """Create a dummy CNF file so SatSolver can be constructed."""
    dummy = tmp_path / "dummy.cnf"
    dummy.write_text("c dummy\np cnf 0 0\n")
    return SatSolver(str(dummy))


def test_sat_bruteforce_simple_sat(solver):
    sat, assignment = solver.sat_bruteforce(1, [[1]])
    assert sat is True
    assert assignment[1] is True


def test_sat_bruteforce_simple_unsat(solver):
    sat, assignment = solver.sat_bruteforce(1, [[1], [-1]])
    assert sat is False
    assert assignment == {}


def test_sat_bruteforce_multi_var_sat(solver):
    clauses = [
        [1, 2],
        [-1, 3]
    ]
    sat, assignment = solver.sat_bruteforce(3, clauses)
    assert sat is True
    assert (assignment[1] is False) or (assignment[2] is True)
    assert (not assignment[1]) or assignment[3]


def test_sat_bruteforce_multi_var_unsat(solver):
    clauses = [
        [1],
        [-1, 2],
        [-2],
        [2]
    ]
    sat, assignment = solver.sat_bruteforce(2, clauses)
    assert sat is False
    assert assignment == {}


def test_sat_bruteforce_negative_literals(solver):
    sat, assignment = solver.sat_bruteforce(2, [[-1, -2]])
    assert sat is True
    assert assignment[1] is False or assignment[2] is False
