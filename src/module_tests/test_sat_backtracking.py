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


def test_single_literal_clause_fills_default_assignment(solver):
    sat, assignment = solver.sat_backtracking(3, [[1]])

    assert sat is True
    assert assignment == {1: True, 2: False, 3: False}


def test_contradictory_unit_clauses_is_unsatisfiable(solver):
    sat, assignment = solver.sat_backtracking(1, [[1], [-1]])

    assert sat is False
    assert assignment == {}


def test_backtracking_recovers_after_initial_conflict(solver):
    clauses = [[-1], [2]]

    sat, assignment = solver.sat_backtracking(2, clauses)

    assert sat is True
    assert assignment == {1: False, 2: True}


def test_empty_clause_list_is_vacuously_true(solver):
    sat, assignment = solver.sat_backtracking(2, [])

    assert sat is True
    assert assignment == {1: False, 2: False}
