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
        # define bitmask based on v * e
        # go up to that in binary
        # we just keep incrementing the mask
        # basically, if the mask says 10011, then we set the first vertex to 1, second to 1, third to 0, etc.

        for mask in range(1 << n_vars):

            assignment = {var: bool(mask & (1 << (var - 1))) for var in range(1, n_vars + 1)}   # our current assignment is based on incrementing bitmask

            formula_satisfied = True                # check if assignment satisfies all clauses
            for clause in clauses:
                clause_satisfied = False            # reset clause_satisfied for each new clause we examine

                for term in clause:
                    var = abs(term)                 # take absolute value (accounting for the negated ones)
                    val = assignment[var]           # set the value to be whatever the mask says for that index

                    # if literal is negated, flip the value
                    if term < 0:
                        val = not val

                    # if any literal in the clause is True, clause is True
                    if val:
                        clause_satisfied = True
                        break

                # if a clause is not satisfied, entire formula fails
                if not clause_satisfied:
                    formula_satisfied = False
                    break

            if formula_satisfied:
                # found satisfying assignment
                return True, assignment

        # no satisfying assignment exists
        print('no assignment')
        return False, {}                                     # not good :(

    def sat_bestcase(self, n_vars:int, clauses:List[List[int]]) -> Tuple[bool, Dict[int, bool]]:
        pass

    def sat_simple(self, n_vars:int, clauses:List[List[int]]) -> Tuple[bool, Dict[int, bool]]:
        pass