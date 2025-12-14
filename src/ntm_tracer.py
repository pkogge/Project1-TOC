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
        initial_config = ["", self.start_state, input_string, -1, -1]

        # The tree is a list of lists of configurations
        tree = [[initial_config]]

        depth = 0
        accepted = False
        final_node = None

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

            for i, config in enumerate(current_level):
                left = config[0]
                state = config[1]
                right = config[2]

                # accept
                if state == self.accept_state:
                    accepted = True
                    final_node = config
                    break

                # reject
                if state == self.reject_state:
                    continue

                # read symbol
                if right:
                    read = right[0]
                else:
                    read = "_"

                # no transitions from this state
                if state not in self.transitions:
                    next_level.append([left, self.reject_state, right, i, -1])
                    continue

                matches = []
                for tnum, t in enumerate(self.transitions[state]):
                    if t["read"][0] == read:
                        matches.append((tnum, t))

                # implicit reject
                if not matches:
                    next_level.append([left, self.reject_state, right, i, -1])
                    continue

                all_rejected = False

                # create children
                for tnum, t in matches:
                    newstate = t["next"]
                    write = t["write"][0]
                    move = t["move"][0]

                    if right:
                        newright = write + right[1:]
                    else:
                        newright = write

                    if move == "R":
                        newleft = left + newright[0]
                        newright = newright[1:] if len(newright) > 1 else ""
                    else:  # L
                        if left:
                            head = left[-1]
                            newleft = left[:-1]
                        else:
                            head = "_"
                            newleft = ""
                        newright = head + newright

                    next_level.append([newleft, newstate, newright, i, tnum])

            if accepted:
                break

            # Placeholder for logic:
            if not next_level and all_rejected:
                # TODO: Handle "String rejected" output [cite: 258]
                self.print_depth_and_trans(tree)
                print(f"String rejected in {len(tree) - 1} transitions")
                return

            tree.append(next_level)
            depth += 1

        if depth >= max_depth:
            print(f"Execution stopped after {max_depth} steps.")  # [cite: 259]
            self.print_dt(tree)
            return

        if accepted:
            self.print_dt(tree)
            for level, configs in enumerate(tree):
                trimmed = [c[:3] for c in configs]
                print(f"Level {level}: {trimmed}")
            self.print_trace_path(final_node, tree)

    def print_trace_path(self, final_node, tree):
        """
        Backtrack and print the path from root to the accepting node.
        Ref: Section 4.2 [cite: 165]
        """
        path = []
        node = final_node
        level = len(tree) - 1

        # backtrack
        while True:
            path.append(node)
            parent = node[3]
            if parent == -1:
                break
            level -= 1
            node = tree[level][parent]

        path.reverse()

        print(f"String accepted in {len(path) - 1} transitions")

        for depth, config in enumerate(path):
            left = config[0]
            state = config[1]
            right = config[2]
            print(f"Level {depth}: '{left}', '{state}', '{right}'")

    def print_dt(self, tree):
        total = 0
        for level in tree:
            total += len(level)

        print(f"Tree Depth: {len(tree) - 1}")
        print(f"Transitions simulated: {total}")

