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
        #Dictionary for variable assignments
        assignments = {}

        #Copy of the list of clauses
        clauses_copy = [clause[:] for clause in clauses]

        #Loop flag
        changed = True

        while changed:
            changed = False
            #Look for unit clauses
            for clause in clauses_copy:
                if len(clause) == 1:
                    literal = clause[0]
                    variable = abs(literal)
                
                    if variable not in assignments:
                        assignments[variable] = (literal > 0)
                        changed = True
            
            #Simplify other clauses based on current assignments
            new_clauses = []
            for clause in clauses_copy:
                is_satisfied = False
                new_clause = []

                for literal in clause:
                    variable = abs(literal)
                    if variable in assignments:
                        if (literal > 0 and assignments[variable]) or (literal < 0 and not assignments[variable]):
                            is_satisfied = True
                            break
                    else:
                        new_clause.append(literal)

                if not is_satisfied:
                    #Empty clause means all literals were false
                    if not new_clause:
                        return False, {}
                    new_clauses.append(new_clause)

            #Update the clauses
            clauses_copy = new_clauses

        #If no clauses remain, everything is satisfied
        if not clauses_copy:
            # Fill in any unassigned variables with arbitrary values
            for i in range(1, n_vars + 1):
                if i not in assignments:
                    assignments[i] = False  # or True, doesn't matter
            return True, assignments
        
        #Find the first unassigned variable for branching
        unassigned = None
        for i in range(1, n_vars+1):
            if i not in assignments:
                unassigned = i
                break

        #Try assigning true to the variable
        satisfiable, assignment = self.sat_backtracking(n_vars, clauses_copy + [[unassigned]])
        if satisfiable:
            # Fill in any unassigned variables
            for i in range(1, n_vars + 1):
                if i not in assignment:
                    assignment[i] = False
            return True, assignment
        
        #Try false if True does not work
        return self.sat_backtracking(n_vars, clauses_copy + [[-unassigned]])

    def sat_bruteforce(self, n_vars:int, clauses:List[List[int]]) -> Tuple[bool, Dict[int, bool]]:

        # 2^n possible assignments
        total = 1 << n_vars
        for mask in range(total):
            # Make a literal assignment
            assignment = {}
            for i in range(1, n_vars + 1):
                bit = (mask >> (i - 1)) & 1
                assignment[i] = bool(bit)

            # Evaluate formula with this assignment
            all_clauses_true = True
            for clause in clauses:
                clause_true = False  # tracking OR of literals in clause
                for lit in clause:
                    val = assignment.get(abs(lit), False)
                    if lit < 0:
                        val = not val
                    if val:
                        clause_true = True
                        break  # short circuit OR if one evaluated literal is true
                if not clause_true:
                    all_clauses_true = False
                    break  # short circuit AND if one clause is false

            if all_clauses_true:
                return True, assignment

        # Unsolvable
        return False, {}
            
    def sat_bestcase(self, n_vars:int, clauses:List[List[int]]) -> Tuple[bool, Dict[int, bool]]:
        # Error check
        if not clauses:
            return True, {}

        # 2^n total possible assignments 
        total = 1 << n_vars

        # Keep track of best assignment
        best_assignment = {}
        best_satisfied = -1
        n_clauses = len(clauses)

        for mask in range(total):
            # Make the current literal assignment
            assignment = {}
            for i in range(1, n_vars + 1):
                bit = (mask >> (i - 1)) & 1
                assignment[i] = bool(bit)

            # Test this assignment
            satisfied_count = 0
            for clause in clauses:
                clause_true = False  # OR of literals in clause
                for lit in clause:
                    val = assignment.get(abs(lit), False)
                    if lit < 0:
                        val = not val
                    if val:
                        clause_true = True
                        break  # short circuit
                if clause_true:
                    satisfied_count += 1

            # Update best so far
            if satisfied_count > best_satisfied:
                best_satisfied = satisfied_count
                best_assignment = assignment

                # Full solution found
                if best_satisfied == n_clauses:
                    return True, best_assignment

        # Problem is unsatisfiable
        return False, {}

    def sat_simple(self, n_vars:int, clauses:List[List[int]]) -> Tuple[bool, Dict[int, bool]]:
        pass