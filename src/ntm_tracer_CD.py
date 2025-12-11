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
        blank = "_"

        # Initial Configuration: ["", start_state, input_string]
        # Note: Represent configuration as triples (left, state, right) [cite: 156]
        # CD NOTED - (adapted: node format used here is [left, state, right, parent_idx] with parent last)
        # initial config: head starts over the leading '$' - THIS IS A CRUCIAL ASSUMPTION
        initial_config = ["", self.start_state, "$" + input_string + blank, None]
        
        # The tree is a list of lists of configurations
        tree = [[initial_config]]

        depth = 0
        total_configs = 0
        used_configs = 0

        while depth < max_depth:
            current_level = tree[-1]
            next_level = []
            all_rejected = True

            # TODO: STUDENT IMPLEMENTATION NEEDED
            
            # 1. Iterate through every config in current_level.
            for parent_idx, config in enumerate(current_level):
                

                left, state, right = config[0], config[1], config[2]

                # 2. Check if config is Accept (Stop and print success) [cite: 179]
                if state == self.accept_state:
                    print(f"Accepted - {input_string} - {depth} depth, {total_configs} transitions")
                    self.print_trace_path(config, tree, depth)
                    return
                # 3. Check if config is Reject (Stop this branch only) [cite: 181]
                if state == self.reject_state:
                    continue

                # 4. If not Accept/Reject, find valid transitions in self.transitions.
                symbol = right[0] if (isinstance(right, str) and right) else blank

                # 5. If no explicit transition exists, treat as implicit Reject.
                valid = self.get_transitions(state, symbol) or []
                if not valid:
                    continue
                
                # 6. Generate children configurations and append to next_level[cite: 148].
                for tr in valid:
                    writeSym = tr['write'][0]
                    moveCh = tr['move'][0]
                    nextState = tr['next']

                    # fresh copies
                    l = left
                    r = right

                    # write
                    r = (writeSym + r[1:]) if (isinstance(r, str) and len(r) > 0) else writeSym

                    # move
                    if moveCh == 'R':
                        if r:
                            l = l + r[0]
                            r = r[1:]
                        else:
                            l = l + blank
                            r = ""
                    elif moveCh == 'L':
                        if l:
                            r = l[-1] + r
                            l = l[:-1]
                        else:
                            # moving left from leftmost -> prepend blank
                            r = blank + r

                    next_level.append([l, nextState, r, parent_idx])
                    total_configs += 1
                    all_rejected = False
            # Placeholder for logic:
            if not next_level and all_rejected:
                # TODO: Handle "String rejected" output [cite: 258]
                print(f"Rejected - {input_string} - {depth} depth, {total_configs} transitions")
                # backtrace from first node in this level (best-effort)
                self.print_trace_path(current_level[0], tree, depth)
                return

            used_configs += len(current_level)
            tree.append(next_level)
            depth += 1

        if depth >= max_depth:
            print(f"Execution stopped after {max_depth} steps.")  # [cite: 259]
            return


    def print_trace_path(self, final_node, tree, level):
        """
        Backtrack and print the path from root to the accepting node.
        Expects nodes of form [left, state, right, parent_idx] (parent_idx may be None).
        """
        if final_node is None or not tree:
            print("Nothing to trace.")
            return []

        path = []
        current = final_node
        curr_level = level

        while True:
            path.append((curr_level, current))
            parent_idx = current[-1] if (isinstance(current, (list, tuple)) and len(current) >= 4) else None
            if parent_idx is None:
                break
            curr_level -= 1
            if curr_level < 0:
                break
            current = tree[curr_level][parent_idx]

        path.reverse()

        print("\n_")
        for lvl, node in path:
            print(f"Level: {lvl}")
            if isinstance(node, (list, tuple)) and len(node) >= 3:
                print(node[0], node[1], node[2])
            else:
                print(str(node))
        print("--\n")
        return path