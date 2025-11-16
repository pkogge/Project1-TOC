import csv
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

#Path to .csv output file (change for each method) btracking_kSAT_sat_solver_results.csv
PATH = "btracking_test_sat_solver_results.csv"  

#Initializing variables needed for plot
sizes = []   
times = []   
colors = []  

#Opening path as file and iterating line by line
with open(PATH, newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        
        #Here we use n_clauses as size and collect rest of the variables (time and U or S)
        size = int(row["n_clauses"])      
        time = float(row["time_seconds"])
        sat_flag = row["satisfiable"]     

        #Append
        sizes.append(size)
        times.append(time)
        colors.append("g" if sat_flag == "S" else "r")

#Plot our data and define labels 
plt.figure(figsize=(8, 6))
plt.scatter(sizes, times, c=colors)

plt.xlabel("Problem size (number of clauses)")
plt.ylabel("Time (seconds)")
plt.title("Brute Force Test: Time vs Problem Size")

plt.grid(True, alpha=0.3)

#Legend for the colors
legend_elements = [
    Line2D([0], [0], marker='o', color='w', label='SAT (S)', markerfacecolor='g', markersize=8),
    Line2D([0], [0], marker='o', color='w', label='UNSAT (U)', markerfacecolor='r', markersize=8),
]
plt.legend(handles=legend_elements, loc="upper left")

plt.tight_layout()
plt.savefig("plots/btracking_test_time_vs_size.png", dpi=200)
plt.show()
