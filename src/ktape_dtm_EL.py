from src.helpers.turing_machine import TuringMachineSimulator

## Example Input
# CopyMachine,2           a two element list consisting of the Name of machine followed by a number k
#                          - where k is the number of tapes in this machine
# start,copy,done         List of state names for Q
# a,b,c                   List of characters from Σ
# a,b,c,_                 List of characters from Γ
# start                   start state
# done                    accept state
# reject                  reject state

# start,*,_,copy,*,*,S,S
# copy,a,_,copy,a,a,R,R
# copy,b,_,copy,b,b,R,R
# copy,c,_,copy,c,c,R,R
# copy,_,_,done,_,_,S,S


# ==========================================
# PROGRAM 2: k-tape DTM [cite: 268]
# ==========================================
class KTape_DTM(TuringMachineSimulator):
    def run(self, input_string, max_steps):
        """
        Simulates a deterministic k-tape machine.
        """
        print(f"Running k-tape DTM: {self.machine_name}")
        print(f"Initial string: {input_string}")

        # Initialize k tapes. Tape 1 has input, others are blank.
        k = self.num_tapes # get number of tapes
        tapes = []
        first_tape = list(input_string) if input_string else ['_']
        tapes.append(first_tape)        
        for _ in range(k-1):
            tapes.append(['_']) # make all other tapes blank besides first one
            
        # Track head positions for k tapes.
        head = [0 for _ in range(k)]

        state = self.start_state # start state
        step = 0

        while step < max_steps:
            # TODO: STUDENT IMPLEMENTATION NEEDED
            # 1. Read characters under all k heads.
            read_chars = []
            for i in range(k):
                head_tape = head[i]
                
                read_chars.append(tapes[i][head_tape])

            # Accept check
            if state == self.accept_state:
                print()
                print(f"String accepted after {step} steps")
                return
            if state == self.reject_state:
                print(f"String rejected after {step} steps")

            # 2. Find matching transition (Look for exact match first, then Wildcard *) [cite: 275-277].
            transitions = self.get_transitions(state, tuple(read_chars))
            if not transitions:
                print(f"String rejected after {step} steps.")
                return

            transition = transitions[0]
            next_state = transition["next"]
            write_char = transition["write"]
            moves = transition["move"]

            # 3. Update tapes, move heads, change state.
            for i in range(k):
                head_tape = head[i]

                # write symbol
                if write_char[i] != "*": 
                    tapes[i][head_tape] = write_char[i]

                # move head, for S just stay so no changes
                if moves[i] == "R":
                    head[i] += 1
                elif moves[i] == "L":
                    head[i] -= 1

                # after moving, ensure tape in bounds
                new_head = head[i]
                if new_head <0:
                    tapes[i].insert(0, '_')
                    head[i] = 0
                elif new_head >= len(tapes[i]):
                    tapes[i].append('_')

            # 4. Print state of tapes as per Output requirements [cite: 281-282].
            print(" ")
            print(f"Transition {step}: State={state}")
            for i in range(k):
                head_tape = head[i]
                tape_string = ''.join(tapes[i])
                left = tape_string[:head_tape]
                head_char = tape_string[head_tape]
                right = tape_string[head_tape+1:]
                print(f"Tape {i+1}: {left}_{head_char}{right}")

            # Update state and continue
            state = next_state
            step += 1