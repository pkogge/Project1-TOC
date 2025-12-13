import unittest
import os
import csv
from src.ntm_tracer import NTM_Tracer 
from src.helpers.turing_machine import TuringMachineSimulator 

# --- Define a simple NTM for testing ---
SIMPLE_NTM_CONFIG = {
    "name": "Single_1_Acceptor",
    "states": ["q0", "q1", "q_accept", "q_reject"],
    "alphabet": ["0", "1"],
    "tape_alphabet": ["0", "1", "_"],
    "start_state": "q0",
    "accept_state": "q_accept",
    "reject_state": "q_reject",
    "transitions": [
        {"from": "q0", "read": "0", "to": "q0", "write": "0", "move": "R"},
        {"from": "q0", "read": "1", "to": "q0", "write": "1", "move": "R"},
        
        {"from": "q0", "read": "0", "to": "q1", "write": "0", "move": "R"},
        {"from": "q0", "read": "1", "to": "q1", "write": "1", "move": "R"},
        
        {"from": "q1", "read": "0", "to": "q1", "write": "0", "move": "R"},
        {"from": "q1", "read": "1", "to": "q_accept", "write": "1", "move": "S"},
        {"from": "q1", "read": "_", "to": "q_reject", "write": "_", "move": "S"},
    ]
}


class TestNTMTracer(unittest.TestCase):
    
    # Define a temporary file name
    CONFIG_FILENAME = "temp_test_machine.csv"
    
    def _write_config_to_file(self, config):
        """Helper to write the dict config to a file."""
        with open(self.CONFIG_FILENAME, 'w', newline='') as f:
            writer = csv.writer(f)
            
            # 1. Header (Name, Tapes)
            writer.writerow([config["name"], 1]) 
            
            # 2. States, Alphabet, Gamma, Start, Accept, Reject
            writer.writerow(config["states"])
            writer.writerow(config["alphabet"])
            writer.writerow(config["tape_alphabet"])
            writer.writerow([config["start_state"]])
            writer.writerow([config["accept_state"]])
            writer.writerow([config["reject_state"]])

            # 3. Transitions (State, Read, Next, Write, Move)
            for t in config["transitions"]:
                writer.writerow([t["from"], t["read"], t["to"], t["write"], t["move"]])

    def setUp(self):
        """Write config to file and instantiate simulator using the filename."""
        self._write_config_to_file(SIMPLE_NTM_CONFIG)
        # PASS FILENAME (STRING) HERE, NOT DICT
        self.ntm = NTM_Tracer(self.CONFIG_FILENAME) 

    def tearDown(self):
        """Clean up the temporary file."""
        if os.path.exists(self.CONFIG_FILENAME):
            os.remove(self.CONFIG_FILENAME)

    def test_acceptance_path(self):
        """Test a string that should be accepted by the NTM."""
        input_string = "0010"
        
        print(f"\n--- Running Acceptance Test: {input_string} ---")
        self.ntm.run(input_string, max_depth=10)

    def test_rejection_path(self):
        """Test a string that should be rejected by the NTM."""
        input_string = "0000"
        
        print(f"\n--- Running Rejection Test: {input_string} ---")
        self.ntm.run(input_string, max_depth=10)

    def test_max_depth_limit(self):
        """Test that the run stops if max_depth is reached."""
        input_string = "0000"
        
        print(f"\n--- Running Max Depth Limit Test: {input_string} ---")
        self.ntm.run(input_string, max_depth=2) 

if __name__ == '__main__':
    unittest.main()
