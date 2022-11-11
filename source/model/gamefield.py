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

    updateSpaceshipPos = pyqtSignal(list, list, list)
    updatePrediction = pyqtSignal(list, list)
    updateInput = pyqtSignal(list)
    
    def __init__(self):
        super().__init__()
        position = [200, 500, 0]
        velocity = [0, 0, 0]
        nPredict = 10
        deltaT = 0.1
        boosterDev = 4_500_000 #
        self.__spaceship = spaceship(position=position, mass=2900*1000, boosterforce=[[34_500_000, 34_500_000],[34_500_000, 34_500_000], [0, 0]], velocity=velocity, boosterforceDev= boosterDev, nPredict=nPredict, deltaT=deltaT)
        self.__updateTime = 1
        self.__measureDeviation = [10, 10, 0]
        
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
        # ui
        time.sleep(1) # wait that qml is created and loaded
        listUI = []
        listUI.append(self.__spaceship.getNPrediction())
        listUI.append(self.__updateTime)
        listUI.append(self.__spaceship.getBoosterforceDeviation())
        listUI.append(self.__measureDeviation[0])
        listUI.append(self.__measureDeviation[1])
        print(listUI)
        self.updateInput.emit(listUI)

        while self.__exit == False:
            tic = time.time()
            # Signals emitten, Oberfläche aktualisieren
            position = self.__spaceship.getPositionList()
            velocity = self.__spaceship.getVelocityList()
            measurment = self.__spaceship.getMeasurePointList()
            self.updateSpaceshipPos.emit(position, velocity, measurment)
            listPosition = self.__spaceship.getPrediction()
            listDeviation = self.__spaceship.getDeviation()
            #print(f"Gamefield->updateSurface:  listPosition: {listPosition}")
            #print(f"Gamefield->updateSurface:   listPosition row: {len(listPosition)}")
            #print(f"Gamefield->updateSurface:  listPosition cols: {len(listPosition[0])}")
            #print(f"Gamefield->updateSurface: listDeviation: {listDeviation}")
            self.updatePrediction.emit(listPosition, listDeviation)
            deltaT = time.time() - tic
            if  deltaT < 0.016: # Proof if elapsed time larger than 16ms
                time.sleep(0.016 - deltaT) # sleep the missing time

            #self.updateInput.emit()
            #redo everything
    
    def  threadUpdateCalculations(self):
        tic = time.time()
        timeVector = np.array([[0.0],[0.0],[0.0]])
        deltaT = 0
        deltaTUpdate = 0
        ticUpdate = tic - self.__updateTime
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
            tic = time.time()

            # check and prediction of boardcomputer
            # nPredict * stepT = Timespan
            # check time to send update
            deltaTUpdate = time.time() - ticUpdate
            dims = self.matchDimsToInput()
            if deltaTUpdate >= self.__updateTime: # send update to spaceship. Reset timers
                ticUpdate = time.time()
                self.__spaceship.sendUpdate(dims, self.__measureDeviation) 

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
    
    def on_input(self, numPredictor: int, updateTime: float, boosterforceDeviation: float, measureDeviationX: float, measureDeviationY: float):
        print("Gamefield->on_input: numPred: %d, time: %f, aDev: %f, measDevX: %f, measDevY: %f" % (numPredictor, updateTime, boosterforceDeviation, measureDeviationX, measureDeviationY))
        #print(f"Gamefield on_input: updateTime pre: {self.__updateTime}")
        self.__updateTime = updateTime
        deltaT = updateTime/numPredictor
        #print(f"Gamefield on_input: updateTime after: {self.__updateTime}")
        self.__spaceship.setNPrediction(numPredictor)
        self.__spaceship.setDeltaT(deltaT)
        self.__spaceship.setBoosterforceDeviation(boosterforceDeviation)
        #print(f"Gamefield on_input: measureDeviation pre: {self.__measureDeviation}")
        self.__measureDeviation = [measureDeviationX, measureDeviationY, 0]
        #print(f"Gamefield on_input: measureDeviation after: {self.__measureDeviation}")

if __name__ == '__main__':
    pass