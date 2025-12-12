from src.helpers.turing_machine import TuringMachineSimulator


# ==========================================
# PROGRAM 1: Nondeterministic TM [cite: 137]
# ==========================================
class NTM_Tracer(TuringMachineSimulator):
    def run(self, input_string, max_depth):
        """
        Performs a Breadth-First Search (BFS) trace of the NTM.
        Ref: Section 4.1 "Trees as List of Lists" [cite: 146]
        """
        print(f"Tracing NTM: {self.machine_name} on input '{input_string}'")

        # Initial Configuration: ["", start_state, input_string]
        # Note: Represent configuration as triples (left, state, right) [cite: 156]
        initial_config = ["", self.start_state, input_string]

        # The tree is a list of lists of configurations
        tree = [[initial_config]]

        depth = 0
        accepted = False
        total_transitions = 0

        while depth < max_depth and not accepted:
            current_level = tree[-1]
            next_level = []
            all_rejected = True
            
            print(f"level {depth}") #print the current levl
            for config in current_level: #format the ledt,state,head_char, rest_of_right
                left, state, right = config
                head_char = right[0] if right else "_"
                rest_right = right[1:] if right else ""
                print(f"{left} {state} {head_char}{rest_right}")
                
                
            for config in current_level: #Iterate through every config in current_level.
                left, state, right = config
                
                
                if state == self.accept_state: #Check if config is Accept
                    print(f"String accepted in {depth}")
                    accepted = True
                    return

                 
                if state == self.reject_state: #Check if config is Reject
                    continue 

                all_rejected = False # Found at least one non-reject state to process
                
                # Determine character under head (treat empty right as blank '_')
                head_char = right[0] if len(right) > 0 else "_"
                
                # If not Accept/Reject, find valid transitions in self.transitions.
                # Key is (current_state, read_char). handle wildcard if necessary, but we want standard lookup first.
                transitions = self.transitions.get((state, head_char), [])
                
                
                for trans in transitions: #If no explicit transition exists, treat as implicit Reject.
                    next_state = trans['next_state']
                    write_char = trans['write_char']
                    direction = trans['direction']
                    
                    #Generate children and append to next_level
                    new_left = left
                    new_right = right
                    
                    # Construct tape after writing
                    # Current head position is replaced by write_char
                    # Tape logic: left + write_char + (right[1:] or "")
                    
                    if direction == 'R':
                        new_left = left + write_char
                        new_right = right[1:] if len(right) > 1 else ""
                        # If we moved right into "void", it becomes empty string.
                    
                    elif direction == 'L':
                        if len(left) > 0:
                            # Move char from end of left to front of right
                            char_from_left = left[-1]
                            new_left = left[:-1]
                            new_right = char_from_left + write_char + (right[1:] if len(right) > 1 else "")
                        else:
                            # test caaese: moving left at start of tape. 
                            # Usually stays or crashes. assuming standard stay-at-edge or blank tape left behavior.
                            # For simplicity/safety with standard strings:
                            new_right = "_" + write_char + (right[1:] if len(right) > 1 else "")
                                                        
                    # Add to next level
                    next_level.append([new_left, next_state, new_right])
                    total_transitions += 1
                    
            # TODO: STUDENT IMPLEMENTATION NEEDED
            # 1. Iterate through every config in current_level.
            # 2. Check if config is Accept (Stop and print success) [cite: 179]
            # 3. Check if config is Reject (Stop this branch only) [cite: 181]
            # 4. If not Accept/Reject, find valid transitions in self.transitions.
            # 5. If no explicit transition exists, treat as implicit Reject.
            # 6. Generate children configurations and append to next_level[cite: 148].


            # Placeholder for logic:
            if not next_level and all_rejected:
                # TODO: Handle "String rejected" output [cite: 258]
                break

            tree.append(next_level)
            depth += 1

        if depth >= max_depth:
            print(f"Execution stopped after {max_depth} steps.")  # [cite: 259]

    def print_trace_path(self, final_node):
        """
        Backtrack and print the path from root to the accepting node.
        Ref: Section 4.2 [cite: 165]
        """
        pass
