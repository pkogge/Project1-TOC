#!/usr/bin/env python3
"""
Built this to run on my end to call on the helper functions that allow parsing and outputting resultsfile.csv and a plot
To use: uv run scripts/local_sat_runner.py input/my_test.cnf results/resultsfile.csv (run in main directory ~$/Project1_TOC) note i changed the names of these files so now to run them use the files as they are named now
"""

import sys
import csv
import time
import os
from typing import List, Tuple, Dict

#had to add this to make the project root importable and be able to call the helper functions
import os, sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)


#calling the help functions
from src.helpers.dmaics_parser import parse_multi_instance_dimacs
from src.sat import SatSolver

import matplotlib.pyplot as plt
import numpy as np

#writing my own csv parser, timing where necessary since it is needed for the graph
def write_results_csv(instances, solver: SatSolver, out_csv: str):
    os.makedirs(os.path.dirname(out_csv) or ".", exist_ok=True)
    nvars_list, times_list, sat_flags = [], [], []

    with open(out_csv, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["instance_id","n_vars","n_clauses","method","satisfiable","time_seconds","solution"])

        #timing how long it takes
        for (inst_id, n_vars, clauses) in instances:
            n_clauses = len(clauses)
            t_start = time.perf_counter()
            sat, assign = solver.sat_bruteforce(n_vars, clauses)
            t_end = time.perf_counter() - t_start

            method = "BruteForce"
            if sat:
                sat_flag = "S" 
            else:
                sat_flag = "U"
            if sat:
                sol_str = str(assign) 
            else:
                sol_str = "{}"

<<<<<<< HEAD
            #these are the rows
            w.writerow([inst_id, n_vars, n_clauses, method, sat_flag, dt, sol_str])

            nvars_list.append(n_vars)
            #times_list needed for the graph
            times_list.append(dt)
            sat_flags.append(ok)
=======
            w.writerow([inst_id, n_vars, n_clauses, method, sat_flag, t_end, sol_str])

            nvars_list.append(n_vars)
            times_list.append(t_end)
            sat_flags.append(sat)
>>>>>>> bd3f9d3 (edits)

    return nvars_list, times_list, sat_flags

#generating a scatter plot with different variables
def plot_from_results(nvars_list, times_list, sat_flags, out_png="sat_solver_performance.png"):
    if not nvars_list:
        return
    x_sat  = [nvars_list[i] for i in range(len(nvars_list)) if sat_flags[i]]
    y_sat  = [times_list[i]  for i in range(len(times_list))  if sat_flags[i]]
    x_uns  = [nvars_list[i] for i in range(len(nvars_list)) if not sat_flags[i]]
    y_uns  = [times_list[i]  for i in range(len(times_list))  if not sat_flags[i]]

    plt.figure(figsize=(10, 6))
    if x_sat:
        plt.scatter(x_sat, y_sat, marker='o', label='Satisfiable')
    if x_uns:
        plt.scatter(x_uns, y_uns, marker='^', label='Unsatisfiable')

    if nvars_list:
        max_n = max(nvars_list)
        xvals = np.arange(1, max_n + 1)
        yref = np.array([2**n for n in xvals], dtype=float)
        if len(times_list) and yref.max() > 0:
            scale = max(times_list) / yref.max()
            plt.plot(xvals, scale * yref, linestyle='--', label='2^n (scaled)')

    plt.xlabel("Number of Variables")
    plt.ylabel("Time (in seconds)")
    plt.title("SAT Solver Performance (Brute Force)")
    plt.legend(loc="upper left")
    plt.tight_layout()
    plt.savefig(out_png)
    print(f"Plot saved to {out_png}")

def main():
    if len(sys.argv) < 3:
        sys.exit(1)

    input = sys.argv[1]
    output = sys.argv[2]

    #using helper given to us
    instances = parse_multi_instance_dimacs(input)
    if not instances:
        sys.exit(1)

    #using my satsolver brute force function
    solver = SatSolver(cnf_file_input_path=input, result_file_name="output_trigonometry")

    #outputting the csv in the order necessary, saving variables for the plot
    nvars_list, times_list, sat_flags = write_results_csv(instances, solver, output)

    #making the plot

    #sending it to the same place as the output file which was results 
    outdir = os.path.dirname(output) or "."
    os.makedirs(outdir, exist_ok=True)
    out_png = os.path.join(outdir, "output_graph_trigonometry.png")

    try:
        plot_from_results(nvars_list, times_list, sat_flags, out_png)
    except Exception as e:
        print("Plotting did not work:", e)

    print(f"Results to {outcsv}")

if __name__ == "__main__":
    main()

