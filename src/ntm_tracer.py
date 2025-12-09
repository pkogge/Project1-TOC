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
        transitions_count = 0
        parent_dict = {}

        while depth < max_depth and not accepted:
            current_level = tree[-1]
            next_level = []
            all_rejected = True

            # TODO: STUDENT IMPLEMENTATION NEEDED
            # 1. Iterate through every config in current_level.
            for node in current_level:
                left_str, curr_st, right_str = node
                # 2. Check if config is Accept (Stop and print success) [cite: 179]
                if curr_st == self.accept_state:
                    # Printing the number of states it went through
                    print(f"String accepted in {depth} steps.") 
                    self.parents = parent_dict
                    self.final_node = tuple(node)
                    self.print_trace_path(node)
                    accepted = True
                    all_rejected = False
                    break

                # 3. Check if config is Reject (Stop this branch only) [cite: 181]
                if curr_st == self.reject_state:
                    continue

                # 4. If not Accept/Reject, find valid transitions in self.transitions.
                if right_str == "":
                    sym = "_"
                else:
                    sym = right_str[0]

                moves = self.get_transitions(curr_st, (sym,))

                # 5. If no explicit transition exists, treat as implicit Reject.
                if not moves:
                    continue
                else:
                    all_rejected = False

                # 6. Generate children configurations and append to next_level[cite: 148].
                for step in moves:
                    next_state = step["next"]
                    wsym = step["write"][0] # wsym = Write Symbol
                    move_dir = step["move"][0]

                    # Writing to the head of the tape
                    if right_str != "":
                        base_right = wsym + right_str[1:]
                    else:
                        base_right = wsym

                    # Moving the head and updating string on both sides
                    if move_dir == "R":
                        new_left = left_str + wsym
                        new_right = right_str[1:] if len(right_str) > 1 else "_"
                    elif move_dir == "L":
                        new_left = left_str[:-1] if left_str else ""
                        temp = left_str[-1] if left_str else "_"
                        new_right = temp + base_right
                    # If the direction is S 
                    else:
                        new_left = left_str
                        new_right = base_right

                    transitions_count += 1
                    child_cfg = [new_left, next_state, new_right]
                    next_level.append(child_cfg)
                    child_key = (new_left, next_state, new_right)
                    parent_key = tuple(node)

                    if child_key not in parent_dict:
                        parent_dict[child_key] = parent_key

            # Placeholder for logic:
            if not next_level and all_rejected:
                # TODO: Handle "String rejected" output [cite: 258]
                print(f"String rejected in {depth} steps.")
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
        ancestor_map = self.parents
        key = tuple(final_node)
        seq = []

        while key is not None:
            seq.append(key)
            key = ancestor_map.get(key, None)

        for i in range(len(seq) - 1, -1, -1):
            left_part, state, right_part = seq[i]
            if right_part:
                head_symbol = right_part[0]
                tail = right_part[1:]
            else:
                head_symbol = "_"
                tail = ""
            print(f"{left_part}, {state}, {head_symbol}, {tail}")
