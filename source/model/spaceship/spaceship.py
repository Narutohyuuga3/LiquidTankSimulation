import numpy as np
from ..physics.kinematic import kinematic
import random

class spaceship:
    """
    Shape of vals
                [x]                 [v_x]
    position =  [y] [m], velocity = [v_y] [m/s]
                [z]                 [v_z]

                    [(F_x), (F_-x)]
    boosterforce =  [(F_y), (F_-y)] [N], dims = [(dim_x) (dim_y) (dim_z)] ONLY + OR -, NO VALUES!
                    [(F_z), (t_-z)]

    boosterforce is absolute.

    mass = [m] [kg]
    """

    def __init__(self, position: list = [0, 0, 0], mass: int = 1000, boosterforce: list = [[100, 100], [100, 100], [100, 100]], velocity: list = [0, 0, 0], nPredict: int = 10, deltaT:float = 0.1):
        self._boosterforce = np.array(boosterforce) # [N]
        self.__mass = mass # [kg]

        accelVar = 0.23
        self.__position = np.array([[position[0]], [position[1]], [position[2]]])
        self.__velocity = np.array([[velocity[0]], [velocity[1]], [velocity[2]]])

        self.__computer = boardcomputer(self, accelVar, nPredict, deltaT)

    def setPosition(self, position):
        self.__position = position

    def setVelocity(self, velocity):
        self.__velocity = velocity

    def setMass(self, mass):
        self.__mass = mass
    
    def setBoosterforce(self, boosterforce):
        self._boosterforce = boosterforce

    # getter
    def getPosition(self):
        return self.__position
    
    def getVelocity(self):
        return self.__velocity

    def getAcceleration(self, dims):
        a = np.zeros((3, 1))
        for idx in range(len(dims)):
            if dims[idx] == '-': 
                a[idx, 0] = -1*self._boosterforce[idx, 0]
            elif dims[idx] == '+':
                a[idx, 0] = self._boosterforce[idx, 1]
            else:
                a[idx, 0] = 0
        return a/self.__mass

    def getMass(self):
        return self.__mass

    def getBoosterforce(self):
        return self._boosterforce
        
    # calculating methods
    def calcVelocity(self, time, dim):
        a = self.getAcceleration(dim)
        self.__velocity = kinematic.acceleration2velocity(a, time, self.__velocity)
        #print('Spaceship calculateVelocity: x=%f.1, y=%f.1, z=%f.1' %(self._velocity[0,0],self._velocity[1,0],self._velocity[2,0]))
        return self.__velocity

    def calculatePosition(self, time):
        self.__position = kinematic.velocity2position(self.__velocity, time, self.__position)
        #print('Spaceship calculatePosition: x=%f.1, y=%f.1, z=%f.1' %(self._position[0,0],self._position[1,0],self._position[2,0]))
        return self.__position

    def sendCompute(self, dims: list, all: bool = False):
        self.__computer.compute(dims, all)

    def sendUpdate(self, dims: list = None):
        #sigm = 0.025
        sigm = 0.0
        #x = self.__position[0].item() * random.gauss(1, sigm)
        #y = self.__position[1].item() * random.gauss(1, sigm)
        #z = self.__position[2].item() * random.gauss(1, sigm)
        #x = self.__position[0].item() * np.random.normal(1, sigm)
        #y = self.__position[1].item() * np.random.normal(1, sigm)
        #z = self.__position[2].item() * np.random.normal(1, sigm)
        x = self.__position[0].item()
        y = self.__position[1].item()
        z = self.__position[2].item()
        self.__computer.update([x, y, z], [sigm, sigm, sigm])
        if dims is None:
            self.__computer.compute(all=True)
        self.__computer.compute(dims, True)


    def getStepT(self):
        return self.__computer.stepT
    
    def getNPrediction(self):
        return self.__computer.nPrediction

    def getMeasurePoint(self):
        return self.__computer.measurePoint

    def getPrediction(self):
        return self.__computer.predictVal
    
    def getVariance(self):
        return self.__computer.sigma

class boardcomputer:
# to calculate predicted position, just call <<compute>>:
#   for all: bool=True
#   just next new prediction: bool=False
#   provide current control input
#
# to insert measure values, call <<update>>
#   give measure values and certainity values

    def __init__(self, spaceship: spaceship,  accel_variance: float = None, predictPosition: int = 10, deltaT: float = 0.1):
        """
        position, velocity, acceleration and accel_variance must be a 3-row vector, containing infos about x, y and z!
        """
        # Mittelwert des Systemzustandes
        position = spaceship.getPosition()
        velocity = spaceship.getVelocity()
        acceleration = np.zeros((3, 1))
        self.__x = np.bmat([[position], [velocity], [acceleration]])
        self.__a_var = accel_variance
        self.__spaceship = spaceship
        self.__stepT = deltaT
        self.__measurepoint = position

        # Covarianz des SS
        self.__P = np.eye(9)
        
        self.__predict = [[], [], []]
        self.__sigma = [[], [], []]
        for i in range(predictPosition):
            for dim in range(3):
                self.__predict[dim].append(dim * predictPosition + i)
                self.__sigma[dim].append(dim * predictPosition + i)
        

    @property
    def pos(self):
        return self.__x[0:3]

    @property    
    def vel(self):
        return self.__x[3:6]

    @property
    def accel(self):
        return self.__x[6:9]

    @property
    def x(self):
        return self.__x

    @property
    def P(self):
        return self.__P

    @property
    def sigma(self):
        return self.__sigma

    @property
    def predictVal(self):
        return self.__predict

    @property
    def stepT(self):
        return self.__stepT

    @property
    def nPrediction(self):
        return len(self.__predict[0])

    @property
    def currentPredictionTime(self):
        return self.__deltaT

    @property
    def measurePoint(self):
        return self.__measurepoint

    def predict(self, deltaT: float, a_input: np.ndarray) -> None:
        # inspired by CppMonk
        # x = F * x + G * u
        # P = F * P * F_t + G * G_t * a
        #print("boardcomputer->predict: deltaT %f.1" % (deltaT))
        #print("boardcomputer->predict: a_input:")
        #print(a_input)
        #print("boardcomputer->predict: state vector x")
        #print(self.__x)

        F=np.bmat([[np.eye(3), np.eye(3)*deltaT, np.zeros((3, 3))],
                   [np.zeros((3, 3)), np.eye(3), np.zeros((3, 3))],
                   [np.zeros((3, 3)), np.zeros((3, 3)), np.zeros((3, 3))]])

        G = np.bmat([[0.5*np.eye(3)*deltaT**2],
                     [np.eye(3)*deltaT],
                     [np.eye(3)]])
                     
        new_x = F.dot(self.__x) + G.dot(a_input)

        new_P = F.dot(self.__P).dot(F.T) + G.dot(G.T) * self.__a_var

        self.__x = new_x
        self.__P = new_P

    def update(self, measPos: list, measVar: list):
        # inspired by CppMonk
        # y = z - H * x
        # S = H * P * H_t
        # K = P * H_t * S_-1
        # x = x + K * y
        # P = (I - K * H) * P
        R = np.array([[measVar[0], 0, 0],
                      [0, measVar[1], 0],
                      [0, 0, measVar[2]]])

        self.__measurepoint = np.array([[measPos[0]],
                      [measPos[1]],
                      [measPos[2]]])

        H = np.bmat([np.eye(3), np.zeros((3, 3)), np.zeros((3, 3))])

        #print(H)
        #print(self.__x)
        y = self.__measurepoint - H.dot(self.__x)
        S = H.dot(self.__P).dot(H.T) + R
        K = self.__P.dot(H.T).dot(np.linalg.inv(S))
        new_x = self.__x + K.dot(y)
        new_P = (np.eye(9)-K.dot(H)).dot(self.__P)

        self.__x = new_x
        self.__P = new_P

        # credits to CppMonk for explaing and showing how to code and test the kalman filter
        # he was also the one, who showed it how to visualize it!
        # https://www.youtube.com/watch?v=m5Bw1m8jJuY
        # also credits to https://www.kalmanfilter.net/default.aspx for helping to develop the model
        # and providing the sources to learn the concepts of the kalman filters

    def compute(self, dims: np.ndarray = None, all: bool = False):
        # updates the time for prediction and initialize the predictionAndFill
        # decide if just a new point gets calculated or all prediction gets updated
        #print("boardcomputer->compute: dims")
        #print(dims)
        if dims is not None:
            accel = self.__spaceship.getAcceleration(dims)
        else:
            accel = np.zeros((3, 1))

        #print("boardcomputer->compute: accel")
        #print(accel)

        if all == False: # calculate just next one position
            self.__deltaT += self.__stepT
            #print("boardcomputer->compute: deltaT: %f0.1" % (self.__deltaT))
            self.predictAndFill(self.__deltaT, accel)

        else: # update all predictions and its cetrainty
            self.__deltaT = self.__stepT
            for k in range(len(self.__predict[0])):
                #print("boardcomputer->compute: deltaT: %f0.1 in %d iter" % (self.__deltaT, k))
                self.predictAndFill(self.__deltaT, accel)
                self.__deltaT += 0.1
        #print("boardcomputer->compute: return")

    def predictAndFill(self, deltaT: float, a_input: np.ndarray):
        # calculate the prediction and store it in the vectors
        predictStorage = self.__predict[:]
        sigmaStorage = self.__sigma[:]
        self.predict(deltaT, a_input)
        #print(self.__predict)
        #print(self.__sigma)
        for dim in range(3): # 0:x, 1:y, 2:z
            #print(dim)
            #print(self.__x[dim, 0].item())
            #print(self.__predict[dim])
            predictStorage[dim].append(self.__x[dim, 0].item()) # append new position at the end
            #print(self.__predict[dim])
            predictStorage[dim].pop(0) # erase 1st element
            #print(self.__predict[dim])
            
            #print(self.__P[dim, dim].item())
            #print(self.__sigma[dim])
            sigmaStorage[dim].append(np.sqrt(self.__P[dim, dim].item())) # append certainty of position at the end
            #print(self.__sigma[dim])
            sigmaStorage[dim].pop(0) # erase 1st element
            #print(self.__sigma[dim])
        #print(self.__predict)
        #print(self.__sigma)
        #print("return")

        self.__predict = predictStorage[:]
        self.__sigma = sigmaStorage[:]

        

if __name__ == '__main__':
    print('23')