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

    kalman filter output
    - estimated position x/y    ]
    - sigma x/y                 ]} depict it as cloud/elipse on gamefield
    - probability cloud


"""

from turtle import update
from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot
from threading import Thread
import time
import numpy as np
from model.spaceship.spaceship import spaceship

class gamefield(QObject):

    updateSpaceshipPos = pyqtSignal(int, int, int)
    updateSpaceshipMeasurepoint = pyqtSignal(int, int, int)
    updateSpaceshipEstimation = pyqtSignal(list)
    
    def __init__(self):
        super().__init__()
        self.__spaceship = spaceship([200, 500, 0], 1500*1000, [[100000000, 95000000],[55000000, 45000000], [0, 0]], [0, 0, 0], nPredict=10, deltaT=0.1)
        self.__keyPressed = False
        self.__dims = ['+', '+', '+']
        self.__keyPressed=[False, False, False]
        self.__exit = False
        
        self.__threadSurface = Thread(target= self.threadUpdateSurface)
        self.__threadSurface.start()

        self.__threadCalculations = Thread(target= self.threadUpdateCalculations)
        self.__threadCalculations.start()

    def __del__(self):
        #print("Gamefield destroyer: called!")
        self.__exit = True
        self.__threadCalculations.join()
        self.__threadSurface.join()
        #print("Gamefield __del__: thread waiting done!")

    def threadUpdateSurface(self):
        # Updates surface after 1/60fps ~ 16ms
        # - emits signals for surface
        # - sleeps required time
        #print("Gamefield threadUpdateSurface: Ping")
        while self.__exit == False:
            tic = time.time()
            # Signals emitten, Oberfläche aktualisieren
            position = self.__spaceship.getPosition()
            self.updateSpaceshipPos.emit(position[0, 0], position[1, 0], position[2, 0])
            position = self.__spaceship.getMeasurePoint()
            self.updateSpaceshipMeasurepoint.emit(position[0, 0], position[1, 0], position[2, 0])
            
            listvar = self.__spaceship.getPrediction()
            self.updateSpaceshipEstimation.emit(listvar)

            deltaT = time.time() - tic
            if  deltaT < 0.016: # Proof if elapsed time larger than 16ms
                time.sleep(0.016 - deltaT) # sleep the missing time
            #redo everything
    
    def  threadUpdateCalculations(self):
        tic = time.time()
        timeVector = np.array([[0.0],[0.0],[0.0]])
        deltaT = 0
        deltaTUpdate = 0
        deltaTPredict = 0
        predictionTimespan = self.__spaceship.getStepT() * 0.8
        updateTime = 3 # s
        ticUpdate = tic - updateTime
        ticPredict = tic + predictionTimespan
        while self.__exit == False:
            if deltaT == 0:
                time.sleep(0.001)

            deltaT = time.time() - tic

            if True in self.__keyPressed:
                for idx, elem in enumerate(self.__keyPressed):
                    if elem == True:
                        timeVector[idx, 0] = deltaT
                    else:
                        timeVector[idx, 0] = 0.0
                self.__spaceship.calcVelocity(timeVector, self.__dims)

            self.__spaceship.calculatePosition(deltaT)
            tic = deltaT + tic

            # check and prediction of boardcomputer
            # nPredict * stepT = Timespan
            # check time to send update
            deltaTUpdate = time.time() - ticUpdate
            deltaTPredict = time.time() - ticPredict
            dims = self.matchDimsToInput()
            if deltaTUpdate >= updateTime: # send update to spaceship. Reset timers
                ticUpdate = ticUpdate + deltaTUpdate
                ticPredict = ticUpdate + predictionTimespan
                self.__spaceship.sendUpdate(dims) 
            
            elif deltaTPredict >= self.__spaceship.getStepT(): # calculate next prediction, erase first prediction
                ticPredict = ticPredict + deltaTPredict # reset timer
                self.__spaceship.sendCompute(dims) 


    def matchDimsToInput(self):
        dims = [0, 0, 0]
        for idx, elem in enumerate(self.__keyPressed):
            if elem == True:
                dims[idx] = self.__dims[idx]
            else:
                dims[idx] = 0
        return dims

    def on_keyPressed(self, key):
        #print(f'Gamefield on_keyPressed: called {key}' )
        if key == 'w':
            self.__keyPressed[1] = True
            self.__dims[1] = '-'
        elif key == 's':
            self.__keyPressed[1] = True
            self.__dims[1] = '+'
        elif key == 'a':
            self.__keyPressed[0] = True
            self.__dims[0] = '-'
        elif key == 'd':
            self.__keyPressed[0] = True
            self.__dims[0] = '+'
        elif key == 'q':
            self.__keyPressed[2] = True
            self.__dims[2] = '+'
        else:
            self.__keyPressed[2] = True
            self.__dims[2] = '-'

    def on_keyReleased(self, key):
        #print(f'Gamefield on_keyReleased: called {key}' )
        if key == 'w':
            self.__keyPressed[1] = False
        elif key == 's':
            self.__keyPressed[1] = False
        elif key == 'a':
            self.__keyPressed[0] = False
        elif key == 'd':
            self.__keyPressed[0] = False
        elif key == 'q':
            self.__keyPressed[2] = False
        else:
            self.__keyPressed[2] = False

if __name__ == '__main__':
    pass