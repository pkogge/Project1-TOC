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
    # Added helper functions
    def evalute_clause(self, clause, assignment):
        for num in clause:
            if num > 0 and assignment.get(abs(num), None) is True:
                return True
            if num < 0 and assignment.get(abs(num), None) is False:
                return True
        return False
    
    def check_satisfy(self, clauses, assignment):
        for clause in clauses:
            if not self.evalute_clause(clause, assignment):
                return False
        return True
    
    def check_partial(self, clauses, assignment):
        for clause in clauses:
            clause_ok = False
            undecided = False
            for lit in clause:
                var = abs(lit)
                if var not in assignment:
                    undecided = True
                    continue
                val = assignment[var]
                if (lit > 0 and val) or (lit < 0 and not val):
                    clause_ok = True
                    break
            if not clause_ok and not undecided:
                return False
        return True


    def sat_backtracking(self, n_vars:int, clauses:List[List[int]]) -> Tuple[bool, Dict[int, bool]]:
        def backtrack(var_index, assignment):
            if var_index > n_vars:
                if self.check_satisfy(clauses,assignment):
                    return True, assignment
                return False, {}
                
            for val in [True, False]:
                assignment[var_index] = val

                partial_assignment_good = self.check_partial(clauses, assignment)
                if not partial_assignment_good:
                    del assignment[var_index]
                    continue
                
                ok, solution = backtrack(var_index + 1, assignment)
                if ok:
                    return ok, solution
                del assignment[var_index]  # undo this choice
            return False, {}
        
        return backtrack(1, {})


    def sat_bruteforce(self, n_vars:int, clauses:List[List[int]]) -> Tuple[bool, Dict[int, bool]]:
        for assignments in itertools.product([False, True], repeat=n_vars):
            assignment = {i+1: assignments[i] for i in range(n_vars)}
            if self.check_satisfy(clauses, assignment):
                return True, assignment
        return False, {}

    def sat_bestcase(self, n_vars:int, clauses:List[List[int]]) -> Tuple[bool, Dict[int, bool]]:
        pass

    def sat_simple(self, n_vars:int, clauses:List[List[int]]) -> Tuple[bool, Dict[int, bool]]:
        pass