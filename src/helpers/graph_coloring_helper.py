from abc import ABC, abstractmethod
import os
from src.helpers.dmaics_parser import parse_multi_instance_graph
from src.helpers.constants import RESULTS_FOLDER, CONFIGURATION_FILE_PATH
from typing import List, Tuple, Dict, Any, Optional
import json
import csv
import time
from src.helpers.project_selection_enum import ProjectSelection, SubProblemSelection


class GraphColoringAbstractClass(ABC):

    def __init__(self, 
                    cnf_file_input_path: str,
                    result_file_name:str = "graph_coloring_results",
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
        return parse_multi_instance_graph(self.cnf_file_input_path)
    
    def save_results(self, run_results: List[Any], sub_problem):
        # Write to CSV
        dir_name, file_name = os.path.split(self.cnf_file_input_path)
        file_name_only, ext = os.path.splitext(file_name)
        temp_result = os.path.join(self.results_folder_path, f"{sub_problem}_{file_name_only}_{self.result_file_name}.csv")
        with open(temp_result, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["instance_id", "n_vertices", "n_edges", "k",
                    "method", "colorable", "time_seconds", "coloring"])
            w.writerows(run_results)
        print(f"\nResults written to {temp_result}")
    
    @abstractmethod
    def coloring_backtracking(self, n_vertices: int, edges: List[Tuple[int]], k:int) -> Tuple[bool, Optional[List[int]]]:
        pass

    @abstractmethod
    def coloring_bruteforce(self, n_vertices: int, edges: List[Tuple[int]], k:int) -> Tuple[bool, Optional[List[int]]]:
        pass

    @abstractmethod
    def coloring_simple(self, n_vertices: int, edges: List[Tuple[int]], k:int) -> Tuple[bool, Optional[List[int]]]:
        pass

    @abstractmethod
    def coloring_bestcase(self, n_vertices: int, edges: List[Tuple[int]], k:int) -> Tuple[bool, Optional[List[int]]]:
        pass

    def run(self):
        results = []
        
        for instance_id, k, n_vertices, edges in self.solution_instances:

            if SubProblemSelection.brute_force in self.sub_problems:
                t0 = time.perf_counter()
                bt_ok, bt_assign = self.coloring_bruteforce(n_vertices, edges, k)
                bt_time = time.perf_counter() - t0
                results.append([instance_id, n_vertices, len(edges), k,
                        "BruteForce", "YES" if bt_ok else "NO",
                        f"{bt_time:.6f}", str(bt_assign)])
        
        if SubProblemSelection.brute_force in self.sub_problems:
            self.save_results(results, SubProblemSelection.brute_force.name)
            results = []

        for instance_id, k, n_vertices, edges in self.solution_instances:

            if SubProblemSelection.btracking in self.sub_problems:
                t0 = time.perf_counter()
                bt_ok, bt_assign = self.coloring_backtracking(n_vertices, edges, k)
                bt_time = time.perf_counter() - t0
                results.append([instance_id, n_vertices, len(edges), k,
                        "BackTracking", "YES" if bt_ok else "NO",
                        f"{bt_time:.6f}", str(bt_assign)])
        
        if SubProblemSelection.btracking in self.sub_problems:
            self.save_results(results, SubProblemSelection.btracking.name)
            results = []

        for instance_id, k, n_vertices, edges in self.solution_instances:

            if SubProblemSelection.simple in self.sub_problems:
                t0 = time.perf_counter()
                bt_ok, bt_assign = self.coloring_simple(n_vertices, edges, k)
                bt_time = time.perf_counter() - t0
                results.append([instance_id, n_vertices, len(edges), k,
                        "Simple", "YES" if bt_ok else "NO",
                        f"{bt_time:.6f}", str(bt_assign)])
        
        if SubProblemSelection.simple in self.sub_problems:
            self.save_results(results, SubProblemSelection.simple.name)
            results = []
        

        for instance_id, k, n_vertices, edges in self.solution_instances:

            if SubProblemSelection.best_case in self.sub_problems:
                t0 = time.perf_counter()
                bt_ok, bt_assign = self.coloring_bestcase(n_vertices, edges, k)
                bt_time = time.perf_counter() - t0
                results.append([instance_id, n_vertices, len(edges), k,
                        "BestCase", "YES" if bt_ok else "NO",
                        f"{bt_time:.6f}", str(bt_assign)])
        
        if SubProblemSelection.best_case in self.sub_problems:
            self.save_results(results, SubProblemSelection.best_case.name)
            results = []
