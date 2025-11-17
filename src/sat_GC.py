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


    def sat_bruteforce(self, n_vars: int, clauses: List[List[int]]) -> Tuple[bool, Dict[int, bool]]:
        """
        Arg:
        n_vars = The number of variables in the SAT problem.
        clauses = A list of clauses where each clause is a list of literals (variables or their negations).

        Returns:
        A tuple where the first value is a boolean showing whether a solution exists,
        and the second value is a dictionary of variable assignments that satisfy the formula, or an empty one if no solution exists.
        """
        total_assignments = 2 ** n_vars

        for i in range(total_assignments):
            # variable 1 uses the highest bit, variable n uses the lowest bit.
            assignment = {}
            for j in range(n_vars):
                bit_index = n_vars - 1 - j   # make var 1 change slowest, var n fastest
                assignment[j + 1] = bool((i >> bit_index) & 1)

            # Check if this assignment satisfies every clause
            all_ok = True
            for clause in clauses:
                clause_ok = False

                for literal in clause:
                    var = abs(literal)
                    val = assignment[var]

                    # positive literal: needs variable True
                    # negative literal: needs variable False
                    if (literal > 0 and val) or (literal < 0 and not val):
                        clause_ok = True
                        break

                if not clause_ok:
                    all_ok = False
                    break

            if all_ok:
                return True, assignment

        # None of the assignments worked
        return False, {}

    def sat_bestcase(self, n_vars:int, clauses:List[List[int]]) -> Tuple[bool, Dict[int, bool]]:
        pass

    def sat_simple(self, n_vars:int, clauses:List[List[int]]) -> Tuple[bool, Dict[int, bool]]:
        pass