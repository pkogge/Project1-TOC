import os
from src.sat import SatSolver

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

# def test_run_on_ksat():
#     assert os.path.exists("kSAT.cnf"), "kSAT.cnf not found"

#     solver = SatSolver("kSAT.cnf")
#     solver.run()

#     expected_folder = "results"
#     files = os.listdir(expected_folder)
#     matching = [f for f in files if "kSAT" in f and f.endswith(".csv")]
#     assert matching, "No results CSV created for kSAT"
