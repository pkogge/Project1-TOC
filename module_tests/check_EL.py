import os
from src.sat_EL import SatSolver

def test_run_on_2sat():
    # Make sure file exists
    assert os.path.exists("2SAT.cnf"), "2SAT.cnf not found"

    solver = SatSolver("2SAT.cnf")
    solver.run()

    # Check that results file was created
    expected_folder = "results"
    files = os.listdir(expected_folder)
    matching = [f for f in files if "2SAT" in f and f.endswith(".csv")]
    assert matching, "No results CSV created for 2SAT"

def test_run_on_ksat():
    assert os.path.exists("cnffile_EL.cnf"), "cnffile_EL not found"

    solver = SatSolver("cnffile_EL.cnf")
    solver.run()

    expected_folder = "results"
    files = os.listdir(expected_folder)
    matching = [f for f in files if "cnffile_EL" in f and f.endswith(".csv")]
    assert matching, "No results CSV created for cnffile_EL"
