import os
import re
from typing import List, Tuple, Any

def _tokenize_dimacs_line(line: str) -> List[str]:
    """
    Normalize a DIMACS/CSV-DIMACS line into a list of tokens.
    Supports space-separated, comma-separated, or mixed.
    """
    line = line.strip()
    if not line:
        return []
    # split on commas OR whitespace
    tokens = [t for t in re.split(r"[,\s]+", line) if t]
    return tokens

def parse_multi_instance_dimacs(path: str) -> List[Tuple[str, int, List[List[int]]]]:
    """
    Parses a DIMACS-like file containing multiple CNF instances.
    Returns a list of (instance_id, n_vars, clauses) tuples.

    Now supports:
      - space-separated DIMACS (standard)
      - comma-separated DIMACS-like lines (CSV-style)
      - mixtures of commas and whitespace
    """

    if not os.path.exists(path):
        raise Exception(f"File path: {path} does not exists!!")

    instances: List[Tuple[str, int, List[List[int]]]] = []

    with open(path) as f:
        # keep non-empty lines only
        lines = [ln.strip() for ln in f if ln.strip()]

    i = 0
    while i < len(lines):
        line = lines[i]
        tokens = _tokenize_dimacs_line(line)

        if not tokens:
            i += 1
            continue

        # Instance header line: starts with 'c' (or 'c,' in CSV style)
        if tokens[0] == "c":
            # Example comment line:
            #   c 3 2 ?
            #   c,1000,2,?
            instance_id = tokens[1] if len(tokens) > 1 else str(len(instances) + 1)

            i += 1
            if i >= len(lines):
                break

            # Expect next line: p cnf n_vars n_clauses (spaces or commas)
            header_tokens = _tokenize_dimacs_line(lines[i])
            if len(header_tokens) < 4 or header_tokens[0] != "p" or header_tokens[1] != "cnf":
                raise ValueError(f"Expected 'p cnf' after {line}")

            n_vars = int(header_tokens[2])
            n_clauses = int(header_tokens[3])

            i += 1
            clauses: List[List[int]] = []

            # Read up to n_clauses clause lines, stopping early if we hit a new 'c' line
            for _ in range(n_clauses):
                if i >= len(lines):
                    break

                clause_line = lines[i]
                clause_tokens = _tokenize_dimacs_line(clause_line)
                if not clause_tokens:
                    i += 1
                    continue

                # New instance starts → stop reading clauses for this one
                if clause_tokens[0] == "c":
                    break

                # Convert clause tokens to ints, ignoring the terminating 0
                clause = [int(x) for x in clause_tokens if x != "0"]
                if clause:
                    clauses.append(clause)

                i += 1

            instances.append((instance_id, n_vars, clauses))
        else:
            # Not a 'c' line → skip
            i += 1

    return instances



def parse_multi_instance_graph(path: str):
    """
    Parse file into list of (instance_id, k, n_vertices, edges)
    Each instance starts with `c` and `p edge` lines.
    """
    instances = []
    with open(path) as f:
        lines = [ln.strip() for ln in f if ln.strip()]

    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("c "):
            parts = line.split()
            instance_id = parts[1] if len(parts) > 1 else str(len(instances) + 1)
            k = int(parts[2]) if len(parts) > 2 else 3
            i += 1
            if i >= len(lines) or not lines[i].startswith("p cnf"):
                raise ValueError(f"Expected 'p cnf' after line: {line}")
            _, _, n_vertices_str, n_edges_str = lines[i].split()
            n_vertices = int(n_vertices_str)
            n_edges = int(n_edges_str)
            i += 1
            edges = []
            # Read next n_edges lines (edge pairs)
            for _ in range(n_edges):
                if i >= len(lines) or lines[i].startswith("c "):
                    break
                parts = lines[i].replace(",", " ").split()
                if len(parts) >= 2:
                    u, v = int(parts[0]), int(parts[1])
                    edges.append((u - 1, v - 1))  # use 0-based indexing
                i += 1
            instances.append((instance_id, k, n_vertices, edges))
        else:
            i += 1

    return instances
    
    
def parse_multi_instance_bin_packing(path: str):
    """
    Parse file into list of (instance_id, n_items, item_sizes, bin_capacity)
    Each instance starts with `c` and `p edge` lines.
    """
    instances = []
    with open(path) as f:
        lines = [ln.strip() for ln in f if ln.strip()]

    i = 0
    for temp_line in lines:
        line = [int(line) for line in temp_line.split(" ")]
        instances.append(line)
    return instances
    
def parse_cnf_instances_hamilton(filename):
    instances = []
    current_instance: dict[str, Any] = {}
    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith("c INSTANCE"):
                if current_instance:
                    instances.append(current_instance)
                instance_id = int(line.split()[-1])
                current_instance = {"id": instance_id, "vertices": set(), "edges": []}
            elif line.startswith("p edge"):
                parts = line.split()
                current_instance["num_vertices"] = int(parts[2])
                current_instance["num_edges"] = int(parts[3])
            elif line.startswith("e"):
                u, v = map(int, line.split()[1:])
                current_instance["edges"].append((u, v))
                current_instance["vertices"].update([u, v])
        if current_instance:
            instances.append(current_instance)
    return instances