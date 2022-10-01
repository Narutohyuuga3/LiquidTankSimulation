"""
Manage gamefield
initialise spaceship
have it's real position
    - posX
    - posY
    - angle r (calculating deltaX and deltaY and verctor orientation)
    - velocity v (deltaX and deltaY and "onboard time")
    - boostpower F (includes acceleration)
    - mass m

    logic:
    receiving keyPressed-Signal -> start time
    receiving keyReleased-Signal -> end timer
    time * F/m = v <- requires absolute time: 
        PROBLEM: no acceleration animation on surface. Player qould press key, sees nothing, releases
            and ship would instantly on calculated velocity
        SOLUTION: need a iterative descripted equation for the velocity
            v[k] = F/m* delta_t + v[k-1]
            delta_t meassured by timer
            Requires thread -> thread created at the start of program
                - includes position calculation
                - keyPressed-signal starts timer of thread and through that velocity calculation
                - keyReleased-signal ends timer and velocity calculation 
            Time thread frequently refresh surface -> emits signals

transmit spaceship "measured" data from earthstation
    by applying a random factor between 0.9 to 1.1 on folowing parameters
    - posX
    - posY
    for easiness, it is estimated, that the transmission is perfectly timed every 1s
"""

from PyQt6.QtCore import QObject, pyqtSignal
from threading import Thread
import time
import numpy as np
from Model.Spaceship.spaceship import spaceship

class Gamefield(QObject):

    updateSpaceshipPos = pyqtSignal(int, int, int)
    _spaceship = None
    _threadSurface = None
    _threadCalculations = None
    _keyPressed = None
    _dims = None

    def __init__(self):
        super().__init__()
        self._spaceship = spaceship(np.array([[200], [500], [0]]), 1500*1000, np.array([[10000000, 9500000],[5500000, 4500000], [0, 0]]), np.array([[0], [0], [0]]))
        self._keyPressed = False
        self._dims = ['+', '+', '+']
        self._keyPressed=[False, False, False]
        
        self._threadSurface = Thread(target= self.threadUpdateSurface, daemon=True)
        self._threadSurface.start()

        self._threadCalculations = Thread(target= self.threadUpdateCalculations, daemon=True)
        self._threadCalculations.start()


    def threadUpdateSurface(self):
        # Updates surface after 1/60fps ~ 16ms
        # - emits signals for surface
        # - sleeps required time
        #print("Gamefield threadUpdateSurface: Ping")
        while True:
            tic = time.time()
            # Signals emitten, Oberfläche aktualisieren
            position = self._spaceship.getPosition()
            self.updateSpaceshipPos.emit(position[0, 0], position[1, 0], position[2, 0])
            
            deltaT = time.time() - tic
            if  deltaT < 0.016: # Proof if elapsed time larger than 16ms
                time.sleep(0.016-deltaT) # sleep the missing time
            #redo everything
    
    def  threadUpdateCalculations(self):
        tic = time.time()
        timeVector = np.array([[0.0],[0.0],[0.0]])
        deltaT = 0
        while True:
            if deltaT == 0:
                time.sleep(0.001)

            deltaT = time.time() - tic

            if True in self._keyPressed:
                for idx, elem in enumerate(self._keyPressed):
                    if elem == True:
                        timeVector[idx, 0] = deltaT
                    else:
                        timeVector[idx, 0] = 0.0

                self._spaceship.calcVelocity(timeVector, self._dims)

            self._spaceship.calculatePosition(deltaT)
            tic = deltaT + tic

    def on_keyPressed(self, key):
        #print(f'Gamefield on_keyPressed: called {key}' )
        if key == 'w':
            self._keyPressed[1] = True
            self._dims[1] = '-'
        elif key == 's':
            self._keyPressed[1] = True
            self._dims[1] = '+'
        elif key == 'a':
            self._keyPressed[0] = True
            self._dims[0] = '-'
        elif key == 'd':
            self._keyPressed[0] = True
            self._dims[0] = '+'
        elif key == 'q':
            self._keyPressed[2] = True
            self._dims[2] = '+'
        else:
            self._keyPressed[2] = True
            self._dims[2] = '-'

    def on_keyReleased(self, key):
        #print(f'Gamefield on_keyReleased: called {key}' )
        if key == 'w':
            self._keyPressed[1] = False
        elif key == 's':
            self._keyPressed[1] = False
        elif key == 'a':
            self._keyPressed[0] = False
        elif key == 'd':
            self._keyPressed[0] = False
        elif key == 'q':
            self._keyPressed[2] = False
        else:
            self._keyPressed[2] = False

if __name__ == '__main__':
    pass