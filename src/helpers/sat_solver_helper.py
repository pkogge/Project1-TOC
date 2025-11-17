from abc import ABC, abstractmethod
import os
from src.helpers.dmaics_parser import parse_multi_instance_dimacs
from src.helpers.constants import RESULTS_FOLDER, CONFIGURATION_FILE_PATH
from typing import List, Tuple, Dict, Any
import json
import csv
import time
from src.helpers.project_selection_enum import ProjectSelection, SubProblemSelection


class SatSolverAbstractClass(ABC):

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
        return parse_multi_instance_dimacs(self.cnf_file_input_path)
    
    def save_results(self, run_results: List[Any], sub_problem):
        # Write to CSV
        dir_name, file_name = os.path.split(self.cnf_file_input_path)
        file_name_only, ext = os.path.splitext(file_name)
        temp_result = os.path.join(self.results_folder_path, f"output_{sub_problem}_{file_name_only}_{self.result_file_name}_Logan_:).csv") #modified this line to do correct output format
        with open(temp_result, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["instance_id", "n_vars", "n_clauses", "method",
                        "satisfiable", "time_seconds", "solution"])
            w.writerows(run_results)
        print(f"\nResults written to {temp_result}")
    
    @abstractmethod
    def sat_backtracking(self, n_vars:int, clauses:List[List[int]]) -> Tuple[bool, Dict[int, bool]]:
        pass

    @abstractmethod
    def sat_bruteforce(self, n_vars:int, clauses:List[List[int]]) -> Tuple[bool, Dict[int, bool]]:
        pass

    @abstractmethod
    def sat_simple(self, n_vars:int, clauses:List[List[int]]) -> Tuple[bool, Dict[int, bool]]:
        pass

    @abstractmethod
    def sat_bestcase(self, n_vars:int, clauses:List[List[int]]) -> Tuple[bool, Dict[int, bool]]:
        pass

    def run(self):
        results = []
        
        for inst_id, n_vars, clauses in self.solution_instances:

            if SubProblemSelection.brute_force in self.sub_problems:
                t0 = time.perf_counter()
                bt_ok, bt_assign = self.sat_bruteforce(n_vars, clauses)
                bt_time = time.perf_counter() - t0
                results.append([inst_id, n_vars, len(clauses),
                                 "BruteForce",
                            "S" if bt_ok else "U", 
                            bt_time,
                            str(bt_assign)])
        
        if SubProblemSelection.brute_force in self.sub_problems:
            self.save_results(results, SubProblemSelection.brute_force.name)
            results = []

        for inst_id, n_vars, clauses in self.solution_instances:

            if SubProblemSelection.btracking in self.sub_problems:
                t0 = time.perf_counter()
                bt_ok, bt_assign = self.sat_backtracking(n_vars, clauses)
                bt_time = time.perf_counter() - t0
                results.append([inst_id, n_vars, len(clauses),
                            "BackTracking",
                            "S" if bt_ok else "U", 
                            bt_time,
                            str(bt_assign)])
        
        if SubProblemSelection.btracking in self.sub_problems:
            self.save_results(results, SubProblemSelection.btracking.name)
            results = []

        for inst_id, n_vars, clauses in self.solution_instances:

            if SubProblemSelection.simple in self.sub_problems:
                t0 = time.perf_counter()
                bt_ok, bt_assign = self.sat_simple(n_vars, clauses)
                bt_time = time.perf_counter() - t0
                results.append([inst_id, n_vars, len(clauses), 
                                "Simple",
                            "S" if bt_ok else "U", 
                            bt_time, 
                            str(bt_assign)])
        
        if SubProblemSelection.simple in self.sub_problems:
            self.save_results(results, SubProblemSelection.simple.name)
            results = []
        

        for inst_id, n_vars, clauses in self.solution_instances:

            if SubProblemSelection.best_case in self.sub_problems:
                t0 = time.perf_counter()
                bt_ok, bt_assign = self.sat_bestcase(n_vars, clauses)
                bt_time = time.perf_counter() - t0
                results.append([inst_id, n_vars, len(clauses), 
                                "BestCase",
                            "S" if bt_ok else "U", 
                            bt_time, 
                            str(bt_assign)])
        
        if SubProblemSelection.best_case in self.sub_problems:
            self.save_results(results, SubProblemSelection.best_case.name)
            results = []



        


    
    


    