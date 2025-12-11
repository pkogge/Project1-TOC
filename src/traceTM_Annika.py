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
        parent_index = None
        initial_config = ["", self.start_state, input_string, parent_index]

        # The tree is a list of lists of configurations
        tree = [[initial_config]]

        depth = 0
        accepted = False
        
        transitionCount = 0

        while depth < max_depth and not accepted:
            current_level = tree[-1]
            next_level = []
            all_rejected = True

            # TODO: STUDENT IMPLEMENTATION NEEDED
            # 1. Iterate through every config in current_level.
            for config in current_level:
                left, state, right, parent_index = config
            # 2. Check if config is Accept (Stop and print success) [cite: 179]
                if state == self.accept_state:
                    print(f"String accepted in {depth} steps")
                    print(f"Transitions simulated: {transitionCount}")
                    accepted = True
                    self.print_trace_path(config, tree, depth)
                    return
            # 3. Check if config is Reject (Stop this branch only) [cite: 181]
                elif state == self.reject_state:
                    continue
            # 4. If not Accept/Reject, find valid transitions in self.transitions.
                current_symbol = right[0] if right else "_"
                valid_trans = self.get_transitions(state, (current_symbol,))
            # 5. If no explicit transition exists, treat as implicit Reject.
                if not valid_trans:
                    continue
                all_rejected = False
            # 6. Generate children configurations and append to next_level[cite: 148].
                for t in valid_trans:
                    nextState = t['next']
                    writeSymbol = t['write'][0]
                    move = t['move'][0]

                    transitionCount += 1

                    l, s, r = left, state, right

                    if move == 'L':
                        if r:
                            r = writeSymbol + r[1:]
                        else:
                            r = writeSymbol
                        if l:
                            r = l[-1] + r
                            l = l[:-1]
                        else:
                            r = "_" + r
                            
                    elif move == 'R':
                        if r:
                            r = writeSymbol + r[1:]
                        else:
                            r = writeSymbol
                        if r:
                            l = l + r[0] 
                            r = r[1:]
                        else:
                            l = l + "_"  
                            r = ""

                    elif move == 'S':
                        if r:
                            r = writeSymbol + r[1:]
                        else:
                            r = writeSymbol
                    
                    parent_idx = current_level.index(config)
                    next_level.append([l, nextState, r, parent_idx])
                        

            # Placeholder for logic:
            if not next_level and all_rejected:
                # TODO: Handle "String rejected" output [cite: 258]
                print(f"String rejected in {depth} steps")
                print(f"Transitions simulated: {transitionCount}")
                break

            tree.append(next_level)
            depth += 1

        if depth >= max_depth:
            print(f"Execution stopped after {max_depth} steps.")  # [cite: 259]



    def print_trace_path(self, final_node, tree, level):
        """
        Backtrack and print the path from root to the accepting node.
        Ref: Section 4.2 [cite: 165]
        """
        path = []
        current = final_node

        while current is not None:

            path.append((level, [current[:-1]]))

            parent_idx = current[-1]
            if parent_idx is None:
                break
            level -= 1
            current = tree[level][parent_idx]
        
        path.reverse()

        for level, pathNode in path:
            print()
            print(f"Level: {level}")
            for l, s, r, p in tree[level]:
                print(l, s, r)





