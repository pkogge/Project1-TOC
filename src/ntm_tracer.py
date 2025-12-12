from src.helpers.turing_machine import TuringMachineSimulator, DIR_L, DIR_R, DIR_S, BLANK


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
        total_transitions = 0
        nonleaves = 0

        while depth < max_depth and not accepted:
            current_level = tree[-1]
            next_level = []
            all_rejected = True

            # TODO: STUDENT IMPLEMENTATION NEEDED
            # 1. Iterate through every config in current_level.
            for config in current_level:
                l, curr, r = config
                # 2. Check if config is Accept (Stop and print success) [cite: 179]
                if curr == self.accept_state:
                    print(f"\nAccepted. String was accepted at a depth of {depth} with configuration: {config} by simulating {total_transitions} transitions.")
                    self.print_trace_path(tree, nonleaves, total_transitions)
                    accepted = True
                    return
                # 3. Check if config is Reject (Stop this branch only) [cite: 181]
                if curr == self.reject_state:
                    continue
                # 4. If not Accept/Reject, find valid transitions in self.transitions.
                if len(r) > 0:
                    head = r[0]
                else:
                    head = BLANK
                transitions = self.get_transitions(curr, head)

                # 5. If no explicit transition exists, treat as implicit Reject.
                if len(transitions) >= 1:
                    nonleaves += 1
                total_transitions += len(transitions)

                if not transitions:
                    continue
                all_rejected = False

                # 6. Generate children configurations and append to next_level[cite: 148].
                for transition in transitions:
                    next_state, write, dir = transition['next'], transition['write'][0], transition['move'][0]
                    if len(r) > 0:
                        head = r[0]
                        new_r = r[1:]
                    else: # if r is empty, new_r is empty, head is blank
                        head = BLANK
                        r= ""
                        new_r = ""
                    
                    if dir == DIR_R:
                        new_l = l + write
                    elif dir == DIR_L:
                        if len(l) > 0:
                            new_head = l[-1]
                            new_l = l[:-1]
                            new_r = new_head + write + new_r
                        else:
                            new_l = ""
                            new_r = BLANK + write + new_r
                    elif dir == DIR_S:
                        new_l = l
                        new_r = write + new_r
                    
                    next_level.append([new_l, next_state, new_r])
                    
            if not next_level and all_rejected:
                # TODO: Handle "String rejected" output [cite: 258]
                print(f"String Rejected in {depth} steps.")
                return
            # debug statements
            # print(f"Left: {l}, Head: {head}, Right: {r} and {curr} and {next_state}")
            # print(f"Next Level: {next_level}")
            tree.append(next_level)
            depth += 1

        if depth >= max_depth:
            print(f"Execution stopped after {max_depth} steps.")  # [cite: 259]

    def print_trace_path(self, tree, nonleaves, total_transitions):
        """
        Backtrack and print the path from root to the accepting node.
        Ref: Section 4.2 [cite: 165]
        """
        print(f"\nDegree of Nondeterminism: {total_transitions / nonleaves}")
        print("NTM Tree Path:")
        depth = 0
        for level in tree:
            print(f"\nDepth {depth}:")
            # print(f"Level: {level}")
            for config in level:
                # print(f"Config: {config}")
                l, curr, r = config
                print(f"Left Stack: {l}, Current State: {curr}, Right Stack: {r}")
            depth += 1

