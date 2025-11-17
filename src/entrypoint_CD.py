import os
from src.helpers.project_selection_enum import ProjectSelection
from src.helpers.constants import CONFIGURATION_FILE_PATH, parse_config, INPUT_FILE
from src.sat_CD import SatSolver
from src.bin_packing import BinPacking
from src.graph_coloring import GraphColoring
from src.hamilton_cycle import HamiltonCycleColoring
from src.helpers.automation_helpers import brief_about_project

# ANDRE MAYARD IMPORTS
import csv
import matplotlib.pyplot as plt

def main():
    """
    Entry point for the project1_toc package.
    """

    if not os.path.exists(CONFIGURATION_FILE_PATH):
        brief_about_project()
    selection, sub_problem = parse_config(CONFIGURATION_FILE_PATH)


    if selection["name"] == ProjectSelection.sat.name:
        solver = SatSolver(INPUT_FILE)
    elif selection["name"] == ProjectSelection.bin_packing.name:
        solver = BinPacking(INPUT_FILE)
    elif selection["name"] == ProjectSelection.hamiltonian.name:
        solver = HamiltonCycleColoring(INPUT_FILE)
    elif selection["name"] == ProjectSelection.graph_coloring.name:
        solver = GraphColoring(INPUT_FILE)
    
    if solver:
        solver.run()

    # ANDRE MAYARD CODE
    xs = []
    ys = []
    colors = []

    with open("./results/brute_force_cnffile_CD_sat_solver_results_CD.csv") as f:
        reader = csv.DictReader(f)
        for row in reader:
            xs.append(int(row["n_vars"]))
            ys.append(float(row["time_seconds"]))

            if row["satisfiable"] == "S":
                colors.append("green")
            else:
                colors.append("red")

    plt.scatter(xs, ys, c=colors)
    plt.xlabel("Number of Variables")
    plt.ylabel("Runtime (seconds)")
    plt.title("Brute Force SAT Solver Runtime vs Problem Size")
    plt.savefig("./results/brute_force_plot_CD.png")


    
    
