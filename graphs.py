#!/usr/bin/env python3
import matplotlib.pyplot as plt
import pandas as pd

def graph(title: str, filename: str):
    df = pd.read_csv(filename)
    output_filename = "results/"+title+".png"
    x_data = df["bin_capacity"] * df["clauses"]
    y_data = df["time_taken"]

    plt.scatter(x_data, y_data)
    plt.xlabel("Problem size")
    plt.ylabel("Time Taken (milliseconds)")
    plt.title(title)
    plt.grid(True)
    plt.savefig(output_filename)
    print(output_filename)
    plt.close()


if __name__ == "__main__":
    files = [
            {
                "name": "Best Case",
                "path": "best_case_binpacking_solver_results.csv"
                },
            {
                "name": "Brute Force",
                "path": "brute_force_binpacking_solver_results.csv"
                },
            {
                "name": "Back Tracking",
                "path": "btracking_binpacking_solver_results.csv"
                },
            {
                "name": "Simple",
                "path": "simple_binpacking_solver_results.csv"
                }
            ]
    for file in files:
        graph(file["name"], "results/"+file["path"])
