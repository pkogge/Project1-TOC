import csv
import matplotlib.pyplot as plt

csv_file = "results/brute_force_kSAT_sat_solver_results_AJC.csv" # change based on file being plotted

x_vars = []
y_time = []
colors = []

with open(csv_file, "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        n_vars = int(row["n_vars"])
        time = float(row["time_seconds"])
        sat = row["satisfiable"]   # "S" or "U"

        x_vars.append(n_vars)
        y_time.append(time)

        if sat == "S":
            colors.append("green")
        else:
            colors.append("red")

plt.scatter(x_vars, y_time, c=colors)

plt.xlabel("Number of Variables (n)")
plt.ylabel("Runtime (seconds)")
plt.title("Brute Force SAT Runtime vs. Problem Size")

# Legend hack:
import matplotlib.patches as mpatches
green_patch = mpatches.Patch(color='green', label='Satisfiable')
red_patch = mpatches.Patch(color='red', label='Unsatisfiable')
plt.legend(handles=[green_patch, red_patch])

plt.grid(True)
plt.tight_layout()
plt.savefig("plots_AJC/bruteforce_runtime_kSAT_plot_AJC.png") # change based on file being plotted
plt.show()
