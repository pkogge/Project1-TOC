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
            for config in current_level:
                left, state, right = config
                curr = right[0] if right else self.blank_symbol
            # 2. Check if config is Accept (Stop and print success) [cite: 179]
                if state == self.accept_state:
                    print(f'string accepted: depth = {depth}. path to acceptance: {config}')
                    accepted = True
                    break
            # 3. Check if config is Reject (Stop this branch only) [cite: 181]
                if state == self.reject_state:
                    continue
            # 4. If not Accept/Reject, find valid transitions in self.transitions.
                valid = False

                if right:
                    curr = right[0]
                else:
                    curr = self.blank_symbol

                for (src, read_ch), transitions in self.transitions.items():
                    if src == state and read_ch == curr:
                        for (dst, write_ch, dir) in transitions:
                            new_left = left.copy()
                            new_right = right.copy()

                            if new_right:
                                new_right[0] = write_ch
                            else:
                                new_right = [write_ch]
            # 5. If no explicit transition exists, treat as implicit Reject.
            # 6. Generate children configurations and append to next_level[cite: 148].

                            if dir == 'R':
                                new_left.append(new_right.pop(0))
                                if not new_right:
                                    new_right.append(self.blank_symbol)

                            elif dir == 'L':
                                new_right.insert(0, new_left.pop() if new_left else self.blank_symbol)

                            next_config = (new_left, dst, new_right)
                            next_level.append(next_config)

                if not valid and state not in [self.accept_state, self.reject_state]:
                    continue

            if accepted:
                return
                

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
