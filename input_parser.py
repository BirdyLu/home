from emitter import Emitter
from receiver import Receiver
from mirror import Mirror
from typing import Optional, Union


'''
Name:   Jianyi Lu
SID:    520400438
Unikey: jilu4724

input_parser - A module that parses the inputs of the program. 
We define parsing as checking the validity of what has been entered 
to determine if it's valid. If it's not valid, an appropriate message 
should be printed. Whenever we retrieve input in the program, we 
should be using functions from this module to validate it.

You are free to add more functions, as long as you aren't modifying the
existing scaffold.
'''

#board_displayer.py & laser_circuit.py
def parse_size(user_input: str) -> Optional[tuple[int, int]]:
    # only requires implementation once you reach GET-MY-INPUTS
    '''
    Checks if user_input is a valid input for the size of the circuit board by
    performing the following checks:
    1)  user_input contains exactly 2 tokens. If there are 2 tokens, we
        interpret the first token as width and the second token as height for
        the remaining checks.
    2)  width is an integer.
    3)  height is an integer.
    4)  width is greater than zero.
    5)  height is greater than zero.

    Parameters
    ----------
    user_input - the user input for the circuit's board size

    Returns
    -------
    If all checks pass, returns a tuple containing the width and height of
    the circuit board.
    Else, if at any point a check fails, prints an error message stating the cause
    of the error and returns None, skipping any further checks.

    Example 1:
    >>> size = parse_size('18 0')
    Error: height must be greater than zero
    >>> size
    None

    Example 2:
    >>> size = parse_size('18 6')
    >>> size
    (18, 6)
    '''
    
    user_input: list = user_input.split()
    
    #check if it's 2 parameters
    if len(user_input) != 2: 
        print("Error: <width> <height>")
        return
    
    width: str = user_input[0]
    height: str = user_input[1]

    #disable any non-integer coordinate
    try:
        width: int = int(width)
    except Exception:
        print("Error: width is not an integer")
        return
    try:
        height: int = int(height)
    except Exception:
        print("Error: height is not an integer")
        return
        
    #disable any non-positive number
    if width <= 0:
        print("Error: width must be greater than zero")
        return
    if height <= 0:
        print("Error: height must be greater than zero")
        return
    
    return width, height

#emitter.py
def parse_emitter(user_input: str) -> Optional[Emitter]:
    # only requires implementation once you reach GET-MY-INPUTS
    '''
    Checks if user_input is a valid input for creating an emitter by
    performing the following checks in order for any errors: 
        1)  user_input contains exactly 3 tokens. If there are 3 tokens, we 
            interpret the first token as symbol, the second token as x and the 
            third token as y for the remaining checks.
        2)  symbol is a character between 'A' to 'J'. 
        3)  x is an integer.
        4)  y is an integer.
        5)  x is greater than 0.
        6)  y is greater than 0

    Parameters
    ----------
    user_input - the user input for creating a new emitter

    Returns
    -------
    If all checks pass, returns a new Emitter instance with the specified
    symbol, x and y position set.
    Else, if at any point a check fails, prints an error message stating the cause
    of the error and returns None, skipping any further checks.
    '''
    
    #split & remove all empty elements in list
    user_input = user_input.split()

    #check input format
    if len(user_input) != 3:
        print("Error: <symbol> <x> <y>")
        return

    symbol: str = user_input[0]
    x: str = user_input[1]
    y: str = user_input[2]

    if len(symbol) != 1 or ord(symbol) < 65 or ord(symbol) > 74: 
        print("Error: symbol is not between 'A'-'J'")
        return
    
    #disable any non-integer coordinate
    try:
        x = int(x)
    except ValueError:
        print("Error: x is not an integer")
        return
    try:
        y = int(y)
    except ValueError:
        print("Error: y is not an integer")
        return

    #disable any negative number but can equal to 0 since 0 is a valid coordinate
    if x < 0:
        print("Error: x cannot be negative")
        return 
    if y < 0:
        print("Error: y cannot be negative")
        return   
    
    return Emitter(symbol, x, y)

#receiver.py
def parse_receiver(user_input: str) -> Optional[Receiver]:
    # only requires implementation once you reach GET-MY-INPUTS
    '''
    Identical to parse_emitter, with the ONLY differences being
    that the symbol must be between 'R0' to 'R9', and that a new Receiver
    instance is returned if all checks pass.

    Parameters
    ----------
    user_input - the user input for creating a new receiver

    Returns
    -------
    If all checks pass, returns a new Receiver instance with the specified
    symbol, x and y position set.
    Else, if at any point a check fails, prints an error message stating the cause
    of the error and returns None, skipping any further checks.    
    '''

    #split & remove all empty elements in list
    user_input = user_input.split()

    #check input format
    if len(user_input) != 3:
        print("Error: <symbol> <x> <y>")
        return
    
    symbol: str = user_input[0]
    x: str = user_input[1]
    y: str = user_input[2]
    
    if len(symbol) != 2 or symbol[0] != 'R' or ord(symbol[1]) < 48 or ord(symbol[1]) > 57: 
        print("Error: symbol is not between R0-R9")
        return
    #disable any non-integer coordinate
    try:
        int(x)
    except ValueError:
        print("Error: x is not an integer")
        return
    try:
        int(y)
    except ValueError:
        print("Error: y is not an integer")
        return

    #disable any negative number but can equal to 0 since 0 is a valid coordinate
    cond1_not = int(x) < 0
    cond2_not = int(y) < 0
    if cond1_not:
        print("Error: x cannot be negative")
        return 
    if cond2_not:
        print("Error: y cannot be negative")
        return
    return Receiver(symbol, int(x), int(y))


def parse_pulse_sequence(line: str) -> Optional[tuple[str, int, str]]:
    # only requires implementation once you reach RUN-MY-CIRCUIT
    '''
    Checks if line is valid for setting the pulse sequence of an emitter by
    performing the following checks in order for any errors:
    1)  line contains exactly 3 tokens.
        If there are 3 tokens, we interpret the first token as symbol, the
        second token as frequency and the third token as direction for the
        remaining checks.
    2)  symbol is a character between 'A' to 'J'.
    3)  frequency is an integer.
    4)  frequency is greater than zero.
    5)  direction is either 'N', 'E', 'S' or 'W'.

    Parameters
    ----------
    user_input - the user input for setting the pulse sequence of an emitter

    Returns
    -------
    If all checks pass, returns a tuple containing the specified symbol,
    frequency and direction which can be used for setting the pulse sequence
    of the emitter.
    Else, if at any point a check fails, prints an error message stating the cause
    of the error and returns None, skipping any further checks.    
    '''

    #split & remove all empty elements in list
    user_input = line.split()

    #check input format
    if len(user_input) != 3:
        print("Error: <symbol> <frequency> <direction>")
        return
    
    symbol: str = user_input[0]
    frequency: str = user_input[1]
    direction: str = user_input[2]
    
    if len(symbol) != 1 or ord(symbol) < 65 or ord(symbol) > 74: 
        print("Error: symbol is not between A-J")
        return

    #disable any non-integer coordinate
    try:
        int(frequency)
    except ValueError:
        print("Error: frequency is not an integer.")
        return

    #disable any non-positive number
    if int(frequency) <= 0: 
        print("Error: frequency must be greater than zero")
        return

    #check direction
    if direction != 'N' and direction != 'E' and direction != 'S' and direction != 'W':
        print("Error: direction must be 'N', 'E', 'S' or 'W'")
        return

    return symbol, int(frequency), direction

#mirror.py
def parse_mirror(user_input: str) -> Optional[Mirror]:
    # only requires implementation once you reach ADD-MY-MIRRORS
    '''
    Checks if user_input is a valid input for creating a mirror by performing
    the following checks in order for any errors:
    1)  user_input contains exactly 3 tokens. If there are 3 tokens, we
        interpret the first token  as symbol, the second token as x and the
        third token as y for the remaining checks.
    2)  symbol is either '/', '\', '>', '<', '^', or 'v'.
    3)  x is an integer. 
    4)  y is an integer. 
    5)  x is greater than 0. 
    6)  y is greater than 0. 

    Parameters
    ----------
    user_input - the user input for creating a mirror

    Returns
    -------
    If all checks pass, returns a new Mirror instance with the specified
    symbol, x and y position set.
    Else, if at any point a check fails, prints an error message stating the cause
    of the error and returns None, skipping any further checks.    
    '''

    #split & remove all empty elements in list
    user_input = user_input.split()

    #check input format
    if len(user_input) != 3:
        print("Error: <symbol> <x> <y>")
        return
    
    symbol: str = user_input[0]
    x: str = user_input[1]
    y: str = user_input[2]
    
    if len(symbol) != 1 or (symbol != '/' and symbol != '\\' and symbol != '>' and symbol != '<' and symbol != '^' and symbol != 'v'): 
        print("Error: symbol must be '/', '\\', '>', '<', '^' or 'v'")
        return
    
    #disable any non-integer coordinate
    try:
        int(x)
    except ValueError:
        print("Error: x is not an integer")
        return
    try:
        int(y)
    except ValueError:
        print("Error: y is not an integer")
        return
    
    #disable any negative number
    cond1_not = int(x) < 0
    cond2_not = int(y) < 0
    if cond1_not:
        print("Error: x cannot be negative")
        return 
    if cond2_not:
        print("Error: y cannot be negative")
        return
    return Mirror(symbol, int(x), int(y))

def main():
    parse_emitter('')
    while True:
        input0 = input("TEST: (size, emitter, receiver, pulse, mirror)\n> ")
        if input0 == 'end':
            return
        if input0 == "size":
            while True:
                input1 = input(">>> ")
                if input1 == "end":
                    break
                parse_size(input1)
        elif input0 == "emitter":
            while True:
                input1 = input(">>> ")
                if input1 == "end":
                    break
                parse_emitter(input1)
        elif input0 == "receiver":
            while True:
                input1 = input(">>> ")
                if input1 == "end":
                    break
                parse_receiver(input1)
        elif input0 == "pulse":
            while True:
                input1 = input(">>> ")
                if input1 == "end":
                    break
                parse_pulse_sequence(input1)
        elif input0 == "mirror":
            while True:
                input1 = input(">>> ")
                if input1 == "end":
                    break
                parse_mirror(input1)

    
if __name__ == "__main__":
    main()