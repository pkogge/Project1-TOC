from src.helpers.turing_machine import TuringMachineSimulator, BLANK, WILDCARD

# ==========================================
# PROGRAM 1: Nondeterministic TM [cite: 137]
# ==========================================
class NTM_Tracer(TuringMachineSimulator):
    def __init__(self, filename):
        # Load the machine using the helper class logic
        super().__init__(filename)

    def run(self, input_string, max_depth):
        """
        Performs a Breadth-First Search (BFS) trace of the NTM.
        Ref: Section 4.1 "Trees as List of Lists" [cite: 146]
        """
        print(f"Tracing NTM: {self.machine_name} on input '{input_string}'")

        # Initial Configuration: ["", start_state, input_string]
        # Note: input_string should treat empty as BLANK if needed, but usually starts as is.
        initial_config = ["", self.start_state, input_string]

        # The tree is a list of lists of configurations
        tree = [[initial_config]]

        depth = 0
        total_transitions = 0

        while depth < max_depth:
            current_level = tree[-1]
            next_level = []
            
            # Print Level Info
            print(f"Level {depth}")
            for config in current_level:
                left, state, right = config
                # Visual format: Left, State, Right
                display_right = right if right else BLANK
                print(f"{left} {state} {display_right}")

            # Check for Acceptance in current level first
            for config in current_level:
                if config[1] == self.accept_state:
                    print(f"String accepted in {depth}") 
                    print(f"Total transitions simulated: {total_transitions}")
                    return

            # Process Transitions to generate next_level
            for config in current_level:
                left, state, right = config

                # Stop this branch if rejected
                if state == self.reject_state:
                    continue

                # Identify character under head
                head_char = right[0] if len(right) > 0 else BLANK

                # Use helper to find valid transitions
                # Helper expects tuple for k-tape compatibility
                valid_moves = self.get_transitions(state, (head_char,))

                for move in valid_moves:
                    # Parse transition details from helper dict
                    # NTM is 1-tape, so we access index 0 of the tuples
                    next_state = move['next']
                    write_char = move['write'][0]
                    direction = move['move'][0]

                    # Handle wildcard write '*' means do not change the character 
                    if write_char == WILDCARD:
                        write_char = head_char

                    # Construct new configuration
                    new_left = left
                    new_right = right

                    if direction == 'R':
                        new_left = left + write_char
                        new_right = right[1:] if len(right) > 1 else ""
                    elif direction == 'L':
                        if len(left) > 0:
                            char_from_left = left[-1]
                            new_left = left[:-1]
                            new_right = char_from_left + write_char + (right[1:] if len(right) > 1 else "")
                        else:
                            # Moving left at start of tape holds position (standard behavior)
                            # or inserts blank depending on specific convention. 
                            # Assuming "Stay" behavior at left edge or blank insertion:
                            new_right = BLANK + write_char + (right[1:] if len(right) > 1 else "")
                            new_left = ""
                    elif direction == 'S': # Stay Option
                        new_right = write_char + (right[1:] if len(right) > 1 else "")

                    # Append new configuration
                    next_level.append([new_left, next_state, new_right])
                    total_transitions += 1

            # If no configurations exist in next level, all branches died then Reject
            if not next_level:
                print(f"String rejected in {depth}")
                print(f"Total transitions simulated: {total_transitions}")
                return

            tree.append(next_level)
            depth += 1

        print(f"Execution stopped after {max_depth} steps.")
        print(f"Total transitions simulated: {total_transitions}")

    def print_trace_path(self, final_node):
        pass