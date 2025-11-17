import csv
import matplotlib.pyplot as plt

# Path to your results file
csv_file = "results/data_GC.csv"

instance_ids = []
sizes = []      # using number of clauses as size
times = []
colors = []    

with open(csv_file, "r") as f:
    r = csv.DictReader(f)
    for row in r:
        instance_ids.append(int(row["instance_id"]))
        sizes.append(int(row["n_clauses"]))
        times.append(float(row["time_seconds"]))
        colors.append("green" if row["satisfiable"] == "S" else "red")

plt.figure(figsize=(8, 6))
plt.scatter(sizes, times, c=colors)

# Labels
plt.xlabel("Number of Clauses (Problem Size)")
plt.ylabel("Time (Seconds)")
plt.title("SAT Brute Force Solver - Time vs Problem Size")

# Legend
handles = [
    plt.Line2D([0], [0], marker='o', color='w', label='Satisfiable',
               markerfacecolor='green', markersize=10),
    plt.Line2D([0], [0], marker='o', color='w', label='Unsatisfiable',
               markerfacecolor='red', markersize=10),
]
plt.legend(handles=handles)

plt.grid(True)

# SAVE IMAGE
output_path = "results/sat_result_plot_GC.png"
plt.savefig(output_path, dpi=300)
plt.show()
