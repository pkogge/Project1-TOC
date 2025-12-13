from src.helpers.turing_machine import TuringMachineSimulator
# ==========================================
# PROGRAM 1: Nondeterministic TM
# ==========================================
class NTM_Tracer(TuringMachineSimulator):
    """
    simulates a NTM using BFS
    """
    def __init__(self, config_source):
        if isinstance(config_source, dict):
            self.load_machine_from_dict(config_source)
        else:
            super().__init__(config_source)

    def run(self, input_string, max_depth):
        """
        performs a BFS trace of the NTM computation tree
        """
        print(f"tracing NTM: {self.machine_name} on input '{input_string}'")
        
        # cfg: [left_tape, state, right_tape]
        initial_config = ["", self.start_state, input_string]
        
        # tree: list of levels
        computation_tree = [[initial_config]] 

        # depth counter
        current_depth = 0
        accepted_flag = False # unused in while loop, but kept for context

        while current_depth < max_depth and not accepted_flag:
            current_level_nodes = computation_tree[-1]
            next_level_nodes = []
            all_branches_rejected = True # tracks if all paths halt or reject

            for node in current_level_nodes:
                # get cfg and parent info
                if isinstance(node, dict):
                    current_cfg = node["config"]
                    parent_node = node
                else:
                    current_cfg = node
                    parent_node = None

                left, state, right = current_cfg

                # check halting states
                
                # accept
                if state == self.accept_state:
                    print(f"\nstring accepted in {current_depth}")

                    
                    total_children = sum(len(level) for level in computation_tree[1:])
                    
                    total_parents = sum(len(level) for level in computation_tree[:-1])

                    
                    degree = total_children / total_parents if total_parents > 0 else 0

                    print(f"degree of nondeterminism: {degree:.2f}")
                    self.print_trace_path(node) 
                    return

            
                if state == self.reject_state:
                    continue

                
                head_symbol = right[0] if right else "_"

                
                possible_moves = self.get_transitions(state, [head_symbol])

                if possible_moves:
                    all_branches_rejected = False 

                for move in possible_moves:
                    next_state = move["next"]
                    write_char = move["write"][0]
                    direction = move["move"][0]

                    # tape remainder
                    remaining_right = right[1:] if right else ""

                    # calculate new tape cfg
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

                    else:  
                        new_left = left
                        new_right = write_char + remaining_right

                    next_cfg = [new_left, next_state, new_right]
                    next_level_nodes.append({
                        "config": next_cfg,
                        "parent": node 
                    })

           
            
            # check for total rejection
            if not next_level_nodes and all_branches_rejected:
                print(f"\nstring rejected in {current_depth}")

                # total children sum
                total_children = sum(len(level) for level in computation_tree[1:])
                # total parent sum (including current level here)
                total_parents = sum(len(level) for level in computation_tree)
                
                # branching factor
                degree = total_children / total_parents if total_parents > 0 else 0

                print(f"degree of nondeterminism: {degree:.2f}")
                return

            
            computation_tree.append(next_level_nodes)
            current_depth += 1 

        # hit max_depth limit
        if current_depth >= max_depth:
            print(f"\nexecution stopped after {max_depth} steps.")

    def print_trace_path(self, final_node):
        """
        backtracks from accepting node and prints trace path
        """
        path_list = [] 
        current_node = final_node 

        # backtrack loop
        while True:
            if isinstance(current_node, dict):
                path_list.append(current_node["config"])
                current_node = current_node["parent"]
            else:
                path_list.append(current_node)
                break

        path_list.reverse()
        print("\n--- acceptance path trace ---")

        for left, state, right in path_list:
            head = right[0] if right else "_"
            rest = right[1:] if len(right) > 1 else ""
            print(f"{left}, {state}, {head}, {rest}")