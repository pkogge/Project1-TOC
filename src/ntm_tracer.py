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

        #initial config (left, state, right)
        initial_config = ["", self.start_state, input_string]
        tree = [[initial_config]]

        depth = 0
        accepted = False

        while depth < max_depth and not accepted:
            current_level = tree[-1]
            next_level = []
            all_rejected = True

            for node in current_level:
                #normalize nodes
                if isinstance(node, dict):
                    cfg = node["config"]
                    parent = node
                else:
                    cfg = node
                    parent = None

                left, state, right = cfg

                #acce[t]
                if state == self.accept_state:
                    print(f"String accepted in {depth}")

                    total_children = sum(len(level) for level in tree[1:])
                    total_parents = sum(len(level) for level in tree[:-1])

                    degree = total_children / total_parents if total_parents > 0 else 0

                    print(f"Degree of Nondeterminism: {degree:.2f}")
                    self.print_trace_path(node)
                    return

                #reject (just kills this branch)
                if state == self.reject_state:
                    continue

                #symbol under head
                head_symbol = right[0] if right else "_"

                #fetches transitions
                possible_moves = self.get_transitions(state, [head_symbol])

                if possible_moves:
                    all_rejected = False

                for move in possible_moves:
                    next_state = move["next"]
                    write_char = move["write"][0]
                    direction = move["move"][0]

                    remaining_right = right[1:] if right else ""

                    if direction == "L":
                        if left:
                            new_left = left[:-1]
                            new_right = left[-1] + write_char + remaining_right
                        else:
                            new_left = ""
                            new_right = write_char + remaining_right

                    elif direction == "R":
                        new_left = left + write_char
                        new_right = remaining_right

                    else:  #stay
                        new_left = left
                        new_right = write_char + remaining_right

                    next_cfg = [new_left, next_state, new_right]
                    next_level.append({
                        "config": next_cfg,
                        "parent": node
                    })

            if not next_level and all_rejected:
                print(f"String rejected in {depth}")

                total_children = sum(len(level) for level in tree[1:])
                total_parents = sum(len(level) for level in tree)
                degree = total_children / total_parents if total_parents > 0 else 0

                print(f"Degree of Nondeterminism: {degree:.2f}")
                return

            tree.append(next_level)
            depth += 1

        if depth >= max_depth:
            print(f"Execution stopped after {max_depth} steps.")

    def print_trace_path(self, final_node):
        """
        Backtrack and print the path from root to the accepting node.
        Ref: Section 4.2 [cite: 165]
        """
        path = []
        curr = final_node

        while True:
            if isinstance(curr, dict):
                path.append(curr["config"])
                curr = curr["parent"]
            else:
                path.append(curr)
                break

        path.reverse()

        for left, state, right in path:
            head = right[0] if right else "_"
            rest = right[1:] if len(right) > 1 else ""
            print(f"{left}, {state}, {head}, {rest}")