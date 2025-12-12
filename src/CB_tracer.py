#This is a program that is meant to do the same thing as ntm_tracer.py but in a different manner
import csv

#read input csv file and convert to TM 
def parse_csv(file_path):
    with open(file_path, 'r') as file:
        csv_reader = csv.reader(file) #read data
        name = next(csv_reader)[0] 
        string_read = next(csv_reader)[0] 
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
        'string_read': string_read,
        'states':states,
        'alphabet': alphabet,
        'tape_symbols':tape_symbols,
        'start_state': start_state,
        'accept_state':accept_state,
        'reject_state': reject_state,
        'transitions': transitions, }

def ntm_tracer(machine, input_string, max_depth=None): #follows same logic as ntm_trace.py program given though I just didnt understand the 'cite' comments
    #perform BFS of NTM
    print(f"Tracing NTM: {machine['name']} on input '{input_string}'")
    initial_config = (machine['start_state'], input_string, 0) #DIFFERERNT from given prog. (state, input_string, head_location)
    tree = [[initial_config]] #list of list of configs
    accept_state = machine['accept_state']
    reject_state = machine['reject_state']
    transitions = machine ['transitions']

    #Vars that will change after going through tree
    total_configs, total_transitions = 0
    accept_configs, reject_configs =0
    curr_depth =0
    transition_log = []
    branch_points =0 #keep track of how many states had more than 1 possible transition (Nondeterminisitc bracnhign points/level of nondeterminism)


    while tree: #will need to iterate throuhg eavery configuration
        curr_level = tree.pop(0)
        next_level = []
        print(f"Depth {curr_depth}, Current Level:  {len(curr_level)} configurations")
        for state, tape, head_position in curr_level:
            total_configs +=1 #keep track of processed configs
            #iterate through level and check if accept/reject to proceed
            if state ==accept_state:
                accept_configs+=1
                print("\n String is accepted!")
                print(f"Accepted at depth: {curr_depth}")
                print(f"Total configurations: {total_configs}")
                print(f"Accepted configurations: {accept_configs}")
                print(f"Rejected configurations: {reject_configs}")
                print(f"Level of nondeterminism: {total_transitions/(branch_points or 1):.2f}")
                print("\nTransition Log:")
                for t in transition_log:
                    print(" ", t)
                return curr_depth

            if state ==reject_state:
                reject_configs +=1
                continue 
            #determine current read symbol
            if 0 <= head_position <len(tape):
                head_char = tape[head_position]   
            else:
                head_char = "_"   #blank if go beyond tape       

            possible = transitions.get((state,head_char),[]) #possible transitions for the state and symbol/char
            # count nondeterminism 
            if len(possible) >1:
                branch_points += 1
            #generate nxt configuraions for THIS config
            #TBD
            for next_state, write_char, move_direction in possible:
                #initilaize modifiable tape list
                tape_list = list(tape)

                #write symbol

                #move head L or R

                #convert tape back to strign

                #save new config
                #log the transiton
                

            

    #TBD test code/program
    machine_input = input('Select file to run\n') #user types
    m = f'input/{machine_input}'
    max_depth = 10
    machine = parse_csv(machine_input)




