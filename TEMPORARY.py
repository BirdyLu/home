def is_finished(photons: list) -> bool:
    # only requires implementation once you reach RUN-MY-CIRCUIT
    '''
    Returns whether or not this circuit has finished running. The
    circuit is finished running if every photon in the circuit has been
    absorbed.

    Returns
    -------
    True if the circuit has finished running or not, else False.
    '''

    i=0
    while i<len(photons):
        if not photons[i].is_absorbed():
            return False
        i+=1
    return True

test = []
print(is_finished(test))