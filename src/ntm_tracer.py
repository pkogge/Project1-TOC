from src.helpers.turing_machine import TuringMachineSimulator
from typing import Dict, List, Optional, Tuple

from src.helpers.turing_machine import (
    TuringMachineSimulator,
    BLANK,
    DIR_L,
    DIR_R,
    DIR_S,
)


# ==========================================
# PROGRAM 1: Nondeterministic TM [cite: 137]
# ==========================================
class NTM_Tracer(TuringMachineSimulator):
    def __init__(self, filename: str) -> None:
        super().__init__(filename)
        self._tree: List[List[dict]] = []

    def run(self, input_string: str, max_depth: int) -> None:
        tape0 = {i: ch for i, ch in enumerate(input_string)}
        root = {
            "tape": tape0,
            "head": 0,
            "state": self.start_state,
            "parent_level": None,
            "parent_index": None,
        }

        """
        Performs a Breadth-First Search (BFS) trace of the NTM.
        Ref: Section 4.1 "Trees as List of Lists" [cite: 146]
        """
        print(f"Tracing NTM: {self.machine_name} on input '{input_string}'")

        # Initial Configuration: ["", start_state, input_string]
        # Note: Represent configuration as triples (left, state, right) [cite: 156]

        # The tree is a list of lists of configurations
        tree: List[List[dict]] = [[root]]
        self._tree = tree
        depth = 0
        total_transitions = 0
        nonleaf_configs = 0
        transitions_from_nonleaf = 0
        accepted = False
        accept_node: Optional[Tuple[int, int]] = None
        deepest_reject_depth = 0
        deepest_reject_node: Optional[Tuple[int, int]] = None

        while depth < max_depth and not accepted:
            current_level = tree[-1]
            next_level = []

            # TODO: STUDENT IMPLEMENTATION NEEDED
            # 1. Iterate through every config in current_level.
            # 2. Check if config is Accept (Stop and print success) [cite: 179]
            # 3. Check if config is Reject (Stop this branch only) [cite: 181]
            # 4. If not Accept/Reject, find valid transitions in self.transitions.
            # 5. If no explicit transition exists, treat as implicit Reject.
            # 6. Generate children configurations and append to next_level[cite: 148].

            # Placeholder for logic:

            for cfg_index, cfg in enumerate(current_level):
                state = cfg["state"]
                if state == self.accept_state or state == self.reject_state:
                    continue

                head_pos = cfg["head"]
                current_symbol = cfg["tape"].get(head_pos, BLANK)
                transitions = self.get_transitions(state, (current_symbol,))
                nonleaf_configs += 1

                if not transitions:
                    transitions_from_nonleaf += 1
                    total_transitions += 1
                    new_cfg = {
                        "tape": dict(cfg["tape"]),
                        "head": head_pos,
                        "state": self.reject_state,
                        "parent_level": depth,
                        "parent_index": cfg_index,
                    }
                    next_level.append(new_cfg)
                    level_new = depth + 1
                    if level_new >= deepest_reject_depth:
                        deepest_reject_depth = level_new
                        deepest_reject_node = (level_new, len(next_level) - 1)
                    continue

                transitions_from_nonleaf += len(transitions)

                for t in transitions:
                    total_transitions += 1
                    write_symbol = t["write"][0]
                    move_dir = t["move"][0]
                    next_state = t["next"]

                    new_tape = dict(cfg["tape"])
                    new_tape[head_pos] = write_symbol
                    new_head = head_pos

                    if move_dir == DIR_L:
                        new_head -= 1
                    elif move_dir == DIR_R:
                        new_head += 1

                    new_cfg = {
                        "tape": new_tape,
                        "head": new_head,
                        "state": next_state,
                        "parent_level": depth,
                        "parent_index": cfg_index,
                    }
                    next_level.append(new_cfg)

                    if next_state == self.accept_state and not accepted:
                        accepted = True
                        accept_node = (depth + 1, len(next_level) - 1)

                if accepted:
                    break

            if not next_level:
                break

            tree.append(next_level)
            self._tree = tree
            depth += 1

            if accepted:
                break

        tree_depth = len(tree) - 1
        print(f"Machine: {self.machine_name}")
        print(f"Input: {input_string}")
        print(f"Tree depth: {tree_depth}")
        print(f"Transitions simulated: {total_transitions}")

        if nonleaf_configs > 0:
            print(f"Nondeterminism: {transitions_from_nonleaf / nonleaf_configs:.3f}")

        if depth >= max_depth and not accepted:
            print(f"Execution stopped after {max_depth} steps.")
            return

        if accepted and accept_node is not None:
            level, _ = accept_node
            print(f"String accepted in {level} steps.")
            self.print_trace_path(accept_node)
            return

        if deepest_reject_node is not None:
            level, _ = deepest_reject_node
            print(f"String rejected in {level} steps.")
        else:
            print("String rejected.")




    def print_trace_path(self, final_node):
        u"""
        Backtrack and print the path from root to the accepting node.
        Ref: Section 4.2 [cite: 165]
        """
        pass
        tree = self._tree
        level, index = final_node
        path = []

        while True:
            cfg = tree[level][index]
            path.append((level, cfg))
            parent_level = cfg["parent_level"]
            parent_index = cfg["parent_index"]
            if parent_level is None:
                break
            level = parent_level
            index = parent_index

        path.reverse()

        for lv, cfg in path:
            left, head_char, right = self._config_to_strings(cfg)
            print(f"Level {lv}")
            print(f"{left} {cfg['state']} {head_char}{right}")


    def _config_to_strings(self, cfg: dict):
        tape: Dict[int, str] = cfg["tape"]
        head: int = cfg["head"]

        indices = list(tape.keys()) + [head]
        min_i = min(indices)
        max_i = max(indices)

        left_chars = [tape.get(i, BLANK) for i in range(min_i, head)]
        left = "".join(left_chars)

        head_char = tape.get(head, BLANK)

        right_chars = [tape.get(i, BLANK) for i in range(head + 1, max_i + 1)]
        right = "".join(right_chars)

        return left, head_char, right
