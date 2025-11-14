#!/usr/bin/env python3
import os
import sys
import csv
import time

"""
 AJ Jones ajones42
 
 TOC Project 1 - Backtracking SAT Solver
"""

### DPLL Algorithm implementation

def parse_cnf_files(filename):
    problems = []
    clauses = []
    var_count = 0
    clause_count = 0

    with open(filename, 'r') as f:
        for line in f:  # DIMACS format
            line = line.strip()
            if not line:
                continue  # empty line
            if line.startswith('c'):
                continue  # comment line
            if line.startswith('p'):
                # parse new problem header in DIMACS format
                if clauses:
                    problems.append((var_count, clauses))
                    clauses = []
                cut = line.replace(',', ' ').split()
                _, _, var_count, clause_count = cut
                var_count = int(var_count)
                clause_count = int(clause_count)
                continue
            # clause line
            items = line.replace(',', ' ').split()
            literals = [int(x) for x in items if x != '0']
            if literals:
                clauses.append(literals)

    if clauses:
        problems.append((var_count, clauses))
    
    return problems


"""

simplify clauses given curr assignment

- sat: all clauses satisfied
- unsat: any clause is empty (contradiction)
- unknown: neither


"""

def simp_clause(clause, assignment):
    new_clause = []
    
    for c in clause:
            c_sat = False
            new_c = []
            
            for literal in c:
                var = abs(literal)
                if var in assignment:
                    if (literal > 0 and assignment[var]) or (literal < 0 and not assignment[var]):
                        c_sat = True
                        break
                else:
                    new_c.append(literal)
             
            if c_sat:
                continue

            if not new_c:
                return None, "UNSAT"
            
            new_clause.append(new_c)

    if not new_clause:
        return new_clause, "SAT"
    
    return new_clause, "UNKNOWN"


"""

unit propagation: if a clause has only one literal, it must be true
            - returns an updated assignment + clause, or none 



"""

def unit_prop(clause, assignment):
    changed = True
    
    while changed:
        changed = False
        
        for c in clause:
            if len(c) == 1:
                literal = c[0]
                var = abs(literal)
                val = (literal > 0)
    
                if var in assignment:
                    if assignment[var] != val:
                        return None, None # conflict
                else:
                    assignment[var] = val
                    changed = True
            
                    clause, status = simp_clause(clause, assignment)
                    
                    if status == "UNSAT":
                            return None, None
                    if status == "SAT":
                        return assignment, clause
                    
                    break

    return assignment, clause


"""

choose next unnassigned var to branch onto

choose firt unassigned var



"""   


def var_pick(clause, assignment, var_count):
    
    for var in range(1, var_count + 1):
        if var not in assignment:
            return var
    return None


"""
 dpll algo

"""

def dpll(clause, assignment, var_count):

    #simplify clauses w cur assignment    
    clause, status = simp_clause(clause, assignment)
    
    if status == "SAT":
        return assignment
    if status == "UNSAT":
        return None
    
    #unit prop
    temp = assignment.copy()

    temp, clause = unit_prop(clause, temp)
    
    if temp is None:
        return None
    
    #check
    clause, status = simp_clause(clause, temp)
    if status == "SAT":
        return temp
    
    if status == "UNSAT":
        return None
    
    # branching
    var = var_pick(clause, temp, var_count)
    
    if var is None:
        return None
    
    new_assignment = temp.copy()
    new_assignment[var] = True
    result = dpll(clause, new_assignment, var_count)
    
    if result is not None:
        return result
    
    #back-track : attept to assign false
    new_assignment = temp.copy()
    new_assignment[var] = False
    result = dpll(clause, new_assignment, var_count)
    
    return result


"""

solve sat 

"""

def solve_sat(clause, var_count):
    
    assignment = {}
    return dpll(clause, assignment, var_count)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: python3 sat_solver.py <filename.cnf>")
        sys.exit(1)
    
    filename = sys.argv[1]
    problems = parse_cnf_files(filename)
    
    # save as csv
    csv_filename = "resultsfile.csv"
    with open(csv_filename, mode='w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        # write header
        csv_writer.writerow([
            "instance_id", "n_vars", "n_clauses", "method", "satisfiable", "time_seconds", "solution"
        ])
        
        for i, (var_count, clause) in enumerate(problems, 1):
            print(f"problem {i}:")
            print(f"variables: {var_count}, clause: {len(clause)}")
            
            start_time = time.time()
            result = solve_sat(clause, var_count)
            end_time = time.time()
            
            method = "backtracking"  
            time_taken = end_time - start_time
            satisfiable = 1 if result is not None else 0
            
            if result is not None:
                print("SAT")
                
                # print assignment in order
                assignment_list = []
                for var in range(1, var_count + 1):
                    if var in result:
                        assignment_list.append(var if result[var] else -var)
                    else:
                        assignment_list.append(var)  # Default to True if unassigned
                print(" ".join(map(str, assignment_list)))
                
                solution_dict = {var: result.get(var, True) for var in range(1, var_count + 1)}
            else:
                print("UNSAT")
                solution_dict = {}
            
            # Write to CSV
            csv_writer.writerow([
                i, var_count, len(clause), method, satisfiable, time_taken, solution_dict
            ])
            
            print()
