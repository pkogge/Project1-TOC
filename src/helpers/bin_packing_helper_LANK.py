from abc import ABC, abstractmethod
import os
from src.helpers.dmaics_parser import parse_multi_instance_bin_packing
from src.helpers.constants import RESULTS_FOLDER, CONFIGURATION_FILE_PATH
from typing import List, Tuple, Dict, Any
import json
import csv
import time
from src.helpers.project_selection_enum import ProjectSelection, SubProblemSelection


class BinPackingAbstractClass(ABC):

    def __init__(self, 
                    cnf_file_input_path: str,
                    result_file_name:str = "sat_solver_results",
                    results_folder_path: str = RESULTS_FOLDER):
        self.cnf_file_input_path = cnf_file_input_path
        self.results_folder_path = results_folder_path
        self.result_file_name = result_file_name
        self.config_path = CONFIGURATION_FILE_PATH
        self.solution_instances = self.parse_input_file()
        print(f"Parsed {len(self.solution_instances)} instances from {self.cnf_file_input_path}")
        self.sub_problems = self.set_config()

    def set_config(self):
        if not os.path.exists(self.config_path):
            raise Exception("Please make sure the configuration file exists!!!")
        with open(self.config_path, mode = 'r' , encoding= 'utf-8') as conf_buffer:
            data = json.load(conf_buffer)
        data = data["Project Configuration"]
        selection = data["Selection"]
        sub_problem = data["Sub Problem"]
        sub_probs = []
        for sub_prob in sub_problem:
            if sub_prob["value"] == SubProblemSelection.brute_force.value:
                sub_probs.append(SubProblemSelection.brute_force)
            elif sub_prob["value"] == SubProblemSelection.btracking.value:
                sub_probs.append(SubProblemSelection.btracking)
            elif sub_prob["value"] == SubProblemSelection.simple.value:
                sub_probs.append(SubProblemSelection.simple)
            elif sub_prob["value"] == SubProblemSelection.best_case.value:
                sub_probs.append(SubProblemSelection.best_case)
        return sub_probs
        
    def parse_input_file(self):
        return parse_multi_instance_bin_packing(self.cnf_file_input_path)
    
    def save_results(self, run_results: List[Any], sub_problem):
        # Write to CSV
        dir_name, file_name = os.path.split(self.cnf_file_input_path)
        file_name_only, ext = os.path.splitext(file_name)
        temp_result = os.path.join(self.results_folder_path, f"{sub_problem}_{file_name_only}_{self.result_file_name}.csv")
        with open(temp_result, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["instance_id", "bin_capacity", "bins_array", "method", "time_taken"])
            w.writerows(run_results)
        print(f"\nResults written to {temp_result}")
    
    def binpacking_backtracing(self, bin_capacity:int, clauses:List[int]) -> List[List[int]]:
        """
        Backtracking approach to find all subsets that sum to bin_capacity.
        """
        results = []
        def backtrack(start: int, current_sum: int, current_bin: List[int]):
            if current_sum == bin_capacity:
                results.append(sorted(current_bin[:]))
                return
            
            if current_sum > bin_capacity:
                return
            
            for i in range(start, len(clauses)):
                item = clauses[i]
                if current_sum + item <= bin_capacity:
                    current_bin.append(item)
                    backtrack(i + 1, current_sum + item, current_bin)
                    current_bin.pop()
        
        backtrack(0, 0, [])
        return results

    @abstractmethod
    def binpacking_bruteforce(self, bin_capacity:int, clauses:List[int]) -> List[List[int]]:
        pass

    @abstractmethod
    def binpacking_simple(self, bin_capacity:int, clauses:List[int]) -> List[List[int]]:
        pass

    @abstractmethod
    def binpacking_bestcase(self, bin_capacity:int, clauses:List[int]) -> List[List[int]]:
        pass

    def run(self):
        results = []
        
        for inst_id, clause in enumerate(self.solution_instances):
            bin_capacity = clause[0]
            clauses = clause[1:]
            if SubProblemSelection.brute_force in self.sub_problems:
                t0 = time.perf_counter()
                temp_results = self.binpacking_bruteforce(bin_capacity, clauses)
                bt_time = time.perf_counter() - t0
                for result in temp_results:
                    results.append([inst_id, bin_capacity, result,"BruteForce", bt_time])
        
        if SubProblemSelection.brute_force in self.sub_problems:
            self.save_results(results, SubProblemSelection.brute_force.name)
            results = []

        for inst_id, clause in enumerate(self.solution_instances):
            bin_capacity = clause[0]
            clauses = clause[1:]
            if SubProblemSelection.btracking in self.sub_problems:
                t0 = time.perf_counter()
                temp_results = self.binpacking_backtracing(bin_capacity, clauses)
                bt_time = time.perf_counter() - t0
                for result in temp_results:
                    results.append([inst_id, bin_capacity, result,"BackTracking", bt_time])
        
        if SubProblemSelection.btracking in self.sub_problems:
            self.save_results(results, SubProblemSelection.btracking.name)
            results = []

        for inst_id, clause in enumerate(self.solution_instances):
            bin_capacity = clause[0]
            clauses = clause[1:]
            if SubProblemSelection.simple in self.sub_problems:
                t0 = time.perf_counter()
                temp_results = self.binpacking_simple(bin_capacity, clauses)
                bt_time = time.perf_counter() - t0
                for result in temp_results:
                    results.append([inst_id, bin_capacity, result,"Simple", bt_time])

        
        if SubProblemSelection.simple in self.sub_problems:
            self.save_results(results, SubProblemSelection.simple.name)
            results = []
        

        for inst_id, clause in enumerate(self.solution_instances):
            bin_capacity = clause[0]
            clauses = clause[1:]
            if SubProblemSelection.best_case in self.sub_problems:
                t0 = time.perf_counter()
                temp_results = self.binpacking_bestcase(bin_capacity, clauses)
                bt_time = time.perf_counter() - t0
                for result in temp_results:
                    results.append([inst_id, bin_capacity, result,"BestCase", bt_time])
        
        if SubProblemSelection.best_case in self.sub_problems:
            self.save_results(results, SubProblemSelection.best_case.name)
            results = []



        


    
    


    