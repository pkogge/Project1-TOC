from src.helpers.turing_machine import TuringMachineSimulator, BLANK, WILDCARD

# ==========================================
# PROGRAM 1: Nondeterministic TM
# ==========================================
class NTM_Tracer(TuringMachineSimulator):
    def __init__(self, filename):
        super().__init__(filename)

    def run(self, input_string, max_depth):
        """
        Performs BFS trace and backtracks the winning path.
        Ref: Section 4.1 "Trees as List of Lists" [cite: 144]
        Ref: Section 4.2 "Tracing Execution"
        """
        print(f"\nTracing NTM: {self.machine_name} on input '{input_string}'")

        # Config: [left, state, right, parent_index, transition_info]
        # We need parent_index to backtrack. 
        # root has parent_index -1
        initial_config = ["", self.start_state, input_string, -1, "Start"]
        
        # Tree is list of lists.
        tree = [[initial_config]]

        depth = 0
        total_transitions = 0
        total_non_leaves = 0
        rejected_branches = 0

        while depth < max_depth:
            current_level = tree[-1]
            next_level = []
            
            print(f"Level {depth}: {len(current_level)} configurations")
            
            # Check for Acceptance
            for i, config in enumerate(current_level):
                left, state, right, _, _ = config
                
                # Print config for the trace log
                display_right = right if right else "_"
                #print(f"  {left} {state} {display_right}")

                if state == self.accept_state:
                    self.print_final_stats(True, depth, total_transitions, total_non_leaves, rejected_branches)
                    # Perform Backtrace
                    self.print_winning_path(tree, depth, i)
                    return

            # Make Next Level
            for i, config in enumerate(current_level):
                left, state, right, _, _ = config

                if state == self.reject_state:
                    rejected_branches += 1
                    continue

                head_char = right[0] if len(right) > 0 else "_"
                valid_moves = self.get_transitions(state, (head_char,))

                if not valid_moves:
                    rejected_branches += 1
                    continue

                total_non_leaves += 1

                for move in valid_moves:
                    next_state = move['next']
                    write_char = move['write'][0]
                    direction = move['move'][0]
                    
                    if write_char == WILDCARD: write_char = head_char

                    new_left = left
                    new_right = right
                    
                    if direction == 'R':
                        new_left = left + write_char
                        new_right = right[1:] if len(right) > 1 else ""
                    elif direction == 'L':
                        if len(left) > 0:
                            new_right = left[-1] + write_char + (right[1:] if len(right) > 1 else "")
                            new_left = left[:-1]
                        else:
                            new_right = "_" + write_char + (right[1:] if len(right) > 1 else "")
                    elif direction == 'S':
                        new_right = write_char + (right[1:] if len(right) > 1 else "")

                    # Store parent index 'i' to link back to current_level[i]
                    # formatting the transition info for the backtrace
                    trans_info = f"({state}, {head_char}) -> ({next_state}, {write_char}, {direction})"
                    next_level.append([new_left, next_state, new_right, i, trans_info])
                    total_transitions += 1

            if not next_level:
                self.print_final_stats(False, depth, total_transitions, total_non_leaves, rejected_branches)
                return

            tree.append(next_level)
            depth += 1

        print(f"Execution stopped after {max_depth} steps.")
        self.print_final_stats(False, depth, total_transitions, total_non_leaves, rejected_branches)

    def print_winning_path(self, tree, depth, final_index):
        """
        Backtracks from the accepting configuration to the root.
        Ref: Section 4.2 "go backwards from any configuration... to the root" [cite: 170]
        """
        
        print("\nTransistion Log:")
       
        
        path = []
        curr_index = final_index
        
        # Walk backwards from current depth down to 0
        for d in range(depth, -1, -1):
            config = tree[d][curr_index]
            path.append(config)
            curr_index = config[3] # Parent index

        # Print in correct order (Root -> Accept)
        path.reverse()
        
        for step_num, config in enumerate(path):
            left, state, right, _, trans = config
            tape = (left + "[" + state + "]" + (right if right else "_"))
            if step_num == 0:
                print(f"Start: {tape}")
            else:
                print(f"Step {step_num}: {tape}  via {trans}")
            
        print("\n")
        
    def print_final_stats(self, accepted, depth, total_trans, total_non_leaves, rejected_count):
       
        print(f"\nResult: {accepted}")
        status = "accepted" if accepted else "rejected"
        print(f"String {status} in {depth} steps.") 
        
        if accepted:
            print(f"Accepted Configurations: 1")
        else:
            print(f"Accepted Configurations: 0")
        
        print(f"Rejected Configurations: {rejected_count}")
        print(f"Total transitions simulated: {total_trans}")

        # Nondeterminism Calculation 
        if total_non_leaves > 0:
            degree = total_trans / total_non_leaves
            print(f"Degree of Nondeterminism: {degree:.2f} ")
        else:
            print("Degree of Nondeterminism: 1.00 (Deterministic)\n")
    
        
    def print_trace_path(self, final_node):
        pass