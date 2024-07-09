import sorter
from emitter import Emitter
from receiver import Receiver
from photon import Photon
from mirror import Mirror
from board_displayer import BoardDisplayer
from typing import Optional, Union


'''
Name:   JIANYI LU
SID:    520400438
Unikey: jilu4724

LaserCircuit - Responsible for storing all the components of the circuit and
handling the computation of running the circuit. It's responsible for delegating 
tasks to the specific components e.g. making each emitter emit a photon, getting 
each photon to move and interact with components, etc. In general, this class is
responsible for handling any task related to the circuit.

You are free to add more attributes and methods, as long as you aren't 
modifying the existing scaffold.
'''

#define the type Entity
entity = Union[Emitter, Receiver, Photon, Mirror, None]

class LaserCircuit:


    def __init__(self, width: int, height: int):
        '''        
        Initialise a LaserCircuit instance given a width and height. All 
        lists of components and photons are empty by default.
        board_displayer is initialised to a BoardDisplayer instance. clock is
        0 by default.

        emitters:        list[Emitter]  - all emitters in this circuit
        receivers:       list[Receiver] - all receivers in this circuit
        photons:         list[Photon]   - all photons in this circuit
        mirrors:         list[Mirror]   - all mirrors in this circuit
        width:           int            - the width of this circuit board
        height:          int            - the height of this circuit board
        board_displayer: BoardDisplayer - helper class for storing and 
                                        displaying the circuit board
        clock:           int            - a clock keeping track of how many 
                                        nanoseconds this circuit has run for

        Parameters
        ----------
        width  - the width to set this circuit board to
        height - the width to set this circuit board to
        '''
        self.width: int = width
        self.height: int = height

        self.emitters: list[Emitter] = []
        self.receivers: list[Receiver] = []
        self.photons: list[Photon] = []
        self.mirrors: list[Mirror] = []
        self.board_displayer: BoardDisplayer = BoardDisplayer(self.width, self.height)
        self.clock: int = 0

    def emit_photons(self) -> None:
        # only requires implementation once you reach RUN-MY-CIRCUIT
        '''
        Gets each emitter in this circuit's list of emitters to emit a photon.
        The photons emitted should be added to this circuit's photons list.
        '''
        i=0
        while i<len(self.get_emitters()):
            emitted_photon = self.emitters[i].emit_photon()
            self.photons.append(emitted_photon)
            i+=1

    def is_finished(self) -> bool:
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
        while i<len(self.photons):
            if not self.photons[i].is_absorbed():
                return False
            i+=1
        return True

    def print_emit_photons(self) -> None:
        # only requires implementation once you reach RUN-MY-CIRCUIT
        '''
        Prints the output for each emitter emitting a photon.
        
        It will also need to write the output into a
        /home/output/emit_photons.out output file. 
        
        You can assume the /home/output/ path exists.
        '''
        print(f"{self.clock}ns: Emitting photons.")
        with open("output/emit_photons.out", "w") as file:
            i=0
            while i<len(self.emitters):
                emitted_photon: Photon = self.emitters[i].emit_photon()
                output = str(self.emitters[i])
                print(output)
                file.write(output + '\n')
                i+=1
        print('')

    def print_activation_times(self) -> None:
        # only requires implementation once you reach RUN-MY-CIRCUIT
        '''
        Prints the output for the activation times for each receiver, sorted
        by activation time in ascending order. Any receivers that have not
        been activated should not be included.
        
        It will also need to write the output into a
        /home/output/activation_times.out output file.

        You can assume the /home/output/ path exists.
        '''
        print(f"Activation times:")
        sorted_receivers: list[Receiver] = sorter.sort_receivers_by_activation_time(self.receivers)
        with open("output/activation_times.out", "w") as file:
            i=0
            while i<len(sorted_receivers):
                if sorted_receivers[i].is_activated():
                    output: str = f"R{sorted_receivers[i].get_symbol()}: {sorted_receivers[i].get_activation_time()}ns"
                    print(output)
                    file.write(output+"\n")
                i+=1
        print('')

    def print_total_energy(self) -> None:
        # only requires implementation once you reach RUN-MY-CIRCUIT
        '''
        Prints the output for the total energy absorbed for each receiver,
        sorted by total energy absorbed in descending order. Any receivers
        that have not been activated should not be included.
        
        It will also need to write the output into a
        /home/output/total_energy_absorbed.out output file.

        You can assume the /home/output/ path exists.
        '''
        print("Total energy absorbed:")
        sorted_receivers: list[Receiver] = sorter.sort_receivers_by_total_energy(self.receivers)
        with open("output/total_energy.out", "w") as file:
            i=0
            while i<len(sorted_receivers):
                if sorted_receivers[i].is_activated():
                    print(sorted_receivers[i])
                    file.write(str(sorted_receivers[i])+"\n")
                i+=1
    
    def print_board(self) -> None:
        '''Calls the print_board method in board_displayer.'''
        self.board_displayer.print_board()

    def get_collided_emitter(self, entity) -> Optional[Emitter]:
        '''
        Takes in one argument entity which is either a component or a photon
        and checks if it has the same position as another emitter in the 
        circuit. 

        If it does, return the emitter already in the entity's position.
        Else, return None, indicating there is no emitter occupying entity's
        position.
        
        Parameter
        ---------
        entity - an emitter, receiver, photon or mirror

        Returns
        -------
        An emitter if it has the same position as entity, else None.
        '''
        x = entity.get_x()
        y = entity.get_y()
        i=0
        while i < len(self.emitters):
            if self.emitters[i].get_x() == x and self.emitters[i].get_y() == y:
                return self.emitters[i]
            i+=1
        return None

    def get_collided_receiver(self, entity) -> Optional[Receiver]:
        '''
        Takes in one argument entity which is either a component or a photon
        and checks if it has the same position as another receiver in the 
        circuit. 

        If it does, return the emitter already in the entity's position.
        Else, return None, indicating there is no receiver occupying entity's
        position.
        
        Parameter
        ---------
        entity - an emitter, receiver, photon or mirror

        Returns
        -------
        A receiver if it has the same position as entity, else None.
        '''
        x = entity.get_x()
        y = entity.get_y()
        i=0
        while i < len(self.receivers):
            if self.receivers[i].get_x() == x and self.receivers[i].get_y() == y:
                return self.receivers[i]
            i+=1
        return None

    def get_collided_mirror(self, entity) -> Optional[Mirror]:
        '''
        Takes in one argument entity which is either a component or a photon
        and checks if it has the same position as another mirror in the 
        circuit. 

        If it does, return the mirror already in the entity's position.
        Else, return None, indicating there is no mirror occupying entity's
        position.
        
        Parameter
        ---------
        entity - an emitter, receiver, photon or mirror

        Returns
        -------
        A mirror if it has the same position as entity, else None.
        '''
        x = entity.get_x()
        y = entity.get_y()
        i=0
        while i < len(self.mirrors):
            if self.mirrors[i].get_x() == x and self.mirrors[i].get_y() == y:
                return self.mirrors[i]
            i+=1
        return None

    def get_collided_component(self, photon: Photon) -> Union[Emitter, Receiver, Mirror, None]:
        # only requires implementation once you reach RUN-MY-CIRCUIT
        # will require extensions in ADD-MY-MIRRORS
        '''
        Given a photon, returns the component it has collided with (if any).
        A collision occurs if the positions of photon and the component are
        the same.

        Parameters
        ----------
        photon - a photon to check for collision with the circuit's components

        Returns
        -------
        If the photon collided with a component, return that component.
        Else, return None.

        Hint
        ----
        Use the three collision methods above to handle this.
        '''
        if self.get_collided_emitter(photon):
            return self.get_collided_emitter(photon)
        elif self.get_collided_receiver(photon):
            return self.get_collided_receiver(photon)
        elif self.get_collided_mirror(photon):
            return self.get_collided_mirror(photon)
        return None
        
    def tick(self) -> None:
        # only requires implementation once you reach RUN-MY-CIRCUIT
        '''
        Runs a single nanosecond (tick) of this circuit. If the circuit has
        already finished, this method should return out early.
        
        Otherwise, for each photon that has not been absorbed, this method is
        responsible for moving it, updating the board to show its new position
        and checking if it collided with a component (and handling it if did
        occur). At the end, we then increment clock.
        '''
        self.clock += 1
        
        if self.is_finished():
            return
        #move every non-absorbed photon
        i=0
        while i < len(self.photons):
            if not self.photons[i].is_absorbed():
                #move photon, check for collision with wall
                self.photons[i].move(self.width, self.height)
                #add photon to board if empty slot
                self.board_displayer.add_photon_to_board(self.photons[i])
                #check for collision with any component
                collided_component: Union[Emitter, Receiver, Mirror, None] = self.get_collided_component(self.photons[i])
                if collided_component:
                    self.photons[i].interact_with_component(collided_component, (self.clock))
            i+=1

    def run_circuit(self) -> None:
        # only requires implementation once you reach RUN-MY-CIRCUIT
        '''
        Runs the entire circuit from start to finish. This involves getting
        each emitter to emit a photon, and continuously running tick until the
        circuit is finished running. All output in regards of running the 
        circuit should be contained in this method.
        '''
        #step 1: print notification message
        print("\n========================\n   RUNNING CIRCUIT...\n========================\n")
        #step 2: emit photons from every emitter and write to /home/output/emit_photons.out
        self.emit_photons()
        self.print_emit_photons()
        if self.is_finished():
            print(f"{self.clock}ns: 0/{len(self.receivers)} receiver(s) activated.")
            self.board_displayer.print_board()
            print('')
        
        #step 3: tick in a loop; print activated receivers every 5 nanoseconds
        while not self.is_finished(): 
            self.tick()
            
            #find all activated receivers
            activated_receivers: list[Receiver] = [] 
            i=0
            while i<len(self.receivers):
                if self.receivers[i].is_activated():
                    activated_receivers.append(self.receivers[i])
                i+=1
                
            if self.is_finished():
                print(f"{self.clock}ns: {len(activated_receivers)}/{len(self.receivers)} receiver(s) activated.")
                self.board_displayer.print_board()
                print('')
                break
            
            #display messages every 5ns
            if self.clock%5 == 0:
                print(f"{self.clock}ns: {len(activated_receivers)}/{len(self.receivers)} receiver(s) activated.")
                self.board_displayer.print_board()
                print('')
            
        #step 4: print the activation times of the receivers in ascending order 
        #and write the output to /home/output/activation_times.out.
        self.print_activation_times()
        #step 5: print the total energy absorbed by each receiver in descending order 
        #and write to /home/output/total_energy_absorbed.out
        self.print_total_energy()
        #step 6: end with a notification message
        print("\n========================\n   CIRCUIT FINISHED!\n========================")
        

    def add_emitter(self, emitter: Emitter) -> bool:
        '''
        If emitter is not an Emitter instance, return False. Else, you need to
        perform the following checks in order for any errors:
        1)  The emitter's position is within the bounds of the circuit.
        2)  The emitter's position is not already taken by another emitter in
            the circuit.
        3)  The emitter's symbol is not already taken by another emitter in 
            the circuit.
        
        If at any point a check is not passed, an error message is printed
        stating the causeof the error and returns False, skipping any further
        checks. If all checks pass, then the following needs to occur:
        1)  emitter is added in the circuit's list of emitters. emitter
            needs to be added such that the list of emitters remains sorted
            in alphabetical order by the emitter's symbol. You can assume the
            list of emitters is already sorted before you add the emitter.
        2)  emitter's symbol is added into board_displayer.
        3)  The method returns True.   

        Paramaters
        ----------
        emitter - the emitter to add into this circuit's list of emitters

        Returns
        ----------
        Returns true if all checks are passed and the emitter is added into
        the circuit.
        Else, if any of the checks are not passed, prints an error message
        stating the cause of the error and returns False, skipping any
        remaining checks.

        Hint
        ----
        Use the get_collided_emitter method to check for position collision.
        You will need to find your own way to check for symbol collisions
        with other emitters.
        '''
        if not isinstance(emitter, Emitter):
            return False

        x, y = emitter.get_x(), emitter.get_y()
        
        # check if emitter's position is within the bounds of the circuit
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            print(f'Error: position {x, y} is out-of-bounds of {self.get_width()}x{self.get_height()} circuit board')
            return False
        
        # check if emitter's position is already taken by another emitter in the circuit
        collision_emitter = self.get_collided_emitter(emitter)
        if collision_emitter:
            print(f"Error: position {x, y} is already taken by emitter '{collision_emitter.get_symbol()}'")
            return False
        
        # check if emitter's symbol is already taken by another emitter in the circuit
        i=0
        while i < len(self.emitters):
            if self.emitters[i].get_symbol() == emitter.get_symbol():
                print(f'Error: symbol {emitter.get_symbol()} is already taken by another emitter in the circuit.')
                return False
            i+=1
            
        # add emitter in the circuit's list of emitters
        # if the list of emitters is empty, append emitter to the list
        if not self.emitters: 
            self.emitters.append(emitter)
        else: 
            #insert alphabetically
            i=0
            while i < len(self.emitters):
                if (self.emitters[i].get_symbol() > emitter.get_symbol()):
                    #insert emitter immediately at index i, pushing all other emitters to the right
                    self.emitters.insert(i, emitter)
                    break
                #when we reach the end of the list, append emitter to the end
                if i == len(self.emitters) - 1:
                    self.emitters.append(emitter)
                    break
                i+=1
            
        #add emitter's symbol into board_displayer
        self.board_displayer.add_component_to_board(emitter)

        return True

    def get_emitters(self) -> list[Emitter]:
        '''Returns emitters.'''
        return self.emitters

    def add_receiver(self, receiver: Receiver) -> bool:
        '''
        If receiver is not a Receiver instance, return False. Else, you need to
        perform the following checks in order for any errors:
        1)  The receiver's position is within the bounds of the circuit.
        2)  The receiver's position is not already taken by another emitter
            or receiver in the circuit.
        3)  The receiver's symbol is not already taken by another receiver in
            the circuit. 
            
        If at any point a check is not passed, an error message is printed stating
        the cause of the error and returns False, skipping any further checks. If 
        all checks pass, then the following needs to occur:
        1)  receiver is added in the circuit's list of receivers. receiver
            needs to be added such that the list of receivers  remains sorted
            in alphabetical order by the receiver's symbol. You can assume the
            list of receivers is already sorted before you add the receiver. 
        2)  receiver's symbol is added into board_displayer.
        3)  The method returns True.

        Paramaters
        ----------
        receiver - the receiver to add into this circuit's list of receivers

        Returns
        ----------
        Returns true if all checks are passed and the receiver is added into
        the circuit.
        Else, if any of the checks are not passed, prints an error message
        stating the cause of the error and returns False, skipping any
        remaining checks.

        Hint
        ----
        Use the get_collided_emitter and get_collided_receiver methods to
        check for position collisions.
        You will need to find your own way to check for symbol collisions
        with other receivers.
        '''
        if not isinstance(receiver, Receiver):
            return False
        # check if receiver's position is within the bounds of the circuit
        x, y = receiver.get_x(), receiver.get_y()
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            print(f'Error: position {x, y} is out-of-bounds of {self.get_width()}x{self.get_height()} circuit board')
            return False
        # check if receiver's position is already taken by another receiver/emitter in the circuit
        collision_emitter = self.get_collided_emitter(receiver)
        collision_receiver = self.get_collided_receiver(receiver)
        if collision_emitter:
            print(f"Error: position {x, y} is already taken by emitter '{collision_emitter.get_symbol()}'")
            return False
        if collision_receiver:
            print(f"Error: position {x, y} is already taken by receiver 'R{collision_receiver.get_symbol()}'")
            return False
        # check if receiver's symbol is already taken by another receiver in the circuit
        i=0
        while i < len(self.receivers):
            if self.receivers[i].get_symbol() == receiver.get_symbol():
                print(f"Error: symbol 'R{receiver.get_symbol()}' is already taken")
                return False
            i+=1
        # add receiver in the circuit's list of receivers
        # if the list of receiver is empty, append receiver to the list
        if not self.receivers: 
            self.receivers.append(receiver)
        else: 
            #insert alphabetically
            i=0
            while i < len(self.receivers):
                if (self.receivers[i].get_symbol() > receiver.get_symbol()):
                    #insert receiver immediately at index i, pushing all other receiver to the right
                    self.receivers.insert(i, receiver)
                    break
                #when we reach the end of the list, append receiver to the end
                if i == len(self.receivers) - 1:
                    self.receivers.append(receiver)
                    break
                i+=1
        #add receiver's symbol into board_displayer
        self.board_displayer.add_component_to_board(receiver)
        #returns True
        return True

    def get_receivers(self) -> list[Receiver]:
        '''Returns receivers.'''
        return self.receivers

    def add_photon(self, photon: Photon) -> bool:
        # only requires implementation once you reach RUN-MY-CIRCUIT
        '''
        If the photon passed in is not a Photon instance, it does not add it in
        and returns False. Else, it adds photon in this circuit's list of
        photons and returns True.

        Parameters
        ----------
        photon - the photon to add into this circuit's list of photons

        Returns
        -------
        Returns True if the photon is added in, else False.
        '''
        if not isinstance(photon, Photon):
            return False
        # add photon in the circuit's list of photons
        self.photons.append(photon)
        return True

    def get_photons(self) -> list[Photon]:
        # only requires implementation once you reach RUN-MY-CIRCUIT
        '''Returns photons.'''
        return self.photons

    def add_mirror(self, mirror: Mirror) -> bool:
        # only requires implementation once you reach ADD-MY-MIRRORS
        '''
        If mirror is not a Mirror instance, return False. Else, you need to
        perform the following checks in order for any errors:
        1)  The mirror's position is within the bounds of the circuit.
        2)  The mirror's position is not already taken by another emitter, 
            receiver or mirror in the circuit.
            
        If at any point a check is not passed, an error message is printed
        stating the cause of theerror and returns False, skipping any further
        checks. If all checks pass, then the following needs to occur: 
        1)  mirror is added in the circuit's list of mirrors.
        2) mirror's symbol is added into board_displayer.
        3)   The method returns True.

        Paramaters
        ----------
        mirror - the mirror to add into this circuit's list of mirrors

        Returns
        ----------
        Returns true if all checks are passed and the mirror is added into
        the circuit.
        Else, if any of the checks are not passed, prints an error message
        stating the cause of the error and returns False, skipping any
        remaining checks.
        '''
        if not isinstance(mirror, Mirror):
            return False
        # check if mirror's position is within the bounds of the circuit
        x, y = mirror.get_x(), mirror.get_y()
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            print(f'Error: position {x, y} is out-of-bounds of {self.get_width()}x{self.get_height()} circuit board')
            return False
        # check if mirror's position is already taken by another mirror/receiver/emiiter in the circuit
        collision_emitter = self.get_collided_emitter(mirror)
        collision_receiver = self.get_collided_receiver(mirror)
        collision_mirror = self.get_collided_mirror(mirror)
        if collision_emitter:
            print(f"Error: position {x, y} is already taken by emitter '{collision_emitter.get_symbol()}'")
            return False
        if collision_receiver:
            print(f"Error: position {x, y} is already taken by receiver 'R{collision_receiver.get_symbol()}'")
            return False
        if collision_mirror:
            print(f"Error: position {x, y} is already taken by mirror '{collision_mirror.get_symbol()}'")
            return False
        
        # add mirror in the circuit's list of mirrors
        # if the list of mirrors is empty, append mirror to the list
        if not self.mirrors: 
            self.mirrors.append(mirror)
        else: 
            #insert alphabetically
            i=0
            while i < len(self.mirrors):
                if (self.mirrors[i].get_symbol() > mirror.get_symbol()):
                    #insert mirror immediately at index i, pushing all other mirrors to the right
                    self.mirrors.insert(i, mirror)
                    break
                #when we reach the end of the list, append mirror to the end
                if i == len(self.mirrors) - 1:
                    self.mirrors.append(mirror)
                    break
                i+=1
        #add mirror's symbol into board_displayer
        self.board_displayer.add_component_to_board(mirror)
        #returns True
        return True

    def get_mirrors(self) -> list[Mirror]:
        # only requires implementation once you reach ADD-MY-MIRRORS
        '''Returns mirrors.'''
        return self.mirrors
    
    def get_width(self) -> int:
        '''Returns width.'''
        return self.width

    def get_height(self) -> int:
        '''Returns height.'''
        return self.height
