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
        import time
        start = time.perf_counter()
        
        for pattern in itertools.product([False, True], repeat=n_vars):
            
            #Creating mapping for True and False variable assignment
            choice = {i + 1: pattern[i] for i in range(n_vars)}
            
            allClauseGood = True

            #Checking/Iterating through the clauses
            for clause in clauses:
                clauseGood = False
                #Checking/Iterating through literals
                for litty in clause:
                    varid = abs(litty)
                    val = choice[varid]

                    #if litty>0 then val should be true, if litty<0 then val should be false
                    if (litty > 0 and val is True) or (litty < 0 and val is False):
                        clauseGood = True
                        break
                
                if not clauseGood:
                    allClauseGood = False
                    break
            if allClauseGood:
                self.last_runtime = time.perf_counter() - start
                return True, choice
        self.last_runime = time.perf_counter() - start
        return False, {}
                    

    def sat_bestcase(self, n_vars:int, clauses:List[List[int]]) -> Tuple[bool, Dict[int, bool]]:
        pass

    def sat_simple(self, n_vars:int, clauses:List[List[int]]) -> Tuple[bool, Dict[int, bool]]:
        pass
