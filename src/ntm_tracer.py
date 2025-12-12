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
        BLANK = "_"
        initial_config = ["", self.start_state, input_string]

        # The tree is a list of lists of configurations
        tree = [[initial_config]]

        depth = 0
        accepted = False

        # helper variables
        parents = {(0, 0): None}
        final_loc = None
        total_transitions = 0  # count all generated child configurations

        # helper function that gets current head
        def _head_char(cfg):
            right = cfg[2]
            return right[0] if (isinstance(right, str) and right) else BLANK

        # helper function that applies a single transition
        def _apply(cfg, next_state, write, move):
            left, _state, right = cfg

            # write replaces current head cell (or blank)
            if isinstance(right, str) and len(right) > 0:
                written = write + right[1:]
            else:
                written = write

            # move head
            if move == "R":
                if written:
                    new_left = left + written[0]
                    new_right = written[1:]
                else:
                    new_left = left + BLANK
                    new_right = ""
            else:  # move == "L"
                if left:
                    new_left = left[:-1]
                    new_right = left[-1] + written
                else:
                    new_left = ""
                    new_right = BLANK + written

            return [new_left, next_state, new_right]

        # helper function that prints every level and its configurations
        def _print_levels():
            print("\nFull level-by-level configurations:")
            for lvl, level in enumerate(tree):
                print(f"Level {lvl}")
                for cfg in level:
                    lft, st, rgt = cfg
                    print(f"  {lft} , {st} , {_head_char(cfg)} , {rgt}")

        # helper function that prints summary line
        def _print_summary():
            print(f"\nMachine: {self.machine_name}")
            print(f"Initial string: '{input_string}'")
            print(f"Depth of configuration tree: {depth}")
            print(f"Total transitions simulated: {total_transitions}")

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

            for idx, cfg in enumerate(current_level):
                left, state, right = cfg

                # 2. Check if config is Accept (Stop and print success) [cite: 179]
                if state == self.accept_state:
                    accepted = True
                    final_loc = (depth, idx)
                    _print_summary()
                    print(f"String accepted in {depth} transitions.")  # [cite: 179]

                    self._tree = tree
                    self._parents = parents
                    _print_levels()
                    self.print_trace_path(final_loc)
                    return

                # 3. Check if config is Reject (Stop this branch only) [cite: 181]
                if state == self.reject_state:
                    continue

                all_rejected = False

                # 4. If not Accept/Reject, find valid transitions
                read = _head_char(cfg)

                try:
                    choices = self.get_transitions(state, read) or []
                except Exception:
                    choices = []

                # fallback for dict-based transitions
                if not choices:
                    try:
                        choices = self.transitions.get((state, read), [])
                    except Exception:
                        choices = []

                # 5. If no explicit transition exists, treat as implicit Reject.
                if not choices:
                    child = [left, self.reject_state, right]
                    next_level.append(child)
                    parents[(depth + 1, len(next_level) - 1)] = (depth, idx)
                    total_transitions += 1
                    continue

                # 6. Generate children configurations and append to next_level[cite: 148].
                for tr in choices:
                    if isinstance(tr, dict):
                        write = tr.get("write")
                        move = tr.get("move")
                        next_state = tr.get("next")

                        if isinstance(write, (list, tuple)):
                            write = write[0]
                        if isinstance(move, (list, tuple)):
                            move = move[0]

                        write = str(write)
                        move = str(move)
                        next_state = str(next_state)
                    else:
                        next_state, write, move = tr

                    child = _apply(cfg, next_state, write, move)
                    next_level.append(child)
                    parents[(depth + 1, len(next_level) - 1)] = (depth, idx)
                    total_transitions += 1

            # Placeholder for logic:
            if not next_level and all_rejected:
                _print_summary()
                print(f"String rejected in {depth} transitions.")  # [cite: 258]
                _print_levels()
                break

            tree.append(next_level)
            depth += 1

        if depth >= max_depth:
            print(f"Execution stopped after {max_depth} steps.")  # [cite: 259]
            _print_summary()

    def print_trace_path(self, final_node):
        """
        Backtrack and print the path from root to the accepting node.
        Ref: Section 4.2 [cite: 165]
        """
        try:
            tree = self._tree
            parents = self._parents
        except AttributeError:
            return

        if final_node is None:
            return

        chain = []
        cur = final_node
        while cur is not None:
            chain.append(cur)
            cur = parents.get(cur)
        chain.reverse()

        BLANK = "_"

        def _head_char(cfg):
            return cfg[2][0] if cfg[2] else BLANK

        print("Accepting path:")
        for lvl, idx in chain:
            cfg = tree[lvl][idx]
            left, state, right = cfg
            print(f"  level {lvl}: {left} , {state} , {_head_char(cfg)} , {right}")
