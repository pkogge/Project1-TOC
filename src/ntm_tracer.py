import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'helpers'))

from turing_machine import TuringMachineSimulator, BLANK, WILDCARD, DIR_L, DIR_R, DIR_S
from argument_input import parse_inputs

# ==========================================
# PROGRAM 1: Nondeterministic TM [cite: 137]
# ==========================================
class NTM_Tracer(TuringMachineSimulator):
    def run(self, input_string, max_depth):
        """
        Performs a Breadth-First Search (BFS) trace of the NTM.
        Ref: Section 4.1 "Trees as List of Lists" [cite: 146]
        """
        print(f"{self.machine_name}")
        print(f"Input: {input_string}")
        
        # Initial Configuration: ["", start_state, input_string]
        # Note: Represent configuration as triples (left, state, right) [cite: 156]
        # Store with parent reference for path reconstruction
        initial_config = ("", self.start_state, input_string if input_string else BLANK, None, -1)
        
        # The tree is a list of lists of configurations
        # Each config is (left, state, right, parent_index, transition_num)
        tree = [[initial_config]]
        depth = 0
        accepted = False
        accepting_config = None
        total_transitions = 0
        
        while depth < max_depth and not accepted:
            current_level = tree[-1]
            next_level = []
            all_rejected = True
            
            # 1. Iterate through every config in current_level.
            for config_idx, config_data in enumerate(current_level):
                left, state, right, parent_idx, trans_num = config_data
                
                # 2. Check if config is Accept (Stop and print success) [cite: 179]
                if state == self.accept_state:
                    accepting_config = (depth, config_idx)
                    accepted = True
                    break
                
                # 3. Check if config is Reject (Stop this branch only) [cite: 181]
                if state == self.reject_state:
                    continue
                
                # Get the current symbol under the tape head
                current_symbol = right[0] if right else BLANK
                
                # 4. If not Accept/Reject, find valid transitions in self.transitions.
                valid_transitions = self.get_transitions(state, (current_symbol,))
                
                # 5. If no explicit transition exists, treat as implicit Reject.
                if not valid_transitions:
                    continue
                
                # If we found transitions, this branch is not rejected
                all_rejected = False
                
                # 6. Generate children configurations and append to next_level[cite: 148].
                for trans_idx, transition in enumerate(valid_transitions):
                    new_state = transition['next']
                    write_symbol = transition['write'][0]
                    direction = transition['move'][0]
                    
                    new_config = self.apply_transition(left, right, write_symbol, direction)
                    if new_config:
                        new_left, new_right = new_config
                        next_level.append((new_left, new_state, new_right, config_idx, trans_idx))
                        total_transitions += 1
            
            if accepted:
                break
            
            # Handle "String rejected" output [cite: 258]
            if not next_level and all_rejected:
                print(f"Depth: {depth}")
                print(f"Total transitions: {total_transitions}")
                print(f"String rejected in {depth} steps")
                return
            
            tree.append(next_level)
            depth += 1
        
        if depth >= max_depth and not accepted:
            print(f"Depth: {depth}")
            print(f"Total transitions: {total_transitions}")
            print(f"Execution stopped after {max_depth} steps.")  # [cite: 259]
            return
        
        # Print acceptance info
        accept_depth, accept_idx = accepting_config
        print(f"Depth: {accept_depth}")
        print(f"Total transitions: {total_transitions}")
        print(f"String accepted in {accept_depth} steps")
        
        # Print the accepting path
        self.print_trace_path(tree, accept_depth, accept_idx)
    
    def apply_transition(self, left, right, write_symbol, direction):
        """
        Apply a single transition and return the new configuration.
        Returns None if the transition is invalid.
        """
        # Handle empty right tape
        if not right:
            right = BLANK
        
        # Write the symbol
        if write_symbol == WILDCARD:
            actual_write = right[0] if right else BLANK
        else:
            actual_write = write_symbol
        
        # Start with writing the symbol to current position
        if len(right) > 1:
            new_right = actual_write + right[1:]
        else:
            new_right = actual_write
        
        # Move the head
        if direction == DIR_R:
            # Move right
            new_left = left + new_right[0]
            new_right = new_right[1:] if len(new_right) > 1 else ""
        elif direction == DIR_L:
            # Move left
            if not left:
                # At leftmost position - tape extends infinitely left with blanks
                new_left = ""
                new_right = BLANK + new_right
            else:
                new_right = left[-1] + new_right
                new_left = left[:-1]
        else:  # DIR_S - Stay
            new_left = left
        
        return (new_left, new_right)
    
    def print_trace_path(self, tree, accept_depth, accept_idx):
        """
        Backtrack and print the path from root to the accepting node.
        Ref: Section 4.2 [cite: 165]
        """
        # Build path by backtracking using parent references
        path = []
        current_depth = accept_depth
        current_idx = accept_idx
        
        while current_depth >= 0:
            config_data = tree[current_depth][current_idx]
            left, state, right, parent_idx, trans_num = config_data
            path.append((left, state, right, current_depth))
            
            if current_depth == 0:
                break
            current_idx = parent_idx
            current_depth -= 1
        
        # Reverse to get root-to-accept order
        path.reverse()
        
        print()
        for left, state, right, level in path:
            # Format: left[state]right
            config_str = left + "[" + state + "]" + right
            print(f"Level {level}: {config_str}")


# ==========================================
# MAIN EXECUTION
# ==========================================
if __name__ == "__main__":
    args = parse_inputs()
    
    # Run the NTM tracer
    ntm = NTM_Tracer(args.file)
    ntm.run(args.input_string, args.max_depth)
