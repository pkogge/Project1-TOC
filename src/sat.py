"""
SAT Solver - DIMACS-like Multi-instance Format
----------------------------------------------------------
Project 1: Tough Problems & The Wonderful World of NP

INPUT FORMAT (multi-instance file):
-----------------------------------
Each instance starts with a comment and a problem definition:

c <instance_id> <k> <status?>
p cnf <n_vertices> <n_edges>
u,v
x,y
...

Example:
c 1 3 ?
p cnf 4 5
1,2
1,3
2,3
2,4
3,4
c 2 2 ?
p cnf 3 3
1,2
2,3
1,3

OUTPUT:
-------
A CSV file named 'resultsfile.csv' with columns:
instance_id,n_vars,n_clauses,method,satisfiable,time_seconds,solution


EXAMPLE OUTPUT
------------
instance_id,n_vars,n_clauses,method,satisfiable,time_seconds,solution
3,4,10,U,0.00024808302987366915,BruteForce,{}
4,4,10,S,0.00013304100139066577,BruteForce,"{1: True, 2: False, 3: False, 4: False}"
"""

from typing import List, Tuple, Dict
from src.helpers.sat_solver_helper import SatSolverAbstractClass
import itertools


class SatSolver(SatSolverAbstractClass):

    """
        NOTE: The output of the CSV file should be same as EXAMPLE OUTPUT above otherwise you will loose marks
        For this you dont need to save anything just make sure to return exact related output.
        
        For ease look at the Abstract Solver class and basically we are having the run method which does the saving
        of the CSV file just focus on the logic
    """

    def sat_backtracking(self, n_vars:int, clauses:List[List[int]]) -> Tuple[bool, Dict[int, bool]]:
        pass

    def sat_bruteforce(self, n_vars:int, clauses:List[List[int]]) -> Tuple[bool, Dict[int, bool]]:
        for bits in itertools.product([False, True], repeat=n_vars):
            assignment = {i+1: bits[i] for i in range(n_vars)}
            ok = True
            for clause in clauses:
                clause_sat = False
                for x in clause:
                    if x == 0:
                        continue
                    var = abs(x)
                    val = assignment.get(var, False)
                    if (x>0 and val) or (x<0 and not val):
                        clause_sat = True
                        break
                if not clause_sat:
                    ok = False
                    break
            if ok:
                return True, assignment
        return False, {}


    def sat_bestcase(self, n_vars:int, clauses:List[List[int]]) -> Tuple[bool, Dict[int, bool]]:
        def evaluate(assignment: Dict[int, bool]) -> Tuple[bool, int]:
            count = 0 #running counter

            for clause in clauses: #iterates over clauses and assumes false
                satisfied = False
                
                for lit in clause: #check each literal in clause
                    var = abs(lit)
                    val = assignment[var]
                    if (lit > 0 and val) or (lit < 0 and not val): #checks if satisfied
                        satisfied = True
                        break

                if satisfied:
                    count += 1
                else:
                    return False, count

            return True, count

        best_satisfied = -1 #keeps track of best so far
        best_assignment: Dict[int, bool] = {}

        for mask in range(1 << n_vars): #try every possible assignment
            assignment = {}

            for v in range(1, n_vars + 1):
                assignment[v] = bool(mask & (1 << (v - 1)))

            is_sat, sat_count = evaluate(assignment)

            if is_sat: #if good, return
                return True, assignment

            if sat_count > best_satisfied: #if not, save the best so far
                best_satisfied = sat_count
                best_assignment = assignment.copy()

        return False, best_assignment #if nothing good, return best partial

    def sat_simple(self, n_vars:int, clauses:List[List[int]]) -> Tuple[bool, Dict[int, bool]]:
        pass