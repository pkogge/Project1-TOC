from typing import List, Tuple, Dict
from src.helpers.sat_solver_helper import SatSolverAbstractClass

"""
SAT Solver implementation for Project 1: Tough Problems & The Wonderful World of NP.

This file defines the concrete SatSolver class that implements the abstract
methods declared in SatSolverAbstractClass.

The CNF instances are already parsed for you by SatSolverAbstractClass using
parse_multi_instance_dimacs() in src/helpers/dmaics_parser.py.

For each instance we get:
    - inst_id:   a string or int identifying the instance
    - n_vars:    number of boolean variables (variables are 1..n_vars)
    - clauses:   list of clauses, each clause is a list of ints (literals)
                 * positive int  k  means variable x_k
                 * negative int -k  means ¬x_k

This class only needs to implement:
    - sat_bruteforce:    full brute-force search over all 2^n assignments
    - sat_backtracking:  (not used if you only select brute force; we stub it)
    - sat_simple:        (stub or simple variant)
    - sat_bestcase:      (stub or wrapper if desired)

The SatSolverAbstractClass.run() method will:
    - call sat_bruteforce / sat_backtracking / sat_simple / sat_bestcase
      depending on what is selected in the JSON config
    - time each call
    - save the results in CSV files under the results/ directory.
"""


class SatSolver(SatSolverAbstractClass):
    def __init__(self, cnf_file_input_path: str):
        # Use the base class constructor to parse the CNF and set up config
        super().__init__(cnf_file_input_path)

    # --------- Helper methods for evaluating assignments ---------

    def _clause_is_true(self, clause: List[int], assignment: Dict[int, bool]) -> bool:
        """
        Returns True iff at least one literal in the clause is True
        under the given assignment.
        clause is a list of ints like [1, -3, 4].
        """
        for lit in clause:
            var = abs(lit)
            val = assignment.get(var, False)
            if lit < 0:
                val = not val  # negated literal
            if val:
                return True
        return False

    def _formula_is_true(self, clauses: List[List[int]], assignment: Dict[int, bool]) -> bool:
        """
        Returns True iff every clause in the CNF is True
        under the given assignment.
        """
        for clause in clauses:
            if not self._clause_is_true(clause, assignment):
                return False
        return True

    # --------- Required abstract methods ---------

    def sat_bruteforce(self, n_vars: int, clauses: List[List[int]]) -> Tuple[bool, Dict[int, bool]]:
        """
        Brute-force SAT solver.

        Tries all 2^n_vars possible assignments of boolean values
        to variables 1..n_vars. Returns:

            (True, assignment_dict)   if a satisfying assignment exists
            (False, {})               if the formula is unsatisfiable

        assignment_dict maps variable index -> bool:
            {1: True, 2: False, ...}
        """
        
        MAX_N_FOR_BRUTE = 20  # Adjust as needed to prevent excessive runtimes

        if n_vars > MAX_N_FOR_BRUTE:
            # This prevents the solver from freezing on giant CNFs
            print(f"Skipping brute force for n_vars={n_vars} (> {MAX_N_FOR_BRUTE})")
            return False, {}  # or you can return None/None or "skipped"
        
        # Iterate over all possible bit patterns from 0 to 2^n_vars - 1
        # Bit i (0-based) corresponds to variable (i+1).
        total_assignments = 1 << n_vars  # 2^n_vars

        for mask in range(total_assignments):
            # Build an assignment dict for this mask
            assignment: Dict[int, bool] = {}
            for var in range(1, n_vars + 1):
                # bit position (var-1)
                assignment[var] = bool(mask & (1 << (var - 1)))

            # Check if this assignment satisfies all clauses
            if self._formula_is_true(clauses, assignment):
                return True, assignment

        # No assignment worked: unsatisfiable
        return False, {}

    def sat_backtracking(self, n_vars: int, clauses: List[List[int]]) -> Tuple[bool, Dict[int, bool]]:
        """
        Backtracking version (not required if only brute force is selected).
        For now we just reuse the brute-force solver so the abstract method
        is implemented and the class is concrete.
        """
        return self.sat_bruteforce(n_vars, clauses)

    def sat_bestcase(self, n_vars: int, clauses: List[List[int]]) -> Tuple[bool, Dict[int, bool]]:
        """
        Best-case / "as close as possible" solution.
        For now, we simply call the brute-force solver:
        if satisfiable, we return that satisfying assignment;
        if unsatisfiable, we return (False, {}) as a placeholder.
        """
        return self.sat_bruteforce(n_vars, clauses)

    def sat_simple(self, n_vars: int, clauses: List[List[int]]) -> Tuple[bool, Dict[int, bool]]:
        """
        A simpler or heuristic solver. For now, we just call brute force.
        """
        return self.sat_bruteforce(n_vars, clauses)
