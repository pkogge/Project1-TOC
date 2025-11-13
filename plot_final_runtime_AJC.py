import csv
import os
from collections import defaultdict

import matplotlib.pyplot as plt

# ------------- USER CONFIGURATION -------------
# List the CSVs you want to combine
CSV_FILES = [
    "results/brute_force_cnffile_sat_solver_results_AJC.csv",
    "results/brute_force_2SAT_sat_solver_results_AJC.csv",
    "results/brute_force_kSAT_sat_solver_results_AJC.csv",
]

# Only keep instances with n_vars <= this (set to None for no cap)
MAX_N_VARS = 20

# To avoid overplotting, keep at most this many points for each n_vars
MAX_POINTS_PER_N = 10  # set to None to keep all

# Output plot path
OUTPUT_PLOT = "plots_AJC/final_bruteforce_runtime_AJC.png"
# ------------- END CONFIGURATION -------------


def parse_bool_like(value: str) -> bool:
    """
    Interpret the 'satisfiable' column flexibly.
    We expect either:
      - 'S' / 'U'
      - 'True' / 'False'
      - '1' / '0'
    Anything truthy-ish -> True, else False.
    """
    v = value.strip().lower()
    if v in {"s", "true", "1", "t", "yes", "y"}:
        return True
    return False


def load_points_from_csv(csv_path: str,
                         max_n_vars=None,
                         max_points_per_n=None):
    """
    Load (n_vars, time_seconds, satisfiable) triples from a csv file,
    applying optional filters.
    """
    points = []
    counts_per_n = defaultdict(int)

    if not os.path.exists(csv_path):
        print(f"[WARN] CSV file not found: {csv_path}")
        return points

    with open(csv_path, "r", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                n_vars = int(row["n_vars"])
                t = float(row["time_seconds"])
                sat_flag = parse_bool_like(row["satisfiable"])
            except (KeyError, ValueError) as e:
                print(f"[WARN] Skipping row in {csv_path} due to parse error: {e}")
                continue

            # Filter by max_n_vars if requested
            if max_n_vars is not None and n_vars > max_n_vars:
                continue

            # Optional cap on number of points per n_vars
            if max_points_per_n is not None:
                if counts_per_n[n_vars] >= max_points_per_n:
                    continue

            counts_per_n[n_vars] += 1
            points.append((n_vars, t, sat_flag))

    print(f"[INFO] Loaded {len(points)} points from {csv_path}")
    return points


def main():
    # gather all points from all CSVs
    all_points = []
    for path in CSV_FILES:
        pts = load_points_from_csv(path,
                                   max_n_vars=MAX_N_VARS,
                                   max_points_per_n=MAX_POINTS_PER_N)
        all_points.extend(pts)

    if not all_points:
        print("[ERROR] No data points loaded. Check CSV paths / filters.")
        return

    # separate x, y, colors
    x_vals = []
    y_vals = []
    colors = []

    for n_vars, t, sat_flag in all_points:
        x_vals.append(n_vars)
        y_vals.append(t)
        # green for satisfiable, red for unsatisfiable
        colors.append("green" if sat_flag else "red")

    plt.figure()
    plt.scatter(x_vals, y_vals, c=colors)

    plt.xlabel("Number of Variables (n)")
    plt.ylabel("Runtime (seconds)")
    plt.title("Brute-Force SAT Runtime vs Problem Size (Combined Instances)")
    plt.grid(True)

    # Legend (green=SAT, red=UNSAT)
    import matplotlib.patches as mpatches
    sat_patch = mpatches.Patch(color="green", label="SAT (Satisfiable)")
    unsat_patch = mpatches.Patch(color="red", label="UNSAT (Unsatisfiable)")
    plt.legend(handles=[sat_patch, unsat_patch])

    # Make sure output directory exists
    out_dir = os.path.dirname(OUTPUT_PLOT)
    if out_dir and not os.path.exists(out_dir):
        os.makedirs(out_dir, exist_ok=True)

    plt.tight_layout()
    plt.savefig(OUTPUT_PLOT)
    print(f"[INFO] Saved final runtime plot to: {OUTPUT_PLOT}")
    # Uncomment if you want to see it interactively
    # plt.show()


if __name__ == "__main__":
    main()
