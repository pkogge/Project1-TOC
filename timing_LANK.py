"""Generate timing plots for bin packing"""
import csv
import time
from src.bin_packing_LANK import BinPacking
import matplotlib.pyplot as plt

test_file = "module_tests/test_data_LANK.txt"
packer = BinPacking(test_file, result_file_name="timing_test")

results = []
for i, instance in enumerate(packer.solution_instances):
    bin_capacity = instance[0]
    items = instance[1:]
    
    start = time.perf_counter()
    solutions = packer.binpacking_backtracing(bin_capacity, items)
    elapsed = time.perf_counter() - start
    
    results.append({
        'instance': i,
        'num_items': len(items),
        'bin_capacity': bin_capacity,
        'num_solutions': len(solutions),
        'time_sec': elapsed
    })
    print(f"Instance {i}: {len(items)} items, {len(solutions)} solutions, {elapsed:.6f}s")

# Save CSV
with open("results/timing_results_LANK.csv", 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['instance', 'num_items', 'bin_capacity', 'num_solutions', 'time_sec'])
    writer.writeheader()
    writer.writerows(results)

# Generate plot with color coding
has_solution = [r for r in results if r['num_solutions'] > 0]
no_solution = [r for r in results if r['num_solutions'] == 0]

plt.figure(figsize=(10, 6))

# Plot points with solutions
if has_solution:
    items_yes = [r['num_items'] for r in has_solution]
    times_yes = [r['time_sec'] for r in has_solution]
    plt.scatter(items_yes, times_yes, color='blue', label='Solution exists')

# Plot points with no solution
if no_solution:
    items_no = [r['num_items'] for r in no_solution]
    times_no = [r['time_sec'] for r in no_solution]
    plt.scatter(items_no, times_no, color='orange', label='No solution')

plt.xlabel('Number of Items')
plt.ylabel('Time (seconds)')
plt.title('Bin Packing Backtracking Performance')
plt.legend()
plt.grid(True, alpha=0.3)
plt.yscale('log')
plt.savefig("results/plots_timing_LANK.png", dpi=300, bbox_inches='tight')


