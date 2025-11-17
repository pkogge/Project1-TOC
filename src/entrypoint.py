import os
from src.helpers.project_selection_enum import ProjectSelection
from src.helpers.constants import CONFIGURATION_FILE_PATH, parse_config, INPUT_FILE
from src.sat import SatSolver
from src.helpers.automation_helpers import brief_about_project
import matplotlib.pyplot as plt
import csv
def generate_plots():
    print("[INFO] Generating graphs in results folder...")

    # Resolve project root relative to this file
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    results_dir = os.path.join(project_root, "results")
    graphs_dir = results_dir   # save inside results/

    # Debug path
    print("[INFO] Reading results from:", results_dir)

    for root, dirs, files in os.walk(results_dir):
        for filename in files:
            full_path = os.path.join(root, filename)
            lower = filename.lower()

            # Helper function to generate a single plot
            def plot_csv(method_name, filetag):
                print(f"[INFO] Processing {method_name}: {filename}")

                with open(full_path) as csvfile:
                    csvlist = list(csv.reader(csvfile))

                xVals, yVals, color = [], [], []

                for index, row in enumerate(csvlist):
                    if index == 0:
                        continue
                    xVals.append(int(row[1]))         # n_vars
                    yVals.append(float(row[5]))      # time
                    color.append("green" if row[4] == "S" else "red")

                if not xVals:
                    print("[WARN] No data found in:", filename)
                    return

                plt.scatter(xVals, yVals, c=color)
                plt.xlabel("Number of Variables")
                plt.ylabel("Time (s)")
                plt.title(method_name)

                out_path = os.path.join(graphs_dir, f"{filetag}.png")
                plt.savefig(out_path)
                plt.clf()
                print(f"[INFO] Saved graph: {out_path}")

            # Detect file types
            if "brute_force" in lower:
                plot_csv("Brute Force", "brute_force_plot")

            if "btracking" in lower:
                plot_csv("Backtracking", "backtracking_plot")

            if "simple" in lower:
                plot_csv("Simple Method", "simple_plot")

            if "best" in lower:
                plot_csv("Best Case", "best_case_plot")

    print("[INFO] All graphs generated.")
def main():
    """
    Entry point for the project1_toc package.
    """

    if not os.path.exists(CONFIGURATION_FILE_PATH):
        brief_about_project()
    selection, sub_problem = parse_config(CONFIGURATION_FILE_PATH)
    solver = SatSolver(INPUT_FILE)
    if solver:
        solver.run()
    generate_plots()


    
    
