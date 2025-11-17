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
from src.helpers.sat_solver_helper_GOODY import SatSolverAbstractClass
import itertools
import time


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
        start_time = time.time()
        totaltries = 1 << n_vars
        totaltries = 2 ** n_vars

        # We will loop 2^n_vars times
        # In each loop, we generate ONE assignment and check it immediately
        for num in range(totaltries):
           
            current_assignment_dict = {i + 1: bool((num >> i) & 1) for i in range(n_vars)}

            #assume dict is a solution
            all_clauses_satisfied = True 
            for clause in clauses:
                
                #for this clause assume not satisfied
                this_clause_satisfied = False
                for literal in clause:
                    
                    #get the actual variable we're using
                    var_num = abs(literal)
                    if literal > 0:
                        #var_num needs to be True in dict
                        if current_assignment_dict[var_num] == True:
                            this_clause_satisfied = True
                            break # Found one! Stop checking this clause.
                    else:
                        #var_num needs to be false in dict
                        if current_assignment_dict[var_num] == False:
                            this_clause_satisfied = True
                            break # Found one! Stop checking this clause.
                
                #check flag after all literals checked
                if not this_clause_satisfied:
                    all_clauses_satisfied = False
                    break #dict was not a solution so stop checking
            
            #after checking all clauses for 'current_assignment_dict'
            if all_clauses_satisfied:
                return (True, current_assignment_dict)
        
        #check if it's taking a loooong time
        elapsed = time.time() - start_time
        if elapsed > 1.0:
            print(f"  Problem with {n_vars} vars took {elapsed:.2f}s")
                
        #If get here means never found one
        return (False, {})
        

    def sat_bestcase(self, n_vars:int, clauses:List[List[int]]) -> Tuple[bool, Dict[int, bool]]:
        pass

    def sat_simple(self, n_vars:int, clauses:List[List[int]]) -> Tuple[bool, Dict[int, bool]]:
        pass




