import matplotlib.pyplot as plt

# Set up the root directory (two levels up from this script)
root_direct = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, root_direct)  # Add root to Python path to allow importing from src

# Import SAT solver and DIMACS parser from src
from src.sat import SatSolver
from src.helpers.dmaics_parser import parse_multi_instance_dimacs

# Path to input directory containing CNF files
dir_path = os.path.join(root_direct, "input")
files = os.listdir(dir_path)  # List all files in the input directory

# Choose a specific CNF file to solve
file = "cnffile.cnf"
path = os.path.join(dir_path, file)
solver = SatSolver(path)
solver.run()  # Run the SAT solver


# Prepare lists to store data points for plotting
# var[0] : number of variables, var[1]: runtime in seconds, var[2] : satisfiable status
var = [[], [], []]

# Set up path to results directory and CSV file containing brute-force results
results_dir = os.path.join(root_direct, "results")
file_name = os.path.splitext(file)[0]  # Extract filename without extension
output = os.path.join(results_dir, f"brute_force_{file_name}_sat_solver_results.csv")

# Open the CSV file and read performance data
with open(output) as fil:
    next(fil)  # Skip the header line
    
    for line in fil:
        components = line.strip().split(",")  # Split CSV line into components
        var[0].append(int(components[1]))     # Number of variables
        var[1].append(float(components[5]))   # Time in seconds
        var[2].append(components[4].strip())  # Satisfiable status ('S' or 'U')

# Print the collected data points for debugging
print(var)

# Plot points with colors based on satisfiable status
for i in range(len(var[0])):
    color = 'green' if var[2][i] == 'S' else 'red'  # Green if satisfiable, red if unsatisfiable
    plt.scatter(var[0][i], var[1][i], c=color, s=50)

# Set plot labels and title
plt.xlabel('Number of Variables')
plt.ylabel('Time (s)')
plt.title('Brute Force SAT')

# Show the plot
plt.show()

