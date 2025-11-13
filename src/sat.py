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
        

        def clauseSatisfied(clause, assignment):
            for literal in clause:
                var = abs(literal)
                if var in assignment:
                    val = assignment[var]
                    if (literal > 0 and val) or (literal < 0 and not val):
                        return True
            return False
        
        def clauseUnsatisfied(clause, assignment):
            for literal in clause:
                var = abs(literal)
                if var not in assignment:
                    return False  
                val = assignment[var]
                if (literal > 0 and val) or (literal < 0 and not val):
                    return False  
            return True
                

        def final():
            variationsTriedStack = []
            assignment = {}
            allVars = sorted({abs(lit) for clause in clauses for lit in clause})

            while True:
                
                good = 0
                for clause in clauses:
                    if clauseSatisfied(clause, assignment):
                        good += 1

                if good == len(clauses):
                    return (True, assignment)
                
                if any(clauseUnsatisfied(clause, assignment) for clause in clauses):

                    backtracked = False
                    
                    while variationsTriedStack:
                        var, tried = variationsTriedStack.pop()
                        if var in assignment:
                            del assignment[var]
                        if len(tried) < 2: 
                            otherVal = not tried[0]
                            tried.append(otherVal)
                            assignment[var] = otherVal
                            variationsTriedStack.append((var, tried))
                            backtracked = True
                            break
                    if not backtracked:
                        return (False, {})
                    
                unassigned = [v for v in allVars if v not in assignment]
                if not unassigned:
                    good = 0
                    for clause in clauses:
                        if clauseSatisfied(clause, assignment):
                            good += 1
                    if good == len(clauses):
                        return (True, assignment)
                    else: 
                        return (False, {})
                        
                var = unassigned[0]
                assignment[var] = True
                variationsTriedStack.append((var, [True]))            




    def sat_bruteforce(self, n_vars:int, clauses:List[List[int]]) -> Tuple[bool, Dict[int, bool]]:
        satisfiable = False
        count = 0
        while not satisfiable:
            # check to see if all the solutions have been generated
            if count >= 2**n_vars:
                break
            
            # create a solution
            solutions = dict()
            binary = bin(count)[2:].zfill(n_vars)
            assignments = [int(x) for x in list(binary)]
            for index, val in enumerate(assignments):
                if val == 0:
                    solutions[index+1] = False
                else:
                    solutions[index+1] = True
            # check if solution is satisfiable
            for clause in clauses:
                good = 0
                for val in clause:
                    if val<0:
                        a = not(solutions[abs(val)])
                        if a: good = 1
                    else:
                        a = solutions[abs(val)]
                        if a: good = 1
                if not good:
                    break # break out of the for loop
            
            # if satisfiable - break and call a day
            if good:
                #print("good")
                #print(solutions)
                satisfiable = 1
            # increment
            count += 1 
            
        if not satisfiable:
            #print("bad")
            return (False, {})
        else:
            return (True, solutions)


    def sat_bestcase(self, n_vars:int, clauses:List[List[int]]) -> Tuple[bool, Dict[int, bool]]:
        pass

    def sat_simple(self, n_vars:int, clauses:List[List[int]]) -> Tuple[bool, Dict[int, bool]]:
        pass