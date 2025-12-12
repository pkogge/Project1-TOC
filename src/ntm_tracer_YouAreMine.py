
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
        BLANK = "_"

        # Initial Configuration: ["", start_state, input_string]
        # Note: Represent configuration as triples (left, state, right) [cite: 156]
        # CD NOTED - (adapted: node format used here is [left, state, right, parent_idx] with parent last)
        # initial config: head starts over the leading '$' - THIS IS A CRUCIAL ASSUMPTION
        initial_config = ["", self.start_state, "$" + input_string + BLANK, None]
        
        # The tree is a list of lists of configurations
        tree = [[initial_config]]

        depth = 0
        total_cfg = 0
        used_cfg = 0

        while depth < max_depth:
            current_level = tree[-1]
            next_level = []
            all_rejected = True

            # TODO: STUDENT IMPLEMENTATION NEEDED
            for index, cfg in enumerate(current_level):
                

                left, state, right = cfg[0], cfg[1], cfg[2]

                if state == self.accept_state:
                    print(f"Accepted, {input_string} was accepted after {depth} steps with a total of {total_cfg} transitions.")
                    self.print_trace_path(cfg, tree, depth)
                    return
                if state == self.reject_state:
                    continue

                char = right[0] if (isinstance(right, str) and right) else BLANK

                valid = self.get_transitions(state, char) or []
                if not valid:
                    continue
                
                for a in valid:
                    writeSym = a['write'][0]
                    moveChar = a['move'][0]
                    nextState = a['next']

                    right = (writeSym + right[1:]) if (isinstance(right, str) and len(right) > 0) else writeSym

                    if moveChar == 'R':
                        if right:
                            left = left + right[0]
                            right = right[1:]
                        else:
                            left = left + BLANK
                            right = ""
                    elif moveChar == 'L':
                        if left:
                            right = left[-1] + right
                            left = left[:-1]
                        else:
                            right = BLANK + right

                    next_level.append([left, nextState, right, index])
                    total_cfg += 1
                    all_rejected = False

            if not next_level and all_rejected:
                # TODO: Handle "String rejected" output [cite: 258]
                print(f"Rejected, {input_string} was rejected after {depth} steps with a total of {total_cfg} transitions")
                self.print_trace_path(current_level[0], tree, depth)
                return

            used_cfg += len(current_level)
            tree.append(next_level)
            depth += 1

        if depth >= max_depth:
            print(f"Execution stopped after {max_depth} steps.")  # [cite: 259]
            return


    def print_trace_path(self, final_node, tree, depth):
        """
        Backtrack and print the path from root to the accepting node.
        Expects nodes of form [left, state, right, parent_idx] (parent_idx may be None).
        """
        if final_node is None or not tree:
            print("There is nothing to trace.")
            return []

        path = []
        current = final_node
        curr_level = depth

        while current is not None and curr_level >= 0:
            path.append((curr_level, current))

            index = None
            if isinstance(current, (list, tuple)) and len(current) >= 4:
                index = current[-1]

            if index is None:
                break

            curr_level -= 1
            current = tree[curr_level][index] if curr_level >= 0 else None

        path.reverse()

        print("\nStart:")
        for level, node in path:
            print(f"Level: {level}")
            if isinstance(node, (list, tuple)) and len(node) >= 3:
                print(node[0], node[1], node[2])
            else:
                print(str(node))
        print("End\n")
        return path
