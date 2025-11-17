import os
import glob
import pandas as pd
import matplotlib.pyplot as plt

def plot_sat_results(csv_file):
    # Read the CSV file
    file = pd.read_csv(csv_file)
    
    # Get the satisfiable and unsatisfiable instances
    satisfiable = file[file['satisfiable'] == 'S']
    unsatisfiable = file[file['satisfiable'] == 'U']
    
    size_metric = 'n_vars'
    
    # Extract method name from the CSV
    method_name = file['method'].iloc[0]
    
    # Create the plot
    plt.figure(figsize=(10, 6))
    
    # Plot satisfiable instances
    if not satisfiable.empty:
        plt.scatter(
            satisfiable[size_metric],
            satisfiable['time_seconds'],
            c='green',
            marker='o',
            label='Satisfiable',
            s=50,
            alpha=0.7
        )
    
    # Plot unsatisfiable instances
    if not unsatisfiable.empty:
        plt.scatter(
            unsatisfiable[size_metric],
            unsatisfiable['time_seconds'],
            c='red',
            marker='o',
            label='Unsatisfiable',
            s=50,
            alpha=0.7
        )
    
    plt.xlabel(f'Number of literals ({size_metric})', fontsize=12)
    plt.ylabel('Time (seconds)', fontsize=12)
    
    # Title
    base_name = os.path.splitext(os.path.basename(csv_file))[0]
    if method_name:
        plt.title(f'{method_name} – Execution Time vs Number of Literals\n({base_name})', fontsize=14)
    else:
        plt.title(f'Execution Time vs Number of Literals\n({base_name})', fontsize=14)
    
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Make the output filename
    output_file = os.path.join(
        os.path.dirname(csv_file),
        f'{base_name}_timing_plot.png'
    )
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()


if __name__ == "__main__":
    # Find all CSV files in the same directory as this script.
    script_dir = os.path.dirname(os.path.abspath(__file__))
    pattern = os.path.join(script_dir, "*.csv")
    
    csv_files = glob.glob(pattern)
    
    # Ensure that there are existing CSV files in directory
    if not csv_files:
        print("No CSV files found in the results directory.")
    else:
        for csv_file in csv_files:
            plot_sat_results(csv_file)
