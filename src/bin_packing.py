"""
SAT Solver - DIMACS-like Multi-instance Format
----------------------------------------------------------
Project 1: Tough Problems & The Wonderful World of NP

INPUT FORMAT (multi-instance file):
-----------------------------------
Each instance starts with a comment and a problem definition:

bin_capacity <capacity>
...

Example:
10 2 5 4 7 1 3 8 6

OUTPUT:
-------
A CSV file named 'resultsfile.csv' with columns:
instance_id,bin_capacity,bins_array,method,time_taken


EXAMPLE OUTPUT
------------
instance_id,bin_capacity,bins_array,method,time_taken
0,10,"[8, 2]",BruteForce,9.862499427981675e-05
0,10,"[7, 3]",BruteForce,9.862499427981675e-05

"""

from typing import List

from src.helpers.bin_packing_helper import BinPackingAbstractClass

import copy

class BinPacking(BinPackingAbstractClass):
    """
    NOTE: The output of the CSV file should be same as EXAMPLE OUTPUT above otherwise you will loose marks
    For this you dont need to save anything just make sure to return exact related output.

    For ease look at the Abstract Solver class and basically we are having the run method which does the saving
    of the CSV file just focus on the logic
    """

    def binpacking_backtracing(
        self, bin_capacity: int, clauses: List[int]
    ) -> List[List[int]]:
        
        target = bin_capacity

        def backtrack(idx: int, current_sum: int, current: List[int]):
            if current_sum == target:
                return current[:]
            if current_sum > target or idx == len(clauses):
                return None

            # choose clauses[idx]
            with_curr = backtrack(idx + 1, current_sum + clauses[idx], current + [clauses[idx]])
            if with_curr is not None:
                return with_curr

            # skip clauses[idx]
            return backtrack(idx + 1, current_sum, current)

        sol = backtrack(0, 0, [])
        if sol is not None:
            return [sol]
        return [[-9]]

    def binpacking_bruteforce(
        self, bin_capacity: int, clauses: List[int]
    ) -> List[List[int]]:
        pass

    def binpacking_simple(
        self, bin_capacity: int, clauses: List[int]
    ) -> List[List[int]]:
        pass

    def binpacking_bestcase(
        self, bin_capacity: int, clauses: List[int]
    ) -> List[List[int]]:
        target = bin_capacity

        # dp[s] = list of clause *indices* that sum to s, or None if unreachable
        dp: List[Optional[List[int]]] = [None] * (target + 1)
        dp[0] = []

        for idx, c in enumerate(clauses):
            if c > target:
                continue  # this item can't fit

            # go backwards so we don't reuse the same item multiple times
            for s in range(target, c - 1, -1):
                if dp[s - c] is not None and dp[s] is None:
                    dp[s] = dp[s - c] + [idx]

            # hit the target
            if dp[target] is not None:
                solution = [clauses[i] for i in dp[target]]
                return [solution]

        # no exact packing found
        return [[-9]]

