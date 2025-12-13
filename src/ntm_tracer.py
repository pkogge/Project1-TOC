from src.helpers.turing_machine import TuringMachineSimulator

# ==========================================
# PROGRAM 1: Nondeterministic TM
# ==========================================
class NTM_Tracer(TuringMachineSimulator):
    def run(self, input_string, max_depth):
        """
        Performs a Breadth-First Search (BFS) trace of the NTM.
        Ref: Section 4.1 "Trees as List of Lists"
        """
        print(f"Tracing NTM: {self.machine_name} on input '{input_string}'")

        self.blank_symbol = '_'

        # Initial Configuration: ["", start_state, input_string]
        initial_config = [[], self.start_state, list(input_string)]

        # The tree is a list of lists of configurations
        tree = [[initial_config]]

        depth = 0
        accepted = False
        
        non_leaf_count = 0 

        while depth < max_depth and not accepted:
            current_level = tree[-1]
            next_level = []
            all_rejected = True

            # 1. Iterate through every config in current_level.
            if depth == 0:
                self.simulated_transitions = 0
                print("[", end="") 

            display_level = []
            for c in current_level:
                l_str = "".join(c[0]) if c[0] else ""
                r_str = "".join(c[2]) if c[2] else ""
                display_level.append([l_str, c[1], r_str])
            
            if depth > 0:
                print(",")
            print(f"{display_level}", end="")

            for config in current_level:
                left, state, right = config[:3]

            # 2. Check if config is Accept (Stop and print success)
                if state == self.accept_state:
                    print("]")
                    print(f'String accepted in {depth}')
                    print(f'Total transitions simulated: {self.simulated_transitions}')
                    
                    if non_leaf_count > 0:
                        score = self.simulated_transitions / non_leaf_count
                    else:
                        score = 1.0 # Default if no branching occurred
                    print(f'Degree of Nondeterminism: {score:.2f}')

                    path = []
                    curr_node = config
                    while curr_node:
                        p_left, p_state, p_right = curr_node[:3]
                        
                        left_str = "".join(p_left) if p_left else ""
                        right_str = "".join(p_right) if p_right else ""
                        
                        path.append(f'["{left_str}", "{p_state}", "{right_str}"]')
                        
                        curr_node = curr_node[3] if len(curr_node) > 3 else None

                    for step in reversed(path):
                        print(step)

                    accepted = True
                    break
            
            # 3. Check if config is Reject (Stop this branch only)
                if state == self.reject_state:
                    continue
            
            # 4. If not Accept/Reject, find valid transitions in self.transitions.
                curr = (right[0],) if right else (self.blank_symbol,)
                valid = False

                transition_found = False

                for src, tr_list in self.transitions.items():
                    if state == self.reject_state:
                        continue

                    if src != state:
                        continue

                    for t in tr_list:
                        
                        read_ch = t['read']
                        dst = t['next']
                        write_ch = t['write']
                        direction = t['move'][0]

                        if read_ch != curr:
                            continue

                        transition_found = True

                        valid = True
                        all_rejected = False
                        self.simulated_transitions += 1

                        new_left = left.copy()
                        new_right = right.copy()

                        if new_right:
                            new_right[0] = write_ch[0]
                        else:
                            new_right = [write_ch[0]]

                        if direction == 'R':
                            if new_right:
                                new_left.append(new_right[0])
                                new_right = new_right[1:] if len(new_right) > 1 else []
                            else:
                                new_left.append(self.blank_symbol)
                                new_right = []

                        elif direction == 'L':
                            if new_left:
                                new_right.insert(0, new_left.pop())
                            else:
                                new_right.insert(0, self.blank_symbol)

                        next_config = (new_left, dst, new_right, config)
                        next_level.append(next_config)

                    if not transition_found:
                        reject_node = [left, self.reject_state, right]
                        next_level.append(reject_node)
                        self.simulated_transitions += 1
                        valid = True

                # 5. Track Non-Leaves
                if valid:
                    non_leaf_count += 1

            if accepted:
                return
            
            if not next_level and all_rejected:
                print("]")
                print(f"String rejected in {depth}")
                print(f"Total transitions simulated: {self.simulated_transitions}")
                
                if non_leaf_count > 0:
                    score = self.simulated_transitions / non_leaf_count
                else:
                    score = 1.0
                print(f'Degree of Nondeterminism: {score:.2f}')
                break

            tree.append(next_level)
            depth += 1

        if depth >= max_depth:
            print("]")
            print(f"Execution stopped after {max_depth} steps.")
    
    def print_trace_path(self, final_node):
        pass