import pandas as pd
import matplotlib.pyplot as plt

# Load csv - Best Case
df = pd.read_csv("results/best_case_data_EL_sat_solver_results.csv")

# Make a seperate data frame for Unsatisfiable & Satisfiable problems
Unsatisfiable = df[df["satisfiable"] == "U" ]
Satisfiable = df[df["satisfiable"] == "S" ]
                                               
# Make Satisfiable points & label
plt.scatter(Satisfiable["n_vars"], Satisfiable["time_seconds"], color="green", label="Satisfiable")
for i, label in enumerate(Satisfiable["instance_id"]):
    plt.annotate(label, (Satisfiable["n_vars"].iloc[i], Satisfiable["time_seconds"].iloc[i])) # use iloc to get the index in the dataframe

# Make Unsatisfiable points & label
plt.scatter(Unsatisfiable["n_vars"], Unsatisfiable["time_seconds"], color="red", label="Unsatisfiable")
for i, label in enumerate(Unsatisfiable["instance_id"]):
    plt.annotate(label, (Unsatisfiable["n_vars"].iloc[i], Unsatisfiable["time_seconds"].iloc[i]))

plt.xlabel("Size")
plt.ylabel("Time (s)")
plt.title("Best Case Solver Performance")
plt.legend()

plt.savefig("plot_best_case_results_EL.png", dpi=300, bbox_inches="tight")
plt.close()

# Load csv - Brute Force
df = pd.read_csv("results/brute_force_data_EL_sat_solver_results.csv")

Unsatisfiable = df[df["satisfiable"] == "U" ]
Satisfiable = df[df["satisfiable"] == "S" ]
                                               
# Make Satisfiable points & label
plt.scatter(Satisfiable["n_vars"], Satisfiable["time_seconds"], color="green", label="Satisfiable")
for i, label in enumerate(Satisfiable["instance_id"]):
    plt.annotate(label, (Satisfiable["n_vars"].iloc[i], Satisfiable["time_seconds"].iloc[i]))

# Make Unsatisfiable points & label
plt.scatter(Unsatisfiable["n_vars"], Unsatisfiable["time_seconds"], color="red", label="Unsatisfiable")
for i, label in enumerate(Unsatisfiable["instance_id"]):
    plt.annotate(label, (Unsatisfiable["n_vars"].iloc[i], Unsatisfiable["time_seconds"].iloc[i]))

plt.xlabel("Size")
plt.ylabel("Time (s)")
plt.title("Brute Force Solver Performance")
plt.legend()

plt.savefig("plot_brute_force_results_EL.png", dpi=300, bbox_inches="tight")
plt.close()