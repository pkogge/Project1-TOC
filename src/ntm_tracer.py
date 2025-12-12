from src.helpers.turing_machine import (
    TuringMachineSimulator,
    BLANK,
    DIR_L,
    DIR_R,
    DIR_S,
)

# Julia Lizak
# TOC Project 2

# Program 1: Tracing NTM Behavior

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

        # suggested to do for analysis in directions!!!
        # for nondeterminsim metric
        nl_configs = 0
        nl_children = 0

        while depth < max_depth and not accepted:
            current_level = tree[-1]
            next_level = []
            all_rejected = True

            # TODO: STUDENT IMPLEMENTATION NEEDED
            # 1. Iterate through every config in current_level.
            for config in current_level:
                left, state, right = config

            # 2. Check if config is Accept (Stop and print success) [cite: 179]
                if state == self.accept_state:
                    accepted = True
                    # print so I know wha is happening
                    print(f"String accepted in {depth} transitions.")
                    print(f"Config: {left} {state} {right}")
                    print(f"Tree depth: {len(tree) - 1}")
                    print(f"Total transitions: {total_transitions}")
                    self.print_trace_path(tree)
                    if nl_configs > 0:
                        print(f"Avg nondeterminism: {nl_children / nl_configs:.3f}")

                    return

            # 3. Check if config is Reject (Stop this branch only) [cite: 181]
                if state == self.reject_state:
                    continue

            # 4. If not Accept/Reject, find valid transitions in self.transitions.
                head_now = right[0] if right else BLANK

                valid_transitions = self.get_transitions(state, (head_now,))

            # 5. If no explicit transition exists, treat as implicit Reject.
                if not valid_transitions:
                    continue

                # check if you hae at least found one child
                if valid_transitions: 
                    all_rejected = False
                    nl_configs += 1
                    nl_children += len(valid_transitions)

            # 6. Generate children configurations and append to next_level[cite: 148].
                for t in valid_transitions:
                    write_char = t["write"][0]
                    move_direction = t["move"][0]

                # and now write it 
                    if right:
                        written_right = write_char + right[1:]
                    else:
                        written_right = write_char

                # now move (i.e. nect level part)
                    if move_direction == DIR_S:
                    # don't move
                        new_left = left
                        new_right = written_right

                    elif move_direction == DIR_R:
                        new_left = left + written_right[0]
                        new_right = written_right[1:]

                    elif move_direction == DIR_L:
                    # need to move the head to the left once
                        if left:
                            new_head = left[-1]
                            new_left = left[:-1]
                        else:
                            new_head = BLANK
                            new_left = ""
                        new_right = new_head + written_right

                    else:
                    # this should not get to this point
                    # but just to finish the loop and statements, maybe an extra check
                    # just act like it stays put
                        new_left = left
                        new_right = written_right

                # now generate child config
                    total_transitions += 1
                    next_level.append([new_left, t["next"], new_right])


            # Placeholder for logic:
            if not next_level and all_rejected:
                # TODO: Handle "String rejected" output [cite: 258]
                print(f"String rejected in {depth} transitions.")
                print(f"Tree depth: {len(tree) - 1}")
                print(f"Total transitions: {total_transitions}")
                self.print_trace_path(tree)
                if nl_configs > 0:
                    print(f"Avg nondeterminism: {nl_children / nl_configs:.3f}")
                break

            tree.append(next_level)
            depth += 1

        if depth >= max_depth:
            print(f"Execution stopped after {max_depth} steps.")  # [cite: 259]
            print(f"Tree depth: {len(tree) - 1}")
            print(f"Total transitions: {total_transitions}")
            if nl_configs > 0:
                print(f"Avg nondeterminism: {nl_children / nl_configs:.3f}")
            self.print_trace_path(tree)



    def print_trace_path(self, final_node):
        """
        Backtrack and print the path from root to the accepting node.
        Ref: Section 4.2 [cite: 165]
        """
        for level, configs in enumerate(final_node):
            # print(f"Level: {level}: ")

            for left, state, right in configs:
                head = right[0] if right else BLANK
                rest = right[1:] if right else ""
                print(f" {left} {state} {head}{rest}")