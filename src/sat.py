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

    def sat_backtracking(self, n_vars:int, clauses:List[List[int]]) -> Tuple[bool, Dict[int, bool]]:
        pass

    def sat_bruteforce(self, n_vars:int, clauses:List[List[int]]) -> Tuple[bool, Dict[int, bool]]:
        #edge case checks
        if any(len(c) == 0 for c in clauses):
            return False, {}
        if not clauses:
            return True, {}
        
        #create empty dictionary to store variable assignments
        #will map variable numbers to either 0 or 1, which represents true or false
        assignment: Dict[int, int] = {}

        #recursive call to helper function
        success = self.incremental_sat(clauses, n_vars, assignment, 1)
        
        #no satisfying assignments found
        if not success:
            return False, {}
        
        #converting 0s and 1s to True and Falses, since that is the output format
        assign = {i: bool(assignment.get(i, 0)) for i in range(1, n_vars + 1)}
        return True, assign

    def sat_bestcase(self, n_vars:int, clauses:List[List[int]]) -> Tuple[bool, Dict[int, bool]]:
        pass

    def sat_simple(self, n_vars:int, clauses:List[List[int]]) -> Tuple[bool, Dict[int, bool]]:
        pass
    
    def is_clause_satisfied(self, clause, assignment):
        for literal in clause:
            var = abs(literal)
            value = assignment.get(var) #looking at the current assignment of this variable (0 or 1)

            #if the value of the literal is positive and the satisfiability is 1 then true
            if literal > 0 and value == 1:
                return True

            #if the value is negative and the satisfiability is 0 then true, since if literal is false then the negation of it is true
            if literal < 0 and value == 0:
                return True

        return False

    def _formula_satisfied(self, clauses, assignment):
        #if any clause is unsatisfied then the whole formula is unsatisfied
        for clause in clauses:
            if not self.is_clause_satisfied(clause, assignment):
                return False
        return True

    def incremental_sat(self, clauses, n_vars, assignment, depth):
        #recursive backtracking --> but the reason this is brute force is because this function doesn't cut off
        #partial assignments, it checks clauses once all variables are assigned which is brute force

        #base case, if we have assigned all the variables check if formula is satisfied
        if depth > n_vars:
            return self._formula_satisfied(clauses, assignment)

        #trying different assignments using recursion
        assignment[depth] = 1
        if self.incremental_sat(clauses, n_vars, assignment, depth + 1):
            return True
        assignment[depth] = 0
        if self.incremental_sat(clauses, n_vars, assignment, depth + 1):
            return True

        #backtrack if neither true nor false worrked remove this variable assignment
        assignment.pop(depth, None)
        return False



