from src.helpers.turing_machine import TuringMachineSimulator

# ==========================================
# CONSTANTS
# ==========================================
BLANK = "_"      # [cite: 231]
WILDCARD = "*"   # 
DIR_L = "L"
DIR_R = "R"
DIR_S = "S"      # [cite: 273]

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
        # New configuration format: [left, state, right, parent_index, trans_id]
        init_right = input_string if input_string else BLANK
        initial_config = ["", self.start_state, init_right, -1, -1]
        tree = [[initial_config]]

        depth = 0
        total_transitions = 0

        expanded_configs = 0
        generated_configs = 0

        accept_level = None
        accept_index = None

        while depth < max_depth:
            current_level = tree[-1]
            next_level = []
            all_rejected = True

            # TODO: STUDENT IMPLEMENTATION NEEDED
            # 1. Iterate through every config in current_level.
            # 2. Check if config is Accept (Stop and print success) [cite: 179]
            # 3. Check if config is Reject (Stop this branch only) [cite: 181]
            # 4. If not Accept/Reject, find valid transitions in self.transitions.
            # 5. If no explicit transition exists, treat as implicit Reject.
            # 6. Generate children configurations and append to next_level[cite: 148].
            for parent_index, cfg in enumerate(current_level):
                left, state, right, _, _ = cfg

                # Accept state reached --> stop execution
                if state == self.accept_state:
                    accept_level = depth
                    accept_index = parent_index
                    break

                # Reject state reached --> stop simulation on this branch
                if state == self.reject_state:
                    continue

                all_rejected = False
                expanded_configs += 1

                # Get head symbol and rest of string
                if right:
                    head = right[0]
                    remaining = right[1:]
                else:
                    head = BLANK
                    remaining = ""

                # Get valid transitions
                transitions = self.get_transitions(state, (head,))

                # Reject if there is not transition out of current state
                if not transitions:
                    next_level.append([left, self.reject_state, right, parent_index, -1])
                    total_transitions += 1
                    generated_configs += 1
                    continue

                # Create the next possible configurations
                for t_id, t in enumerate(transitions):
                    next_state = t["next"]
                    write_symbol = t["write"][0]
                    dir_to_move = t["move"][0]
                    
                    # Configure based on direction head moves
                    if dir_to_move == DIR_R:
                        new_left = left + write_symbol
                        new_right = remaining if remaining else BLANK
                    elif dir_to_move == DIR_L:
                        if left:
                            new_head = left[-1]
                            new_left = left[:-1]
                        else:
                            new_head = BLANK
                            new_left = ""
                        new_right = new_head + write_symbol + remaining
                    else:
                        new_left = left
                        new_right = write_symbol + remaining

                    next_level.append([new_left, next_state, new_right, parent_index, t_id])
                    total_transitions += 1
                    generated_configs += 1

            degree = (generated_configs / expanded_configs if expanded_configs > 0 else 0.0)

            # If accept found at current depth, print necessary info
            if accept_level is not None:
                # Required initial echo info
                print(self.machine_name)
                print(input_string)
                print(accept_level)
                print(total_transitions)
                print(f"String accepted in {accept_level}")
                print(f"Degree of nondeterminism: {degree:.2f}")
                self.print_trace_path(tree, accept_level, accept_index)
                return

            # If all branches have been rejected and no next level exists, then reject
            if not next_level and all_rejected:
                # Required initial echo info
                print(self.machine_name)
                print(input_string)
                print(depth)
                print(total_transitions)

                print(f"String rejected in {depth}")
                return

            tree.append(next_level)
            depth += 1

        # Max depth exceeded
        print(self.machine_name)
        print(input_string)
        print(max_depth)
        print(total_transitions)
        print(f"Execution stopped after {max_depth} steps.")

    def print_trace_path(self, tree, level, index):
        """
        Backtrack and print the path from root to the accepting node.
        Ref: Section 4.2 [cite: 165]
        """
        path = []

        # Append configurations to path
        while level >= 0:
            config = tree[level][index]
            path.append(config)
            parent_index = config[3]
            level -= 1
            index = parent_index

        path.reverse()

        # Print out the path
        print("\nExecution path:")
        for i, cfg in enumerate(path):
            left, state, right, _, _ = cfg
            head = right[0] if right else BLANK
            remaining = right[1:] if right else ""
            print(f"Level {i}: {left}, {state}, {head}{remaining}")