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
        #go over all possible assignemnt of n_vars booleans
        for values in itertools.product([False, True], repeat=n_vars):
            assignment = {i + 1: val for i, val in enumerate(values)} #turn the tuple into a dict

            all_clauses_ok = True #assume this assignemnt works until we find a bad clause
            for clause in clauses: #check every clause under this assignment
                clause_ok = False #start by assuming clause is false
                for literal in clause: #go through each literal in clause
                    var_num = abs(literal) #get variable index
                    var_is_true = assignment[var_num] #truth value of var in current assignment
                    literal_is_true = var_is_true if literal > 0 else (not var_is_true) #find truth of the literal itself
                    if literal_is_true: #if literal is true, the whole clause is true
                        clause_ok = True
                        break #no need to check other literals in clause

                if not clause_ok: #if clause false, this assignemnt fails
                    all_clauses_ok = False
                    break #no need to check the reamining clauses

            if all_clauses_ok: #if every clause was true, we found a satisfying assignment
                return True, assignment

        return False, {} #if we tried all assignments and none worked, the formula is unsatisfiable

    def sat_bestcase(self, n_vars:int, clauses:List[List[int]]) -> Tuple[bool, Dict[int, bool]]:
        pass

    def sat_simple(self, n_vars:int, clauses:List[List[int]]) -> Tuple[bool, Dict[int, bool]]:
        pass
