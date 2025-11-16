#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt

def make_plot(csv_path, title, output_png):
    df = pd.read_csv(csv_path)

    # compute problem size
    df["problem_size"] = df["n_vars"] * df["n_clauses"]

    plt.figure(figsize=(8, 6))

    # green = satisfiable (S), red = unsatisfiable (U)
    for _, row in df.iterrows():
        color = "green" if row["satisfiable"] == "S" else "red"
        plt.scatter(row["problem_size"], row["time_seconds"], color=color)

    plt.title(title)
    plt.xlabel("Problem Size (n_vars * n_clauses)")
    plt.ylabel("Time (seconds)")
    plt.grid(True)

    plt.savefig(output_png)
    print(f"[graph] Saved plot to {output_png}")
    plt.close()


def run_graphs(result_files):
    """
    result_files = (bruteforce_csv_path, backtracking_csv_path)
    """
    for f in result_files: 
        if "brute_force" in f:
            bf_csv = f
        elif "btracking" in f:
            bt_csv = f

    make_plot(bf_csv,
              "Brute Force SAT Solver Timing",
              "bruteforce_plot.png")

    make_plot(bt_csv,
              "Backtracking SAT Solver Timing",
              "btracking_plot.png")

    print("[graph] All plots generated.")
