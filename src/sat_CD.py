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
        
        # Total number of assignments = 2^n_vars
        total = 1 << n_vars

        # Loop over every possible assignment encoded as an integer
        # Example: n_vars = 3 -> (000, 001, 010, ..., 111)
        # Using a bitmask
        for mask in range(total):

            # Convert the integer mask to an assignment dict
            # bit i of mask determines variable (i+1)
            assignment = {}
            for i in range(n_vars):
                # Get the i-th bit: 1 -> True, 0 -> False
                bit = (mask >> i) & 1
                assignment[i+1] = bool(bit)

            # Assume this assignment works until we find a failing clause
            all_clauses_ok = True

            for clause in clauses:
                # Remove trailing zeros
                cl = [lit for lit in clause if lit != 0]

                # Check if this clause is satisfied under the current assignment.
                clause_ok = False
                for lit in cl:
                    # Positive literal: lit is True in assignment
                    if lit > 0 and assignment[lit]:
                        clause_ok = True
                        break
                    # Negative literal: variable must be False
                    if lit < 0 and not assignment[-lit]:
                        clause_ok = True
                        break

                # If this clause fails, no need to check the rest.
                if not clause_ok:
                    all_clauses_ok = False
                    break

            # If this assignment satisfies every clause, we are done
            if all_clauses_ok:
                return True, assignment

        # Exhausted all assignments, so UNSAT.
        return False, {}

    def sat_bestcase(self, n_vars:int, clauses:List[List[int]]) -> Tuple[bool, Dict[int, bool]]:
        pass

    def sat_simple(self, n_vars:int, clauses:List[List[int]]) -> Tuple[bool, Dict[int, bool]]:
        pass