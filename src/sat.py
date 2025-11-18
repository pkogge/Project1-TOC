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
,4,10,S,0.00013304100139066577,BruteForce,"{1: True, 2: False, 3: False, 4: False}"
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

        
        # correct implementation: sat_solver.py

        def simp_clause(clause, assignment):
            new_clause = []
            for c in clause:
                c_sat = False
                new_c = []
                for literal in c:
                    var = abs(literal)
                    if var in assignment:
                        if (literal > 0 and assignment[var]) or (literal < 0 and not assignment[var]):
                            c_sat = True
                            break
                    else:
                        new_c.append(literal)
                if c_sat:
                    continue
                if not new_c:
                    return None, "UNSAT"
                new_clause.append(new_c)
            if not new_clause:
                return new_clause, "SAT"
            return new_clause, "UNKNOWN"

        def unit_prop(clause, assignment):
            changed = True
            while changed:
                changed = False
                for c in clause:
                    if len(c) == 1:
                        literal = c[0]
                        var = abs(literal)
                        val = (literal > 0)
                        if var in assignment:
                            if assignment[var] != val:
                                return None, None
                        else:
                            assignment[var] = val
                            changed = True
                            clause, status = simp_clause(clause, assignment)
                            if status == "UNSAT":
                                return None, None
                            if status == "SAT":
                                return assignment, clause
                            break
            return assignment, clause

        def pure_literal_elim(clause, assignment, var_count):
            changed = True
            while changed:
                changed = False
                polarity = {}
                for c in clause:
                    for literal in c:
                        var = abs(literal)
                        if var in assignment:
                            continue
                        sign = 1 if literal > 0 else -1
                        if var not in polarity:
                            polarity[var] = sign
                        elif polarity[var] != sign:
                            polarity[var] = 0
                for v, p in polarity.items():
                    if p != 0:
                        assignment[v] = (p > 0)
                        changed = True
                        clause, status = simp_clause(clause, assignment)
                        if status == "UNSAT":
                            return None, None
                        if status == "SAT":
                            return assignment, clause
                        break
            return assignment, clause

        def var_pick(clause, assignment, var_count):
            for var in range(1, var_count + 1):
                if var not in assignment:
                    return var
            return None

        def dpll(clause, assignment, var_count):
            clause, status = simp_clause(clause, assignment)
            if status == "SAT":
                return assignment
            if status == "UNSAT":
                return None
            temp = assignment.copy()
            temp, clause = unit_prop(clause, temp)
            if temp is None:
                return None
            temp, clause = pure_literal_elim(clause, temp, var_count)
            if temp is None:
                return None
            clause, status = simp_clause(clause, temp)
            if status == "SAT":
                return temp
            if status == "UNSAT":
                return None
            var = var_pick(clause, temp, var_count)
            if var is None:
                return None
            new_assignment = temp.copy()
            new_assignment[var] = True
            result = dpll(clause, new_assignment, var_count)
            if result is not None:
                return result
            new_assignment = temp.copy()
            new_assignment[var] = False
            result = dpll(clause, new_assignment, var_count)
            return result

        # run the solver
    
        result = dpll(clauses, {}, n_vars)

        if result is None:
            return False, {}

        final_assignment = {var: result.get(var, True) for var in range(1, n_vars + 1)}
        return True, final_assignment
















    def sat_bruteforce(self, n_vars:int, clauses:List[List[int]]) -> Tuple[bool, Dict[int, bool]]:
        pass

    def sat_bestcase(self, n_vars:int, clauses:List[List[int]]) -> Tuple[bool, Dict[int, bool]]:
        pass

    def sat_simple(self, n_vars:int, clauses:List[List[int]]) -> Tuple[bool, Dict[int, bool]]:
        pass
