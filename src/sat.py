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

Better example:
c 1 2 U             // c - comment line     1 - problem number  2 - num literals possible   U - unsatisfiable
p cnf 4 10          // p - problem line     cnf - type of file  4 - num variables           10 - num clauses
-2,-3,0             // each clause ended with a 0 to mark end of clause
4,4,0               
-2,-4,0
4,1,0
-3,1,0
-1,-1,0
-4,-4,0
2,-4,0
-3,2,0
-3,-4,0
c 2 2 S             // to track end of problem look for next 'c'




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

    def sat_bruteforce(self, n_vars:int, clauses:List[List[int]]) -> Tuple[bool, Dict[int, bool]]:
        # Use itertools.product to generate all possible True/false combos one at a time
        for values in itertools.product([False, True], repeat=n_vars):
            # Create a dict to store variable assignments
            # assignmnet = {1: True, 2: False, 3: True}
            assignment = {}
            for i in range(n_vars):
                assignment[i+1] = values[i]

            # Initialize all clauses to satisfied until we find one that isn't
            satisfied = True

            # Check each clause in the CNF
            for clause in clauses:
                clause_satisfied = False # Assume that this clause is not satisfied first

                # Go through each literal in the clause - if one of them is true, then the clause is satisfied
                for literal in clause:
                    variable_num = abs(literal) # Get variable number, need to ignore sign
                    variable_val = assignment[variable_num] # Get the true/false value

                    # Literal is positive - then it is true if the variable is true
                    if literal > 0 and variable_val:
                        clause_satisfied = True
                        break # Do not need to check rest of this clause - it is satisfied if one is true

                    # Literal is negative - then it is true if the variable is false
                    elif literal <0 and not variable_val:
                        clause_satisfied = True
                        break

                # If the clause failed, then mark unsatisfied
                if not clause_satisfied:
                    satisfied = False
                    break

            # If all clauses passed, then it is satisfied; return true and assignment
            if satisfied:
                return (True, assignment)
            
        # No assignment found
        return (False, {})

    def sat_bestcase(self, n_vars:int, clauses:List[List[int]]) -> Tuple[bool, Dict[int, bool]]:
        # Initialize a tracker & assignmnet to keep the score of the best overall assignment
        best_tracker = 0
        best_assignment = {}

        # Use itertools.product to generate all possible True/false combos one at a time
        for values in itertools.product([False, True], repeat=n_vars):
            # Initialize tracker to record "goodness" of each combo
            tracker = 0

            # Create a dict to store variable assignments
            # assignmnet = {1: True, 2: False, 3: True}
            assignment = {}
            for i in range(n_vars):
                assignment[i+1] = values[i]

            # Initialize all clauses to satisfied until we find one that isn't
            satisfied = True

            # Check each clause in the CNF
            for clause in clauses:
                clause_satisfied = False # Assume that this clause is not satisfied first

                # Go through each literal in the clause - if one of them is true, then the clause is satisfied
                for literal in clause:
                    variable_num = abs(literal) # Get variable number, need to ignore sign
                    variable_val = assignment[variable_num] # Get the true/false value

                    # Literal is positive - then it is true if the variable is true
                    if literal > 0 and variable_val:
                        clause_satisfied = True
                        tracker+=1
                        break # Do not need to check rest of this clause - it is satisfied if one is true

                    # Literal is negative - then it is true if the variable is false
                    elif literal <0 and not variable_val:
                        clause_satisfied = True
                        tracker+=1
                        break

                # If the clause failed, then mark unsatisfied but do not break - we want to try for best case
                if not clause_satisfied:
                    satisfied = False

            # If we get a satisfiable set of assignments, then it is automatically the best case - return it
            # If all clauses passed, then it is satisfied; return true and assignment
            if satisfied:
                return (True, assignment)
            
            # If it is not satisfiable but we have a better case, update best tracker & best assignment
            if tracker > best_tracker:
                best_tracker = tracker
                for i in range(n_vars):
                    best_assignment[i+1] = values[i]
            
        # Return best case assignment found
        return (False, best_assignment)
    
    def sat_backtracking(self, n_vars:int, clauses:List[List[int]]) -> Tuple[bool, Dict[int, bool]]:
        pass

    def sat_simple(self, n_vars:int, clauses:List[List[int]]) -> Tuple[bool, Dict[int, bool]]:
       pass