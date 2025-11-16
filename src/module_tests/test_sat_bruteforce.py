from pathlib import Path
import sys

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.sat import SatSolver


@pytest.fixture
def solver():
    """
    SatSolver performs file parsing in __init__, so we bypass it here
    """
    return SatSolver.__new__(SatSolver)


def test_bruteforce_satisfies_simple_unit_clause(solver):
    sat, assignment = solver.sat_bruteforce(2, [[1]])

    assert sat is True
    assert assignment == {1: True, 2: False}


def test_bruteforce_finds_assignment_for_binary_clauses(solver):
    clauses = [[1, 2], [-1, 3], [-2, -3]]

    sat, assignment = solver.sat_bruteforce(3, clauses)

    assert sat is True
    assert assignment == {1: False, 2: True, 3: False}


def test_bruteforce_unsatisfiable_return_empty_assignment(solver):
    sat, assignment = solver.sat_bruteforce(1, [[1], [-1]])

    assert sat is False
    assert assignment == {}


def test_bruteforce_empty_clauses_trivially_true(solver):
    sat, assignment = solver.sat_bruteforce(2, [])

    assert sat is True
    assert assignment == {1: False, 2: False}
