# src/ntm_tracer.py
from typing import List, Dict, Any, Tuple
from src.helpers.turing_machine import TuringMachineSimulator

try:
    from src.helpers.turing_machine import BLANK, WILDCARD, DIR_L, DIR_R, DIR_S
except Exception:
    BLANK = "_"
    WILDCARD = "*"
    DIR_L = "L"
    DIR_R = "R"
    DIR_S = "S"


class NTM_Tracer(TuringMachineSimulator):
    def __init__(self, file_path: str):
        super().__init__(file_path)
        if getattr(self, "num_tapes", 1) != 1:
            print("Warning: NTM_Tracer instantiated for machine with num_tapes != 1")

    def run(self, input_string: str, max_depth: int = 100, verbose: bool = False) -> List[List[Dict[str, Any]]]:
        print(f"\n=== Tracing NTM: {getattr(self, 'machine_name', '<unknown>')} on input '{input_string}' ===")

        initial_right = input_string if input_string != "" else BLANK
        root = {"left": "", "state": self.start_state, "right": initial_right, "parent": None, "trans": None}
        tree: List[List[Dict[str, Any]]] = [[root]]

        depth = 0
        accept_node: Tuple[int, int] = None

        total_transitions_simulated = 0
        nonleaf_count = 0
        outgoing_transitions = 0

        accept_state = getattr(self, "accept_state", None)
        reject_state = getattr(self, "reject_state", None)

        while depth < max_depth:
            current_level = tree[-1]
            next_level: List[Dict[str, Any]] = []
            all_rejected = True

            for idx, cfg in enumerate(current_level):
                state = cfg["state"]
                left = cfg["left"]
                right = cfg["right"] if cfg["right"] is not None else BLANK
                head = right[0] if right else BLANK

                if accept_state is not None and state == accept_state:
                    accept_node = (depth, idx)
                    print(f"✓ Accepted at depth {depth} (level {depth} node #{idx}).")
                    break

                if reject_state is not None and state == reject_state:
                    if verbose:
                        print(f"[DBG] Level {depth} node {idx}: state={state!r} is reject; skipping")
                    continue

                # Find transitions first
                read_symbols = (head,)
                matches = self.get_transitions(state, read_symbols)

                if verbose:
                    print(f"[DBG] Level {depth} node {idx}: state={state!r}, head={head!r}, matches={len(matches)}")
                    for m in matches:
                        print(f"      match: read={m.get('read')}, next={m.get('next')}, write={m.get('write')}, move={m.get('move')}")

                # Only treat as a non-leaf if it actually has outgoing transitions
                if not matches:
                    continue

                # Now increment counts because this node actually expands
                nonleaf_count += 1
                all_rejected = False
                outgoing_transitions += len(matches)

                for t in matches:
                    next_state = t.get("next")
                    write_sym = t.get("write", (BLANK,))[0] if t.get("write") else BLANK
                    move_sym = t.get("move", (DIR_R,))[0] if t.get("move") else DIR_R

                    if write_sym == WILDCARD:
                        write_char = head
                    else:
                        write_char = write_sym if write_sym != "" else BLANK

                    if right is None or right == "":
                        new_right_after_write = write_char
                    else:
                        tail = right[1:] if len(right) > 1 else BLANK
                        new_right_after_write = write_char + tail

                    if move_sym == DIR_R:
                        if new_right_after_write is None or new_right_after_write == "":
                            moved = BLANK
                            new_left = left + moved
                            new_right = BLANK
                        else:
                            moved = new_right_after_write[0]
                            new_left = left + moved
                            new_right = new_right_after_write[1:] if len(new_right_after_write) > 1 else BLANK

                    elif move_sym == DIR_L:
                        if left:
                            moved = left[-1]
                            new_left = left[:-1]
                            new_right = moved + new_right_after_write
                        else:
                            new_left = ""
                            new_right = BLANK + new_right_after_write

                    else:
                        new_left = left
                        new_right = new_right_after_write

                    child = {
                        "left": new_left,
                        "state": next_state,
                        "right": new_right,
                        "parent": (depth, idx),
                        "trans": f"{state},{head} -> {next_state},{write_sym},{move_sym}"
                    }
                    next_level.append(child)
                    total_transitions_simulated += 1

            if accept_node:
                break

            if not next_level and all_rejected:
                print(f"✗ String rejected in {depth} transitions (all branches dead at level {depth}).")
                break

            if verbose:
                print(f"[DBG] End of level {depth}: nonleaf_count={nonleaf_count}, outgoing_transitions={outgoing_transitions}, total_simulated={total_transitions_simulated}")

            tree.append(next_level)
            depth += 1

        if depth >= max_depth and not accept_node:
            print(f"⚠ Execution stopped after reaching max_depth = {max_depth} (no accept found).")

        print("\n--- SUMMARY ---")
        print("Machine:", getattr(self, "machine_name", "<unknown>"))
        print("Input:", input_string)
        print("Depth reached:", depth)
        print("Total transitions simulated:", total_transitions_simulated)
        nondet = (outgoing_transitions / nonleaf_count) if nonleaf_count else 0.0
        print(f"Nondeterminism = {nondet:.4f} ({outgoing_transitions}/{nonleaf_count})")

        if accept_node:
            print("\nAccepting path:")
            path = self.print_trace_path(tree, accept_node)
            for lvl, conf in enumerate(path):
                print(f"Level {lvl}: '{conf['left']}', {conf['state']}, '{conf['right']}'  via {conf.get('trans')}")

        return tree

    def print_trace_path(self, tree: List[List[Dict[str, Any]]], final_node: Tuple[int, int]) -> List[Dict[str, Any]]:
        level, idx = final_node
        path: List[Dict[str, Any]] = []
        cur = (level, idx)
        while cur is not None:
            lev, i = cur
            conf = tree[lev][i]
            path.insert(0, conf)
            cur = conf.get("parent")
        return path
