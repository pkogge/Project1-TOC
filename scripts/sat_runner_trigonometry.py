#!/usr/bin/env python3
"""
Built this to run on my end to call on the helper functions that allow parsing and outputting resultsfile.csv and a plot
To use: uv run scripts/local_sat_runner.py input/my_test.cnf results/resultsfile.csv (run in main directory ~$/Project1_TOC)
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

def write_results_csv(instances, solver: SatSolver, out_csv: str):
    os.makedirs(os.path.dirname(out_csv) or ".", exist_ok=True)
    nvars_list, times_list, sat_flags = [], [], []

    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["instance_id","n_vars","n_clauses","method","satisfiable","time_seconds","solution"])

        for (inst_id, n_vars, clauses) in instances:
            n_clauses = len(clauses)
            t0 = time.perf_counter()
            ok, assign = solver.sat_bruteforce(n_vars, clauses)
            dt = time.perf_counter() - t0

            method = "BruteForce"
            sat_flag = "S" if ok else "U"
            sol_str = str(assign) if ok else "{}"

            w.writerow([inst_id, n_vars, n_clauses, method, sat_flag, dt, sol_str])

            nvars_list.append(n_vars)
            times_list.append(dt)
            sat_flags.append(ok)

    return nvars_list, times_list, sat_flags

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
    plt.ylabel("Time (seconds)")
    plt.title("SAT Solver Performance (Brute Force)")
    plt.legend(loc="upper left")
    plt.tight_layout()
    plt.savefig(out_png)
    print(f"Plot saved to {out_png}")

def main():
    if len(sys.argv) < 3:
        print("Usage: uv run scripts/local_sat_runner.py <input.cnf> <resultsfile.csv>")
        sys.exit(1)

    inpath = sys.argv[1]
    outcsv = sys.argv[2]

    #using helper given to us
    instances = parse_multi_instance_dimacs(inpath)
    if not instances:
        print("No instances parsed. Check the input file.")
        sys.exit(1)

    #using my satsolver brute force function
    solver = SatSolver(cnf_file_input_path=inpath, result_file_name="output_trigonometry")

    #outputting the csv in the order necessary, saving variables for the plot
    nvars_list, times_list, sat_flags = write_results_csv(instances, solver, outcsv)

    #making the plot

    #sending it to the same place as the outcsv file which was results 
    outdir = os.path.dirname(outcsv) or "."
    os.makedirs(outdir, exist_ok=True)
    out_png = os.path.join(outdir, "output_graph_trigonometry.png")

    try:
        plot_from_results(nvars_list, times_list, sat_flags, out_png)
    except Exception as e:
        print("Plotting failed:", e)

    print(f"Wrote results to {outcsv}")

if __name__ == "__main__":
    main()
