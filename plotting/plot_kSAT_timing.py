import csv
import matplotlib.pyplot as plt

csv_path = "results/btracking_kSAT_sat_solver_results.csv"

x_sat = []
y_sat = []
x_unsat = []
y_unsat = []

with open(csv_path, newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        size = int(row["n_clauses"])        # or int(row["n_vars"])
        time = float(row["time_seconds"])
        sat_flag = row["satisfiable"]

        if sat_flag == "S":
            x_sat.append(size)
            y_sat.append(time)
        else:
            x_unsat.append(size)
            y_unsat.append(time)

plt.scatter(x_sat, y_sat, label="Satisfiable", marker="o")   # make this green in your IDE
plt.scatter(x_unsat, y_unsat, label="Unsatisfiable", marker="o")  # make this red

plt.xlabel("Problem size (number of clauses)")
plt.ylabel("Runtime (seconds)")
plt.title("Backtracking SAT Solver Timing on k-SAT Instances")
plt.legend()
plt.tight_layout()

plt.savefig("plotting/plotting_results/kSAT_Backtracking_Plot.png", dpi=300)