from laser_circuit import LaserCircuit
from circuit_for_testing import get_my_lasercircuit
from run import set_pulse_sequence
from sorter import sort_emitters_by_symbol
from emitter import Emitter

'''
Name:   JIANYI LU
SID:    520400438
Unikey: jilu4724

This test program checks if the set_pulse_sequence function is implemented
correctly.

You can modify this scaffold as needed (changing function names, parameters, 
or implementations...), however, DO NOT ALTER the code in circuit_for_testing 
file, which provides the circuit. The circuit can be retrieved by calling 
get_my_lasercircuit(), and it should be used as an argument for the 
set_pulse_sequence function when testing.

Make sure to create at least 6 functions for testing: 2 for positive cases,
2 for negative cases, and 2 for edge cases. Each function should take
different input files.

NOTE: Whenever we use ... in the code, this is a placeholder for you to
replace it with relevant code.
'''

def initialize(my_circuit, pulse_file_path) -> list[Emitter]:
    """
    Attempt to set pulse sequence to the circuit; initialize the circuit for further checking. 
    Performs the first check i.e. checking if the number of emitters are set up correctly.
    At the end, return a list of all emitters existing in the circuit. 

    Args:
    ---------------
    pulse_file_path - path to the pulse sequence file
    """
    
    #set pulse sequence using specifications given by pulse_sequence.in
    with open(pulse_file_path, 'r') as file:
        set_pulse_sequence(my_circuit, file)
    
    #get all the existing emitters in the circuit
    my_emitters: list[Emitter] = my_circuit.get_emitters()
    
    print('') #formatting
    
    #check if the amount of emitters added to circuit is correct
    print("Checking the amount of emitters added to circuit...")
    try:
        assert len(my_emitters) == 3
        print("Success! The correct number of emitters had been added.") #will only be printed if assertion passes
    except AssertionError:
        print("Error: exactly 3 emitters should be added to the circuit!")

    print('') #formatting
    
    return my_emitters


def positive_test_1(my_circuit: LaserCircuit, pulse_file_path: str) -> None: 
    '''
    Positive test case to verify the set_pulse_sequence function.
    
    When setup correctly, emitters must have these specifications. Format: (symbol frequency direction). 
    A 100000000000000 E
    B 3000 W
    C 10 N

    Parameters
    ----------
    my_circuit      - the circuit instance for testing
    pulse_file_path - path to the pulse sequence file
    '''
    my_emitters: list[Emitter] = initialize(my_circuit, pulse_file_path)
    
    #check each emitter
    print("Checking if each emitter has correct pulse sequence parameters according to its specification...")
    i, error_count = 0, 0
    while i < len(my_emitters):
        #check if every emitter has its pulse sequence set. If not, ignore the specification check.
        try:
            assert my_emitters[i].is_pulse_sequence_set() == True
        except AssertionError:
            error_count += 1
            print(f"Error: emitter '{my_emitters[i].get_symbol()}' didn't get its pulse sequence set!")        
            i += 1
            continue
            
        #check if the frequency set is correct according to the specifications described in docstring
        try:
            current_frequency: int = my_emitters[i].get_frequency()
            if my_emitters[i].get_symbol() == "A":
                target_frequency: int = 100000000000000
                assert current_frequency == target_frequency
            elif my_emitters[i].get_symbol() == "B":
                target_frequency: int = 3000
                assert current_frequency == target_frequency
            elif my_emitters[i].get_symbol() == "C":
                target_frequency: int = 10
                assert current_frequency == target_frequency
        except AssertionError:
            error_count += 1
            print(f"Error: emitter '{my_emitters[i].get_symbol()}' has been set to an incorrect frequency of {current_frequency}THz, while it's supposed to be {target_frequency}THz!")
            
        #check if the direction set is correct according to the specifications described in docstring
        try:
            current_direction: str = my_emitters[i].get_direction()
            if my_emitters[i].get_symbol() == "A":
                target_direction: str = 'E'
                assert current_direction == target_direction
            elif my_emitters[i].get_symbol() == "B":
                target_direction: str = 'W'
                assert current_direction == target_direction
            elif my_emitters[i].get_symbol() == "C":
                target_direction: str = 'N'
                assert current_direction == target_direction
        except AssertionError:
            error_count += 1
            print(f"Error: emitter '{my_emitters[i].get_symbol()}' has been set to an incorrect direction of {current_direction}, while it's supposed to be {target_direction}!")

        i += 1
        
    if error_count == 0: 
        print("(Positive test 1) Automatic test passed! All emitters have been set with correct pulse sequence parameters.\
 Now check the test_plan.md file for error message expectations.")
    else:
        print('') #formatting
        print(f"(Positive test 1) Encountered {error_count} error(s). Please read them and check your codes again.")
        
    print('')



def positive_test_2(my_circuit: LaserCircuit, pulse_file_path: str) -> None: 
    '''
    Positive test case to verify the set_pulse_sequence function.
    
    When setup correctly, emitters must have these specifications. Format: (symbol frequency direction). 
    A 1 W
    B 10 S
    C 100 S

    Parameters
    ----------
    my_circuit      - the circuit instance for testing
    pulse_file_path - path to the pulse sequence file
    '''
    
    my_emitters: list[Emitter] = initialize(my_circuit, pulse_file_path)
    
    #check each emitter
    print("Checking if each emitter has correct pulse sequence parameters according to its specification...")
    i, error_count = 0, 0
    while i < len(my_emitters):
        #check if every emitter has its pulse sequence set. If not, ignore the specification check.
        try:
            assert my_emitters[i].is_pulse_sequence_set() == True
        except AssertionError:
            error_count += 1
            print(f"Error: emitter '{my_emitters[i].get_symbol()}' didn't get its pulse sequence set!")        
            i += 1
            continue
            
        #check if the frequency set is correct according to the specifications described in docstring
        try:
            current_frequency: int = my_emitters[i].get_frequency()
            if my_emitters[i].get_symbol() == "A":
                target_frequency: int = 1
                assert current_frequency == target_frequency
            elif my_emitters[i].get_symbol() == "B":
                target_frequency: int = 10
                assert current_frequency == target_frequency
            elif my_emitters[i].get_symbol() == "C":
                target_frequency: int = 100
                assert current_frequency == target_frequency
        except AssertionError:
            error_count += 1
            print(f"Error: emitter '{my_emitters[i].get_symbol()}' has been set to an incorrect frequency of {current_frequency}THz, while it's supposed to be {target_frequency}THz!")
            
        #check if the direction set is correct according to the specifications described in docstring
        try:
            current_direction: str = my_emitters[i].get_direction()
            if my_emitters[i].get_symbol() == "A":
                target_direction: str = 'W'
                assert current_direction == target_direction
            elif my_emitters[i].get_symbol() == "B":
                target_direction: str = 'S'
                assert current_direction == target_direction
            elif my_emitters[i].get_symbol() == "C":
                target_direction: str = 'S'
                assert current_direction == target_direction
        except AssertionError:
            error_count += 1
            print(f"Error: emitter '{my_emitters[i].get_symbol()}' has been set to an incorrect direction of {current_direction}, while it's supposed to be {target_direction}!")

        i += 1
        
    if error_count == 0: 
        print("(Positive test 2) Automatic test passed! All emitters have been set with correct pulse sequence parameters.\
 Now check the test_plan.md file for error message expectations.")
    else:
        print('') #formatting
        print(f"(Positive test 2) Encountered {error_count} error(s). Please read them and check your codes again.")

    print('')



def negative_test_1(my_circuit: LaserCircuit, pulse_file_path: str) -> None: 
    '''
    Negative test case to verify the set_pulse_sequence function.
    Tests the symbol parameter. 
    
    None of the emitters should be set up successfully with the specifications below: 
    R0 10 S
    10 10 S
    ?? 10 S
    AA 10 S
    AB 10 S

    Parameters
    ----------
    my_circuit      - the circuit instance for testing
    pulse_file_path - path to the pulse sequence file
    '''
    
    my_emitters: list[Emitter] = initialize(my_circuit, pulse_file_path)
        
    #check each emitter
    print("Checking if invalid pulse sequence symbols were set up...")
    i, error_count = 0, 0
    while i < len(my_emitters):
        #none of the emitters should have their pulse sequence set because the symbols given were all invalid.
        try:
            assert my_emitters[i].is_pulse_sequence_set() == False
        except AssertionError:
            error_count += 1
            print(f"Error: pulse sequence for emitter '{my_emitters[i].get_symbol()}' should not be set since the symbol given was invalid!")        
        i += 1
        
    if error_count == 0: 
        print("(Negative test 1) Automatic test passed! Your set_pulse_sequence function didn't set up emitters with invalid symbols.\
 Now check the test_plan.md file for error message expectations.")
    else:
        print('') #formatting
        print(f"(Negative test 1) Encountered {error_count} error(s). Please read them and check your codes again.")

    print('')



def negative_test_2(my_circuit: LaserCircuit, pulse_file_path: str) -> None: 
    '''
    Negative test case to verify the set_pulse_sequence function.
    Tests the frequency parameter. 
    
    None of the emitters should be set up successfully with the specifications below: 
    A 0 W
    B -1 S
    C 4.5 E
    C -4.5 E

    Parameters
    ----------
    my_circuit      - the circuit instance for testing
    pulse_file_path - path to the pulse sequence file
    '''
    
    my_emitters: list[Emitter] = initialize(my_circuit, pulse_file_path)
    
    #check each emitter
    print("Checking if invalid pulse sequence frequencies were set up...")
    i, error_count = 0, 0
    while i < len(my_emitters):
        #none of the emitters should have their pulse sequence set because the frequencies given were all invalid.
        try:
            assert my_emitters[i].is_pulse_sequence_set() == False
        except AssertionError:
            error_count += 1
            print(f"Error: pulse sequence for emitter '{my_emitters[i].get_symbol()}' should not be set since the frequency given was invalid!")        
        i += 1
        
    if error_count == 0: 
        print("(Negative test 2) Automatic test passed! Your set_pulse_sequence function didn't set up emitters with invalid frequencies.\
 Now check the test_plan.md file for error message expectations.")
    else:
        print('') #formatting
        print(f"(Negative test 2) Encountered {error_count} error(s). Please read them and check your codes again.")

    print('')

def negative_test_3(my_circuit: LaserCircuit, pulse_file_path: str) -> None: 
    '''
    Negative test case to verify the set_pulse_sequence function.
    Tests the direction parameter. 
    
    None of the emitters should be set up successfully with the specifications below: 
    A 10 West
    B 10 s
    C 10 10
    C 10 ?!

    Parameters
    ----------
    my_circuit      - the circuit instance for testing
    pulse_file_path - path to the pulse sequence file
    '''
    
    my_emitters: list[Emitter] = initialize(my_circuit, pulse_file_path)
        
    #check each emitter
    print("Checking if invalid pulse sequence directions were set up...")
    i, error_count = 0, 0
    while i < len(my_emitters):
        #none of the emitters should have their pulse sequence set because the directions given are all invalid.
        try:
            assert my_emitters[i].is_pulse_sequence_set() == False
        except AssertionError:
            error_count += 1
            print(f"Error: pulse sequence for emitter '{my_emitters[i].get_symbol()}' should not be set since the direction given was invalid!")        
        i += 1
        
    if error_count == 0: 
        print("(Negative test 3) Automatic test passed! Your set_pulse_sequence function didn't set up emitters with invalid directions.\
 Now check the test_plan.md file for error message expectations.")
    else:
        print('') #formatting
        print(f"(Negative test 3) Encountered {error_count} error(s). Please read them and check your codes again.")

    print('')
    
    

def edge_test_1(my_circuit: LaserCircuit, pulse_file_path: str) -> None: 
    '''
    Edge test case to verify the set_pulse_sequence function.
    Tests how the set_pulse_sequence respond to empty inputs at different positions.
    
    None of the emitters should be set up successfully with the specifications below: 
    A    W
    A 10
    10 W
        
    A     
    10  
        W

    Parameters
    ----------
    my_circuit      - the circuit instance for testing
    pulse_file_path - path to the pulse sequence file
    '''

    my_emitters: list[Emitter] = initialize(my_circuit, pulse_file_path)
        
    #check each emitter
    print("Checking if invalid pulse sequence directions were set up...")
    i, error_count = 0, 0
    while i < len(my_emitters):
        #none of the emitters should have their pulse sequence set because the parameters given were incomplete.
        try:
            assert my_emitters[i].is_pulse_sequence_set() == False
        except AssertionError:
            error_count += 1
            print(f"Error: pulse sequence for emitter '{my_emitters[i].get_symbol()}' should not be set since the parameters given were incomplete!")        
        i += 1
        
    if error_count == 0: 
        print("(Edge test 1) Automatic test passed! Your set_pulse_sequence function didn't set up emitters with empty parameters.\
 Now check the test_plan.md file for error message expectations.")
    else:
        print('') #formatting
        print(f"(Edge test 1) Encountered {error_count} error(s). Please read them and check your codes again.")

    print('')



def edge_test_2(my_circuit: LaserCircuit, pulse_file_path: str) -> None: 
    '''
    Edge test case to verify the set_pulse_sequence function.
    Tests how the set_pulse_sequence respond to no input.
    
    None of the emitters should be set up successfully because the file has no content. 

    Parameters
    ----------
    my_circuit      - the circuit instance for testing
    pulse_file_path - path to the pulse sequence file
    '''

    my_emitters: list[Emitter] = initialize(my_circuit, pulse_file_path)
        
    #check each emitter
    print("Checking if invalid pulse sequence directions were set up...")
    i, error_count = 0, 0
    while i < len(my_emitters):
        #none of the emitters should have their pulse sequence set because the input file was empty.
        try:
            assert my_emitters[i].is_pulse_sequence_set() == False
        except AssertionError:
            error_count += 1
            print(f"Error: pulse sequence for emitter '{my_emitters[i].get_symbol()}' should not be set since the input file was empty!")        
        i += 1
        
    if error_count == 0: 
        print("(Edge test 2) Automatic test passed! Your set_pulse_sequence function didn't set up emitters with no input.\
 Now check the test_plan.md file for error message expectations.")
    else:
        print('') #formatting
        print(f"(Edge test 2) Encountered {error_count} error(s). Please read them and check your codes again.")

    print('')


if __name__ == '__main__':
    # Run each function for testing
    positive_test_1(get_my_lasercircuit(), '/home/input/pos_pulse_sequence_1.in')
    positive_test_2(get_my_lasercircuit(), '/home/input/pos_pulse_sequence_2.in')
    negative_test_1(get_my_lasercircuit(), '/home/input/neg_pulse_sequence_1.in')
    negative_test_2(get_my_lasercircuit(), '/home/input/neg_pulse_sequence_2.in')
    negative_test_3(get_my_lasercircuit(), '/home/input/neg_pulse_sequence_3.in')
    edge_test_1(get_my_lasercircuit(), '/home/input/edge_pulse_sequence_1.in')
    edge_test_2(get_my_lasercircuit(), '/home/input/edge_pulse_sequence_2.in')