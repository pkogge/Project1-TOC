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
            
            if not hasattr(self, "_transitions_simulated"):
                self._transitions_simulated = 0
            if not hasattr(self, "_nonleaf_configs"):
                self._nonleaf_configs = 0
            if not hasattr(self, "_outgoing_transitions"):
                self._outgoing_transitions = 0

            accept_node= None

            for parent_node, config in enumerate(current_level):
                if len(config) == 3:
                    config.extend([-1, -1])

                left_node = config[0]
                state = config[1]
                right_node = config[2]

                if state == self.accept_state:
                    self._trace_tree = tree

                    print(f"String accepted in {depth} steps.")
                    print(f"Depth: {depth}")
                    print(f"Transitions simulated: {self._transitions_simulated}")

                    if self._nonleaf_configs > 0:
                        print(f"Nondeterminism: {self._outgoing_transitions / self._nonleaf_configs}")

                    self.print_trace_path((depth, parent_node))

                    accepted = True
                    accept_node= (depth, parent_node)

                    break

                if state == self.reject_state:
                    continue

                all_rejected = False

                head_symbol = right_node[0] if right_node else "_"
                valid_transition = self.get_transitions(state, (head_symbol,))

                if not valid_transition:

                    child_node = [left_node, self.reject_state, right_node, parent_node, -1]
                    next_level.append(child_node)
                    self._transitions_simulated += 1

                    continue

                self._nonleaf_configs += 1
                self._outgoing_transitions += len(valid_transition)

                for transition_idx, t in enumerate(valid_transition):

                    next_state = t["next"]
                    character_written = t["write"][0]
                    direction = t["move"][0]

                    if right_node:
                        right_written = character_written + right_node[1:]

                    else:
                        right_written = character_written

                    if direction == "R":
                        new_left_node = left_node + character_written
                        if len(right_written) > 1: 
                            new_right_node = right_written[1:] 

                        else:
                            new_right_node = ""

                    elif direction == "L":

                        if left_node:
                            new_left_node = left_node[:-1]
                            new_right_node = left_node[-1] + right_written

                        else:
                            new_left_node = ""
                            new_right_node = "_" + right_written

                    else:
                        
                        new_left_node = left_node
                        
                        new_right_node = right_written

                    child_node = [new_left_node, next_state, new_right_node, parent_node, transition_idx]

                    next_level.append(child_node)

                    self._transitions_simulated += 1

                    if next_state == self.accept_state:

                        tree.append(next_level)
                        self._trace_tree = tree

                        print(f"String accepted in {depth + 1} steps.")
                        print(f"Depth: {depth + 1}")
                        print(f"Transitions simulated: {self._transitions_simulated}")


                        if self._nonleaf_configs > 0:
                            print(f"Nondeterminism: {self._outgoing_transitions / self._nonleaf_configs}")

                        self.print_trace_path((depth + 1, len(next_level) - 1))

                        accepted = True

                        accept_node= (depth + 1, len(next_level) - 1)

                        break

                if accepted:
                    break

            if accepted:
                break

            # Placeholder for logic:
            if not next_level and all_rejected:
                # TODO: Handle "String rejected" output [cite: 258]

                print(f"String rejected in {depth} steps.")
                print(f"Depth: {depth}")

                if hasattr(self, "_transitions_simulated"):
                    print(f"Transitions simulated: {self._transitions_simulated}")

                if hasattr(self, "_nonleaf_configs") and self._nonleaf_configs > 0:
                    print(f"Nondeterminism: {self._outgoing_transitions / self._nonleaf_configs}")

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
        if not hasattr(self, "_trace_tree"):
            return

        tree = self._trace_tree
        level_index = final_node[0]
        node_index = final_node[1]

        path = []
        lvl = level_index
        idx = node_index

        while lvl >= 0 and idx >= 0 and lvl < len(tree) and idx < len(tree[lvl]):
            config = tree[lvl][idx]

            if len(config) == 3:
                config.extend([-1, -1])

            path.append((lvl, config))
            idx = config[3]
            lvl -= 1

        path.reverse()

        for lvl, config in path:
            
            left_node = config[0]

            state = config[1]

            right_node = config[2]

            if right_node:

                head_char = right_node[0]
                rest = right_node[1:]

            else:

                head_char = "_"
                rest = ""

            print(f"Level {lvl}")
            print(f"{left_node} {state} {head_char} {rest}")
