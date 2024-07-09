import sys
import input_parser
from emitter import Emitter
from receiver import Receiver
from mirror import Mirror
from laser_circuit import LaserCircuit
from typing import Optional, Union

'''
Name:   Jianyi Lu
SID:    520400438
Unikey: jilu4724

run - Runs the entire program. It needs to take in the inputs and process them
into setting up the circuit. The user can specify optional flags to perform
additional steps, such as -RUN-MY-CIRCUIT to run the circuit and -ADD-MY-MIRRORS
to include mirrors in the circuit.

You are free to add more functions, as long as you aren't modifying the
existing scaffold.
'''


def is_run_my_circuit_enabled(args: list[str]) -> bool:
    '''
    Returns whether or not '-RUN-MY-CIRCUIT' is in args.
    
    Parameters
    ----------
    args - the command line arguments of the program
    '''
    found = False
    i=0
    while i<len(args):
        if args[i] == '-RUN-MY-CIRCUIT':
            found = True
            return found
        i+=1
    return found

def is_add_my_mirrors_enabled(args: list[str]) -> bool:
    # only requires implementation once you reach ADD-MY-MIRRORS
    '''
    Returns whether or not '-ADD-MY-MIRRORS' is in args.
    
    Parameters
    ----------
    args - the command line arguments of the program
    '''
    found = False
    i=0
    while i<len(args):
        if args[i] == '-ADD-MY-MIRRORS':
            found = True
            return found
        i+=1
    return found


def initialise_circuit() -> LaserCircuit:
    '''
    Gets the inputs for the board size, emitters and receivers and processes
    it to create a LaserCircuit instance and return it. You should be using
    the functions you have implemented in the input_parser module to handle
    validating each input.

    Returns
    -------
    A LaserCircuit instance with a width and height specified by the user's
    inputted size. The circuit should also include each emitter and receiver
    the user has inputted.
    '''
    print("Creating circuit board...")
    
    #infinitely asking for board size until valid size is given
    while True:
        try: 
            user_input_board_size = input("> ")
        except EOFError:
            break
        try:
            parsed_size: Optional[tuple[int, int]] = input_parser.parse_size(user_input_board_size)
        except Exception: 
            parsed_size: Optional[tuple[int, int]] = None
        if parsed_size:
            break

    new_circuit: LaserCircuit = LaserCircuit(parsed_size[0], parsed_size[1])
    print(f"{parsed_size[0]}x{parsed_size[1]} board created.")

    #add emitters
    print("\nAdding emitter(s)...")
    added_emitters: list[Emitter] = []

    i=0
    while i < 10:
        try: 
            user_input = input("> ")
            if user_input == "END EMITTERS":
                print(f"{len(added_emitters)} emitter(s) added.\n")
                break
        except EOFError:
            print(f"{len(added_emitters)} emitter(s) added.\n")
            break

        try: 
            parsed_emitter: Optional[Emitter] = input_parser.parse_emitter(user_input) #validate input
        except Exception:
            parsed_emitter: Optional[Emitter] = None
        try: 
            if parsed_emitter:
                has_added_emitter: bool = new_circuit.add_emitter(parsed_emitter) #try to add emitter to circuit
            else: 
                has_added_emitter: bool = False
        except Exception: 
            has_added_emitter: bool = False
        
        if has_added_emitter:
            added_emitters.append(parsed_emitter)
            i+=1 #only increment if emitter was successfully added
        
        if i==10: 
            print(f"{len(added_emitters)} emitter(s) added.\n")
            break

    #add receivers
    print("Adding receiver(s)...")
    added_receivers: list[Receiver] = []
    
    i=0
    while i < 10:
        try: 
            user_input = input("> ")
            if user_input == "END RECEIVERS":
                print(f"{len(added_receivers)} receiver(s) added.\n")
                break
        except EOFError:
            print(f"{len(added_receivers)} receiver(s) added.\n")
            break

        
        try: 
            parsed_receiver: Optional[Receiver] = input_parser.parse_receiver(user_input) #validate input
        except Exception: 
            parsed_receiver: Optional[Receiver] = None
        try: 
            if parsed_receiver:
                has_added_receiver: bool = new_circuit.add_receiver(parsed_receiver) #try to add receiver to circuit
            else: 
                has_added_receiver: bool = False
        except Exception: 
            has_added_receiver: bool = False
        
        if has_added_receiver:
            added_receivers.append(parsed_receiver)
            i+=1 #only increment if receiver was successfully added
        
        if i==10: 
            print(f"{len(added_emitters)} receiver(s) added.\n")
            break
            
    return new_circuit


def set_pulse_sequence(circuit: LaserCircuit, file_obj) -> None:
    '''
    Handles setting the pulse sequence of the circuit. 
    The lines for the pulse sequence will come from the a file named
    /home/input/<file_name>.in. 
    You should be using the functions you have implemented in the input_parser module 
    to handle validating lines from the file.

    Parameter
    ---------
    circuit - The circuit to set the pulse sequence for.
    file_obj - A file like object returned by the open()
    '''
    
    #get all unset emitters
    unset_emitter_symbols: list[str] = []
    
    i=0
    while i<len(circuit.emitters):
        if not circuit.emitters[i].is_pulse_sequence_set():
            unset_emitter_symbols.append(circuit.emitters[i].get_symbol())
        i+=1

    #set pulse sequence for each emitter
    print("Setting pulse sequence...")
    #read all lines from file
    lines: list[str] = file_obj.readlines()
    if len(lines) == 0:
        print("Pulse sequence set.")
        return

    #process each line
    l=0
    while l<len(lines):
        lines[l] = lines[l].strip() #remove \n
        
        #print line information
        str_unset_emitter_symbols: str = ', '.join(unset_emitter_symbols)
        print(f"-- ({str_unset_emitter_symbols})")
        print(f"Line {l+1}: {lines[l]}")
        
        #parse the line
        try: 
            parsed_pulse_sequence: Optional[tuple[str, int, str]] = input_parser.parse_pulse_sequence(lines[l])
        except Exception:
            parsed_pulse_sequence: Optional[tuple[str, int, str]] = None
        
        #check if input from line is valid. If not, move to next line
        if not parsed_pulse_sequence: 
            l+=1
            continue
        
        #search through all existing emitters in circuit
        found = False #for each line, assume it is not among existing emitters
        i=0
        while i<len(circuit.emitters): 
            if circuit.emitters[i].get_symbol() == parsed_pulse_sequence[0]:
                found = True
                if not circuit.emitters[i].is_pulse_sequence_set():
                    circuit.emitters[i].set_pulse_sequence(parsed_pulse_sequence[1], parsed_pulse_sequence[2])
                    unset_emitter_symbols.pop(unset_emitter_symbols.index(circuit.emitters[i].get_symbol()))
                else: 
                    print(f"Error: emitter '{circuit.emitters[i].get_symbol()}' already has its pulse sequence set")
                break
            i+=1
            
        #if the pulse sequence described in this line isn't found among existing emitters
        if not found:
            print(f"Error: emitter '{parsed_pulse_sequence[0]}' does not exist")
        
        if len(unset_emitter_symbols) == 0:
            print("Pulse sequence set.")
            return
        
        l+=1

def add_mirrors(circuit: LaserCircuit) -> None:
    '''
    Handles adding the mirrors into the circuit. You should be using the
    functions you have implemented in the input_parser module to handle
    validating each input. There are no limit on the mirrors users can enter. 
    
    Parameters
    ----------
    circuit - the laser circuit to add the mirrors into
    '''
    print("Adding mirror(s)...")
    added_mirrors: list[Mirror] = []

    #infinitely ask for mirrors
    while True:
        try:
            user_input = input("> ")
            if user_input == "END MIRRORS":
                print(f"{len(added_mirrors)} mirror(s) added.")
                break
        except EOFError:
            print(f"{len(added_mirrors)} mirror(s) added.")
            break
        
        try: 
            parsed_mirror: Optional[Mirror] = input_parser.parse_mirror(user_input) #validate input
        except Exception:
            parsed_mirror: Optional[Mirror] = None
        try:
            has_added_mirror: bool = circuit.add_mirror(parsed_mirror) #try to add receiver to circuit
        except Exception:
            has_added_mirror: bool = False
        
        if has_added_mirror:
            added_mirrors.append(parsed_mirror)

def main(args: list[str]) -> None:
    # only requires implementation once you reach GET-MY-INPUTS
    # will require extensions in RUN-MY-CIRCUIT and ADD-MY-MIRRORS
    '''
    Responsible for running all code related to the program.

    Parameters
    ----------
    args - the command line arguments of the program
    '''

    new_circuit = initialise_circuit()
    
    if is_add_my_mirrors_enabled(args):
        print("<ADD-MY-MIRRORS FLAG DETECTED!>\n")
        add_mirrors(new_circuit)
        print('')
        
    new_circuit.print_board()
    print('')
        
    if is_run_my_circuit_enabled(args):
        print("<RUN-MY-CIRCUIT FLAG DETECTED!>\n")
        try:
            with open("input/pulse_sequence.in", "r") as file:
                set_pulse_sequence(new_circuit, file)
                new_circuit.run_circuit()
                return
        except FileNotFoundError:
            print("Error: -RUN-MY-CIRCUIT flag detected but /home/input/pulse_sequence.in does not exist")
            return

if __name__ == '__main__':
    '''
    Entry point of program. We pass the command line arguments to our main
    program. We do not recommend modifying this.
    '''
    main(sys.argv)
