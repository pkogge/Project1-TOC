from src.helpers.turing_machine import TuringMachineSimulator, WILDCARD, DIR_L, DIR_R, DIR_S

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
        initial_config = ["", self.start_state, input_string, None]

        # The tree is a list of lists of configurations
        tree = [[initial_config]]
        depth = 0
        accepted = False
        transitions_simulated = 0
        
        while depth < max_depth and not accepted:
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

            # 1. Iterate through every config in current_level.
            for config in current_level:
                left, state, right, parent = config

                # 2. Check if config is Accept (Stop and print success) [cite: 179]
                if state == self.accept_state:
                    accepted = True
                    print(f"Machine: {self.machine_name}")
                    print(f"Input: {input_string}")
                    print(f"Depth of tree: {depth}")
                    print(f"String accepted in {depth} steps.")
                    print(f"Total transitions simulated: {transitions_simulated}")
                    self.print_trace_path(config)
                    return

                # 3. Check if config is Reject (Stop this branch only) [cite: 181]
                if state == self.reject_state:
                    continue
                all_rejected = False
                if right:
                    head = right[0]
                    tail = right[1:]
                else:
                    head = "_"
                    tail = ""

                # 4. If not Accept/Reject, find valid transitions in self.transitions.
                transitions = self.get_transitions(state, (head,))

                # 5. If no explicit transition exists, treat as implicit Reject.
                if not transitions:
                    next_level.append([left, self.reject_state, right, config])
                    continue

                # 6. Generate children configurations and append to next_level[cite: 148].
                for t in transitions:
                    transitions_simulated += 1
                    write = t["write"][0]
                    move = t["move"][0]
                    next_state = t["next"]
                    if write == WILDCARD:
                        write = head
                    if move == DIR_R:
                        new_left = left + write
                        new_right = tail
                    elif move == DIR_L:
                        new_left = left[:-1] if left else ""
                        new_head = left[-1] if left else "_"
                        new_right = new_head + write + tail
                    else:
                        new_left = left
                        new_right = write + tail

                    next_level.append([new_left, next_state, new_right, config]) 

            if not next_level and all_rejected:
                # TODO: Handle "String rejected" output [cite: 258]
                print(f"Machine: {self.machine_name}")
                print(f"Input: {input_string}")
                print(f"Depth of tree: {depth}")
                print(f"String rejected in {depth} steps.")
                print(f"Total transitions simulated: {transitions_simulated}")
                return

            tree.append(next_level)
            depth += 1

        if depth >= max_depth:
            print(f"Execution stopped after {max_depth} steps.")  # [cite: 259]

    def print_trace_path(self, final_node):
        """
        Backtrack and print the path from root to the accepting node.
        Ref: Section 4.2 [cite: 165]
        """
        path = []
        node = final_node

        while node is not None:
            left, state, right, parent = node
            path.append((left, state, right))
            node = parent

        for left, state, right in reversed(path):
            head = right[0] if right else "_"
            tail = right[1:] if right else ""
            print(f"{left}, {state}, {head}, {tail}")
        