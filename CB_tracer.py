#This is a program that is meant to do the same thing as ntm_tracer.py but in a different manner
import csv

#read input csv file and convert to TM 
def parse_csv(file_path):
    with open(file_path, 'r') as file:
        csv_reader = csv.reader(file) #read data
        name = next(csv_reader)[0] 
        states = next(csv_reader)[0].split(',') 
        alphabet = next(csv_reader)[0].split(',') #sigma
        tape_symbols = next(csv_reader)[0].split(',') 
        start_state = next(csv_reader)[0] 
        accept_state = next(csv_reader)[0]
        reject_state = next(csv_reader)[0]

        transitions = {} #written as: state, character/symbol -> list of (next state, write char/symbol, direction )        
        for row in csv_reader:
            if not row: #extra check
                continue
            curr_state,char, next_state, write_char, move_dir= row
            transitions.setdefault((curr_state, char),[]).append((next_state, write_char, move_dir))
    return { 'name': name,
        'states':states,
        'alphabet': alphabet,
        'tape_symbols':tape_symbols,
        'start_state': start_state,
        'accept_state':accept_state,
        'reject_state': reject_state,
        'transitions': transitions, }

def ntm_tracer(machine, input_string, max_depth=None):
    print(f"Tracing NTM: {machine['name']} on input '{input_string}'")
    #initlization
    initial_config =(machine['start_state'], input_string, 0)
    tree= [[initial_config]]  #list of levels
    transitions =machine['transitions']
    accept_state = machine['accept_state']
    reject_state = machine['reject_state']

    total_transitions = 0
    curr_depth = 0
    transition_log = []

    while tree:
        if max_depth is not None and curr_depth > max_depth: #limitation check (max depth limit)
            print(f"Execution stopped after {max_depth} steps.")
            return None

        curr_level = tree.pop(0)
        next_level = []

        print(f"Level {curr_depth}:") #follo woutput instructions
        for state,tape, head in curr_level:
            
            if head >= 0:
                left = tape[:head]
            else:
                left = ""

            if head >= 0 and head < len(tape):
                head_char = tape[head]
            else:
                head_char = "_"

            if head + 1 < len(tape):
                right = tape[head + 1:]
            else:
                right = ""
            print(f"{left} {state} {head_char} {right}")

            #CHECK STATES
            if state == accept_state:
                print(f"\nString accepted in {curr_depth} steps")
                print(f"Total transitions: {total_transitions}")
                return curr_depth
            if state == reject_state:
                continue

            #determine current symbol
            if 0 <= head < len(tape):
                symbol = tape[head]
            else:
                symbol = "_"

#possible transitons for curr state and symbol
            possible = transitions.get((state, symbol), [])
            total_transitions += len(possible)

            #generate next configs
            for next_state, write_char, move_dir in possible:
                new_tape = list(tape)  #make tape modifiable  (coulf get neew configs)
                if 0 <= head < len(new_tape):
                    new_tape[head] = write_char
                else:
                    new_tape.append(write_char)

                #move head --usually we go right first--first check
                if move_dir == "R":
                    new_head = head + 1
                else:
                    new_head = head - 1                
                next_level.append((next_state, ''.join(new_tape), new_head))
                transition_log.append(f"({state}, {symbol}) -> ({next_state}, { write_char}, {move_dir})") 

        if not next_level:
            print(f"\nString rejected in {curr_depth} steps")
            print(f"Total transitions: {total_transitions}")
            return None

        tree.append(next_level)
        curr_depth += 1


#TBD test code/program
machine_input = input('Select file to run\n').strip() #user types
machine_input = f"input/{machine_input}" #search wuthin the input folder
max_depth = 15 #termination limit
machine = parse_csv(machine_input)
#ask user for the input string instead of reading it from the CSV
string = input("Enter the input string for this machine:\n").strip()

print(f"Running Simulation for: {string}")
result = ntm_tracer(machine, string, max_depth)
print(f"Solution Depth for '{string}': {result}")
