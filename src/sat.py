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
        a = {}
        def valid():
            for clause in clauses:
                sat = False
                unk = False
                for lit in clause:
                    v = abs(lit)
                    if v not in a:
                        unk = True
                    else:
                        if (lit > 0 and a[v]) or (lit < 0 and not a[v]):
                            sat = True
                if not sat and not unk:
                    return False
            return True

        def dfs(i):
            if i == n_vars + 1:
                for clause in clauses:
                    if not any((lit > 0 and a[abs(lit)]) or (lit < 0 and not a[abs(lit)]) for lit in clause):
                        return False
                return True
            for val in (False, True):
                a[i] = val
                if valid() and dfs(i+1):
                    return True
            del a[i]
            return False

        if dfs(1):
            return True, a.copy()
        return False, {}

    def sat_bruteforce(self, n_vars:int, clauses:List[List[int]]) -> Tuple[bool, Dict[int, bool]]:
        for bits in itertools.product([False, True], repeat=n_vars):
            a = {i+1: bits[i] for i in range(n_vars)}
            ok = True
            for clause in clauses:
                if not any((lit > 0 and a[abs(lit)]) or (lit < 0 and not a[abs(lit)]) for lit in clause):
                    ok = False
                    break
            if ok:
                return True, a
        return False, {}

    def sat_bestcase(self, n_vars:int, clauses:List[List[int]]) -> Tuple[bool, Dict[int, bool]]:
        a = {}
        def score(var, val):
            s = 0
            for clause in clauses:
                ok = False
                for lit in clause:
                    v = abs(lit)
                    if v == var:
                        if (lit > 0 and val) or (lit < 0 and not val):
                            ok = True
                            break
                    else:
                        if v in a and ((lit > 0 and a[v]) or (lit < 0 and not a[v])):
                            ok = True
                            break
                if ok:
                    s += 1
            return s
        for v in range(1, n_vars+1):
            t = score(v, True)
            f = score(v, False)
            a[v] = True if t >= f else False
        ok = True
        for clause in clauses:
            if not any((lit > 0 and a[abs(lit)]) or (lit < 0 and not a[abs(lit)]) for lit in clause):
                ok = False
                break
        return ok, a

    def sat_simple(self, n_vars:int, clauses:List[List[int]]) -> Tuple[bool, Dict[int, bool]]:
        a = {}

        def unit(clauses, a):
            changed = True
            while changed:
                changed = False
                for clause in clauses:
                    true_clause = False
                    free = []
                    for lit in clause:
                        v = abs(lit)
                        if v in a:
                            if (lit > 0 and a[v]) or (lit < 0 and not a[v]):
                                true_clause = True
                                break
                        else:
                                free.append(lit)
                    if true_clause:
                        continue
                    if len(free) == 0:
                        return False
                    if len(free) == 1:
                        lit = free[0]
                        a[abs(lit)] = lit > 0
                        changed = True
            return True

        if not unit(clauses, a):
            return False, {}

        def dfs(i):
            if i == n_vars + 1:
                for clause in clauses:
                    if not any((lit > 0 and a.get(abs(lit), False)) or (lit < 0 and not a.get(abs(lit), False)) for lit in clause):
                        return False
                return True
            if i in a:
                return dfs(i+1)
            for val in (False, True):
                a[i] = val
                if dfs(i+1):
                    return True
            del a[i]
            return False  
        if dfs(1):
            return True, a.copy()
        return False, {}