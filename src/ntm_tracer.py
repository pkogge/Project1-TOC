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
        initial_config = ["", self.start_state, input_string if input_string else "_", -1, -1]

        # The tree is a list of lists of configurations
        tree = [[initial_config]]

        depth = 0
        accepted = False
        accepted_node = None
        num_transitions = 0
        rejection_depth = 0


        while depth < max_depth and not accepted:
            current_level = tree[-1]
            next_level = []
            all_rejected = True

            # TODO: STUDENT IMPLEMENTATION NEEDED
            # 1. Iterate through every config in current_level.
            for i, config in enumerate(current_level):
                left, state, right, _ , _ = config

            # 2. Check if config is Accept (Stop and print success) [cite: 179]
                if state == self.accept_state:
                    accepted = True
                    accepted_node = (depth, i)
                    break

            # 3. Check if config is Reject (Stop this branch only) [cite: 181]
                if state == self.reject_state:
                    rejection_depth = max(rejection_depth, depth)
                    continue

                #Not rejected since the branch isnt in either terminal state        
                all_rejected = False

                #Get current tape character
                if right and right[0] != "_":
                    current_char = right[0]
                else:
                    current_char = "_"
            # 4. If not Accept/Reject, find valid transitions in self.transitions.
                valid_transitions = []
                transition_num = 0

                if state in self.transitions:
                    for transition_dict in self.transitions[state]:
                        if transition_dict['read'][0] == current_char:
                            transition = (
                                state,
                                transition_dict['read'][0],
                                transition_dict['next'],
                                transition_dict['write'][0],
                                transition_dict['move'][0]
                            )
                            valid_transitions.append((transition, transition_num))
                            transition_num += 1

                if not valid_transitions:
                    rejection_depth = max(rejection_depth, depth)
                    num_transitions += 1 
                    continue
                

                if not valid_transitions:
                    rejection_depth = max(rejection_depth, depth)
                    continue           

            # 5. If no explicit transition exists, treat as implicit Reject.
                if not valid_transitions:
                    rejection_depth = max(rejection_depth, depth)
                    continue

            # 6. Generate children configurations and append to next_level[cite: 148].
                for transition, transition_num in valid_transitions:
                    _, _, next_state, write_char, direction = transition

                    num_transitions += 1

                    #New config
                    new_left = left
                    new_right = right

                    #Write character to tape
                    if right:
                        new_right = write_char + right[1:]
                    else: 
                        new_right = write_char

                    #Move head
                    if direction == 'R':
                        #Moving right - add current char to left and update the right
                        new_left = left + new_right[0]
                        new_right = new_right[1:]
                        if not new_right:
                            new_right = "_"
                    elif direction == 'L':
                        #Moving left - add last char of left to front of right and update the left
                        if new_left:
                            new_right = new_left[-1] + new_right
                            new_left = new_left[:-1]
                        else:
                            new_right = "_"

                    new_config = (new_left, next_state, new_right, i, transition_num)
                    next_level.append(new_config)

            if accepted:
                break


            # Placeholder for logic:
            if not next_level and all_rejected:
                # TODO: Handle "String rejected" output [cite: 258]
                break

            tree.append(next_level)
            depth += 1
        
        nondeterminism = self.calculate_nondeterminism(tree, num_transitions=num_transitions)

        print()
        print(f"Machine: {self.machine_name}")
        print(f"Input string: '{input_string}'")
        print(f"Tree depth: {depth}")
        print(f"Total transitions simulated: {num_transitions}")
        print(f"Average nondeterminism: {nondeterminism:.3f}")
        print()

        if accepted:
            print(f"String accepted in {depth} steps")
            print()
            self.print_trace_path(tree, accepted_node)
        elif depth >= max_depth:
            print(f"Execution stopped after {max_depth} steps.")  # [cite: 259]  
        else:
            print(f"String rejected in {rejection_depth} steps")

    def calculate_nondeterminism(self, tree, num_transitions):
        total_nonleaves = 0

    
        for i in range(len(tree) - 1):
            level = tree[i]


            for config in level:
                _, state, _, _, _ = config
                if state != self.accept_state and state != self.reject_state:
                    total_nonleaves += 1
        

        if total_nonleaves == 0:
            return 1.0
        
        return num_transitions / total_nonleaves

    def print_trace_path(self, tree, final_node):
        """
        Backtrack and print the path from root to the accepting node.
        Ref: Section 4.2 [cite: 165]
        """
        depth, idx = final_node
        path = []

        current_depth = depth
        current_idx = idx

        while current_depth >= 0:
            config = tree[current_depth][current_idx]
            path.append((current_depth, config))

            _, _, _, parent_idx, _ = config
            if parent_idx == -1:
                break

            current_depth -= 1
            current_idx = parent_idx
        
        path.reverse()

        print("Accepting path configurations:")
        for level, config in path:
            left, state, right, _, _ = config
            print(f"Level {level}:")

            level_configs = tree[level]
            for c in level_configs:
                c_left, c_state, c_right, _, _ = c
                marker = " <-- accepting path" if c == config else ""
                print(f"  {c_left} {c_state} {c_right}{marker}")

