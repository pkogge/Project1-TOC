from src.helpers.turing_machine import TuringMachineSimulator

### Example Input
# a plus         Name of machine
# q1,q2,q3       List of state names for Q
# a              List of characters from Σ
# a,_            List of characters from Γ
# q1             The start state
# q3             Name of Accept state
# qreject        Name of Reject state

## Instructions for the machine to follow outlined:
# The name of a state that the machine might be in.
# 2. A character from Σ.
# 3. The name of a state that the machine may go into if that character was found next
# on the input.
# 4. The character from Γ that should replace the current tape cell.
# 5. Either a L or a R denoting which direction to move the head next.
# It is possible (in fact needed for NTMs) that two rows in a file have the same first state
# and character, and different second states. This represents non-determinism.
# Unlike NFAs and PDAs, there is no needed support for εs.
# Finally, there is no assumed ordering of transitions in any way. Transitions from any
# state may be found in any order, and interleaved with other transitions from other states
# in any order
# q1,a,q1,a,R
# q1,a,q2,a,R
# q2,_,q3,_,L


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

        # parent dictionary
        parents = { tuple(initial_config) : None}

        while depth < max_depth and not accepted:
            current_level = tree[-1]
            next_level = []
            all_rejected = True

            # TODO: STUDENT IMPLEMENTATION NEEDED
            # 1. Iterate through every config in current_level.
            for config in current_level:
                left, state, right = config # initialize variables for each part of tuple
                # 2. Check if config is Accept (Stop and print success) [cite: 179]
                if state == self.accept_state:
                    print(f"String accepted in {depth}")

                    # make parent map and final node available for printing
                    self.parents = parents
                    self.final_node = tuple(config)
                    self.print_trace_path(config)
                    accepted = True
                    break

                # 3. Check if config is Reject (Stop this branch only) [cite: 181]
                if state == self.reject_state:
                    continue

                # 4. If not Accept/Reject, find valid transitions in self.transitions.
                if right == "": # checks if symbol is a blank
                    read_symbol = "_"
                else:
                    read_symbol = right[0] # reads symbol under tape head

                transitions = self.get_transitions(state, (read_symbol,))
                
                # 5. If no explicit transition exists, treat as implicit Reject.
                if not transitions:
                    continue
                else:
                    all_rejected = False
                # 6. Generate children configurations and append to next_level[cite: 148].
                for x in transitions:
                    next_state = x["next"]
                    write_symbol = x["write"][0]
                    move = x["move"][0]

                    # Apply the write section
                    if right == "":
                        new_right = write_symbol
                    else:
                        new_right = write_symbol + right[1:]

                    # now move head in left or right direction
                    if move == "R":
                        new_left = left + write_symbol
                        new_right = right[1:] if len(right) > 1 else "_"
                    elif move == "L":
                        new_left = left[:-1] if left else ""
                        pulled = left[-1] if left else "_"
                        new_right = pulled + new_right
                    else: # stay at position
                        new_left = left
                    
                    new_config = [new_left, next_state, new_right]
                    next_level.append(new_config)
                    child_t = (new_left, next_state, new_right)
                    parent_t = tuple(config)

                    if child_t not in parents:
                        parents[child_t] = parent_t

            # break out of while loop if string accepted
            if accepted:
                break

            # Placeholder for logic:
            if not next_level and all_rejected:
                # TODO: Handle "String rejected" output [cite: 258]
                print(f"String rejected in {depth}")
                break

            tree.append(next_level)
            depth += 1

        if depth >= max_depth:
            print(f"Execution stopped after, {max_depth}, steps.")  # [cite: 259]

    def print_trace_path(self, final_node):
        """
        Backtrack and print the path from root to the accepting node.
        Ref: Section 4.2 [cite: 165]
        """

        parents = self.parents
        curr = tuple(final_node)
        path = []

        while curr is not None:
            path.append(curr)
            curr = parents.get(curr)
        
        path.reverse()

        for (left, state, right) in path:
            head = right[0] if right else "_"
            rest = right[1:] if len(right) > 1 else ""
            print(f"{left}, {state}, {head}, {rest}")
