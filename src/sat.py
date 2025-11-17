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
        max_combos = 2**n_vars                              # total number of assignments = 2^n

        for num in range(max_combos):                       # go through every possible combo 
            assignment = {}
            for i in range(n_vars): 
                assignment[i+1] = bool((num>>i)&1)          # change into 0 or one T/F 

            satisfied = True                                # assume satisfied first 

            for clause in clauses:                          # check each clause under current assignmet 
                clause_satisfied = False                    # assume false first 
            
                for literal in clause: 
                    var = abs(literal) 
                    val = assignment[var] 
                    if literal < 0: 
                        val = not val
                    if val: 
                        # found something that makes it true 
                        clause_satisfied = True  
                        break 
                if not clause_satisfied: 
                    # once false all false 
                    satisfied = False 
                    break 
            
            # found a satisfying assignment for all clauses 
            if satisfied: 
                return True, assignment
        
        # if after everything still false then it is unsatisfiable 
        return False, {}


    def sat_bestcase(self, n_vars:int, clauses:List[List[int]]) -> Tuple[bool, Dict[int, bool]]:
        pass

    def sat_simple(self, n_vars:int, clauses:List[List[int]]) -> Tuple[bool, Dict[int, bool]]:
        pass 

