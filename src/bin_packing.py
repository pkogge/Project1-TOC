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
from itertools import product
from collections import deque

from src.helpers.bin_packing_helper import BinPackingAbstractClass


class BinPacking(BinPackingAbstractClass):
    """
    NOTE: The output of the CSV file should be same as EXAMPLE OUTPUT above otherwise you will loose marks
    For this you dont need to save anything just make sure to return exact related output.

    For ease look at the Abstract Solver class and basically we are having the run method which does the saving of the CSV file just focus on the logic
    """

    def binpacking_backtracing(
        self, bin_capacity: int, clauses: List[int]
    ) -> List[List[int]]:
        res = []

        def backtrack(start: int, path: list[int], total: int):
            if total == bin_capacity:
                res.append(path[:])
                return

            if total > bin_capacity:
                return

            for i in range(start, len(clauses)):
                path.append(clauses[i])
                backtrack(i, path, total + clauses[i])
                path.pop()

        backtrack(0, [], 0)

        return res

    def binpacking_bruteforce(
        self, bin_capacity: int, clauses: List[int]
    ) -> List[List[int]]:
        res = []
        clauses = sorted(clauses)
        bounds = [(bin_capacity // c) for c in clauses]

        for counts in product(*[range(b + 1) for b in bounds]):
            if sum(c * n for c, n in zip(clauses, counts)) == bin_capacity:
                comb = [c for c, n in zip(clauses, counts) for _ in range(n)]
                res.append(comb)

        return res

    def binpacking_simple(
        self, bin_capacity: int, clauses: List[int]
    ) -> List[List[int]]:
        clauses = sorted(clauses)
        combs = {0: [[]]}

        for c in clauses:
            new = {s: [lst[:] for lst in lists] for s, lists in combs.items()}
            for s, lists in combs.items():
                max_ops = (bin_capacity - s) // c
                for k in range(1, max_ops + 1):
                    new_sum = s + k * c
                    for comb in lists:
                        new.setdefault(new_sum, []).append(comb + [c] * k)
            combs = new
        return combs.get(bin_capacity, [])

    def binpacking_bestcase(
        self, bin_capacity: int, clauses: List[int]
    ) -> List[List[int]]:
        res = []
        clauses = sorted(clauses)
        q = deque()
        q.append((0, 0, []))

        while q:
            curr_sum, i, curr_combination = q.popleft()
            if curr_sum == bin_capacity:
                res.append(curr_combination)
                continue

            if i >= len(clauses):
                continue

            curr = clauses[i]
            max_ntimes = (bin_capacity - curr_sum) // curr
            for k in range(max_ntimes + 1):
                new_sum = curr_sum + k * curr
                if new_sum <= bin_capacity:
                    q.append((new_sum, i + 1, curr_combination + [curr] * k))

        return res
