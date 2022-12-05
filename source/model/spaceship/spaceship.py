import numpy as np
from ..physics.kinematic import kinematic
import random, copy

class spaceship:
    """
    Shape of vals
                [x]                 [v_x]                  [phi]                  [omega_r]
    position =  [y] [m], velocity = [v_y] [m/s], rotPos = [theta] [rad], rotVel = [omega_p] [rad/s]
                [z]                 [v_z]                  [psi]                  [omega_y]

                    [(F_x), (F_-x), (F_xr)]
    boosterforce =  [(F_y), (F_-y), (F_yp)] [N], dims = [(dim_x) (dim_y) (dim_z)] ONLY + OR -, NO VALUES!
                    [(F_z), (t_-z), (F_zy)]    dimsRot = [(roll) (pitch) (yawn)] ONLY + OR -, NO VALUES!

    boosterforce is absolute.

    mass = [m] [kg], diameter = [d] [m], height = [h] [m], 
    """

    def __init__(self, position: list = [0, 0, 0], mass: float = 2_900_000.0, rocketDiameter: float = 10.1, rocketHeigth: float = 110.6, boosterforce: list = [[34_500_000, 34_500, 800], [34_500, 34_500, 800], [34_500, 34_500, 800]], velocity: list = [0, 0, 0], orientation: list= [0, 0, 0], rotationVelocity: list = [0, 0, 0], boosterforceDev: float = 10.3 ,nPredict: int = 10, deltaT:float = 0.1):
        self.__boosterforce = np.array(boosterforce) # [N]
        self.__mass = mass # [kg]
        self.__position = np.array([[position[0]], [position[1]], [position[2]]])
        self.__velocity = np.array([[velocity[0]], [velocity[1]], [velocity[2]]])
        self.__rotPos = np.array([[orientation[0]], [orientation[1]], [orientation[2]]])
        self.__rotVel = np.array([[rotationVelocity[0]], [rotationVelocity[1]], [rotationVelocity[2]]])
        self.__diameter = rocketDiameter
        self.__height = rocketHeigth

        self.__accelDev = boosterforceDev/mass
        self.__rotAccelDev =  boosterforceDev * (self.__diameter * 0.5)/self.getMomentOfInertia()

        self.__computer = boardcomputer(self, nPredict, deltaT)

    # getter/setter
    def setPosition(self, position = np.zeros((3, 1))):
        self.__position = position
    def getPosition(self):
        return self.__position
    def getPositionList(self):
        return self.__position.reshape(3).tolist()

    def setRotPos(self, position = np.zeros((3, 1))):
        self.__rotPos = position
    def getRotPos(self):
        return self.__rotPos
    def getRotPosList(self):
        return self.__rotPos.reshape(3).tolist()

    def setVelocity(self, velocity = np.zeros((3, 1))):
        self.__velocity = velocity
    def getVelocity(self):
        return self.__velocity
    def getVelocityList(self):
        return self.__velocity.reshape(3).tolist()
    
    def setRotVel(self, velocity):
        self.__rotVel = velocity
    def getRotVel(self):
        return self.__rotVel
    def getRotVelList(self):
        return self.__rotVel.reshape(3).tolist()

    def setMass(self, mass: float = 1000.0):
        #print(f"Spaceship->setMass: {mass}")
        self.__mass = mass    
    def getMass(self):
        return self.__mass
    def getMomentOfInertia(self):
        return 0.8*self.__mass*(self.__diameter*0.5)**2 # I = [1/2 <-> 1]*m*r**2, 1 = full body cylinder, 1/2 = outer hull cylinder

    def setBoosterforce(self, boosterforce = np.ones((3, 3))):
        #print(f"Spaceship->setBoosterforce: {boosterforce}")
        self.__boosterforce = np.array(boosterforce)
    def getBoosterforce(self):
        return self.__boosterforce.tolist()

    def setBoosterforceDeviation(self, var):
        #print(f"Spaceship->setAccelDevaition: accelVar pre: {self.__computer.accelVar} with variable var as: {np.sqrt(np.abs(self.__computer.accelVar))}")
        self.__accelDev = var/self.__mass # convert Force to acceleration
        self.__rotAccelDev =  var * (self.__diameter * 0.5)/self.getMomentOfInertia()
        #print(f"Spaceship->setAccelVariance: accelVar after: {self.__computer.accelVar} with variable var as: {var}")
    def getBoosterforceDeviation(self):
        return self.__accelDev*self.__mass # convert acceleration to force
    
    def getAcceleration(self, dims = None):
        a = np.zeros((3, 1))
        if dims == None:
            return a
        #print(f'Spaceship->getAcceleration: dims: {dims}')
        for idx in range(len(dims)):
            if dims[idx] == '-': 
                a[idx, 0] = -1*self.__boosterforce[idx, 1]
            elif dims[idx] == '+':
                a[idx, 0] = self.__boosterforce[idx, 0]
            else:
                a[idx, 0] = 0
        # convert force to acceleration
        #print(f'Spaceship->getAcceleration: a: {a}')
        return a/self.__mass # F/m = a 
    def getRotAcceleration(self, dims = None):
        a = np.zeros((3, 1))
        if dims == None:
            return a
        for idx in range(len(dims)):
            if dims[idx] == '-': 
                a[idx, 0] = -1*self.__boosterforce[idx, 2]
            elif dims[idx] == '+':
                a[idx, 0] = self.__boosterforce[idx, 2]
            else:
                a[idx, 0] = 0
            # convert force to rotational acceleration, dependen from dimension
            if idx == 0: # dim x -> roll
               a[idx, 0] = a[idx, 0] * (self.__diameter * 0.5)/ self.getMomentOfInertia() # F * r/I = M/I = alpha
            else: # dim y/z -> pitch/yawn
                a[idx, 0] = a[idx, 0] * (self.__height * 0.5 * 0.8)/ self.getMomentOfInertia() # F * r/I = M/I = alpha
        return a 

    def setDeltaT(self, var):
        self.__computer.deltaT = var
    def getDeltaT(self):
        return self.__computer.deltaT
    
    def setNPrediction(self, val):
        #print("Spaceship->setNPrediction: val: %d" % (val))
        #print(f"Spaceship->setNPrediction: nPrediction pre: {self.__computer.nPrediction}")
        self.__computer.nPrediction = val
        #print(f"Spaceship->setNPrediction: nPrediction after: {self.__computer.nPrediction}")
    def getNPrediction(self):
        return self.__computer.nPrediction

    def getMeasurePoint(self):
        return self.__computer.measurePoint
    def getMeasurePointList(self):
        return self.__computer.measurePoint.reshape(6).tolist()

    def getPrediction(self):
        return self.__computer.predictVal
    def getDeviation(self):
        return self.__computer.sigma

    # calculating methods
    def calcVelocity(self, time, dim, dimRot):
        a = self.getAcceleration(dim)
        alpha = self.getRotAcceleration(dimRot)
        # add deviation on it
        for idx, elem in enumerate(a):
            a[idx] = random.gauss(elem, self.__accelDev)
            #a[idx] = np.random.normal(elem, self.__boosterforceDev)
            pass
        
        #print('Spaceship->calcVelocity: ax=%f.1, ay=%f.1, az=%f.1' %(a[0,0], a[1,0], a[2,0]))
        self.__velocity = kinematic.acceleration2velocity(a, time, self.__velocity)
        #print('Spaceship->calcVelocity: x=%f.1, y=%f.1, z=%f.1' %(self.__velocity[0,0], self.__velocity[1,0], self.__velocity[2,0]))
        return self.__velocity

    def calculatePosition(self, time, dim = None, dimRot = None):
        a = self.getAcceleration(dim)
        alpha = self.getRotAcceleration(dimRot)
        #print(f'Spaceship->calculatePosition: time: {time}, timeNorm: {timeNorm}, timeRot: {timeRot}')
        for idx, elem in enumerate(a):
            #a[idx] = random.gauss(elem, self.__accelDev)
            #a[idx] = np.random.normal(elem, self.__boosterforceDev)
            pass
        #self.__position = kinematic.velocity2position(self.__velocity, time, self.__position)
        #print(f'Spaceship->calculatePosition: time: {time}, velocity: {self.__velocity}, position: {self.__position}')
        #self.__position = kinematic.acceleration2position(a, time, self.__velocity, self.__position)
        self.__position = kinematic.acceleration2positionWBodyAngle(a, alpha, time, time, self.__velocity, self.__position, self.__rotPos, self.__rotVel)
        # update velocity, rotVel and rotPos, 
        self.__rotPos = kinematic.rotAcceleration2rotPos(alpha, time, self.__rotVel, self.__rotPos)
        self.__velocity = kinematic.acceleration2velocityWBodyAngle(a, alpha, time, time, self.__velocity, self.__rotPos, self.__rotVel)
        self.__rotVel = kinematic.rotAcceleration2rotVelocity(alpha, time, self.__rotVel)
        #print('Spaceship->calculatePosition: x=%f.1, y=%f.1, z=%f.1' %(self.__position[0,0],self.__position[1,0],self.__position[2,0]))
        #print('Spaceship->calculatePosition: vx=%f.1, vy=%f.1, vz=%f.1' %(self.__velocity[0,0],self.__velocity[1,0],self.__velocity[2,0]))
        return self.__position

    def sendCompute(self, dims: list, all: bool = False):
        self.__computer.compute(dims, all)

    def sendUpdate(self, dims: list, dimsRot: list, measureDeviation: list = [40, 40, 0], rotMeasureDeviation: list = [0.1, 0.1, 0]):
        x = random.gauss(self.__position[0, 0].item(), measureDeviation[0])
        y = random.gauss(self.__position[1, 0].item(), measureDeviation[1])
        z = random.gauss(self.__position[2, 0].item(), measureDeviation[2])
        #x = np.random.normal(self.__position[0].item(), measureDeviation[0])
        #y = np.random.normal(self.__position[1].item(), measureDeviation[1])
        #z = np.random.normal(self.__position[2].item(), measureDeviation[2])
        #x = self.__position[0].item()
        #y = self.__position[1].item()
        #z = self.__position[2].item()

        phi = self.__rotPos[0, 0]
        theta = self.__rotPos[1, 0]
        psi = self.__rotPos[2, 0]

        #print("Spaceship->sendUpdate: measureDevaiation pre: ")
        #print(measureDevaition)
        l_measureVariance = measureDeviation.copy()
        for index, elem in enumerate(l_measureVariance):
            l_measureVariance[index] = elem**2
        #print("Spaceshipe->sendUpdate: measureDevbiation to measureVariance:")
        #print(l_measureVariance)
        l_rotMeasureVariance = rotMeasureDeviation.copy()
        for index, elem in enumerate(l_rotMeasureVariance):
            l_rotMeasureVariance[index] = elem**2

        self.__computer.update([x, y, z], l_measureVariance, [phi, theta, psi], l_rotMeasureVariance)
        #print("Spaceship->sendUpdate: dims")
        #print(dims)
        accel = self.getAcceleration(dims)
        #print(f"Spaceship->sendUpdate: accel: {accel}")
        accelVar = (self.__accelDev)**2
        #print(f"Spaceship->sendUpdate: accelVar: {accelVar}")

        rotAccel = self.getRotAcceleration(dimsRot)
        rotAccelVar = (self.__rotAccelDev)**2
        self.__computer.compute(accelVar= accelVar, accel = accel, rotAccelVar = rotAccelVar, rotAccel = rotAccel, all = True)


class boardcomputer:
# to calculate predicted position, just call <<compute>>:
#   for all: bool=True
#   just next new prediction: bool=False
#   provide current control input
#
# to insert measure values, call <<update>>
#   give measure values and certainity values

    def __init__(self, spaceship: spaceship, predictPosition: int = 10, deltaT: float = 0.1):
        """
        position, velocity, acceleration and accel_variance must be a 3-row vector, containing infos about x, y and z!
        """
        # Mittelwert des Systemzustandes
        position = spaceship.getPosition()
        velocity = spaceship.getVelocity()
        acceleration = np.zeros((3, 1))
        rotPos = spaceship.getRotPos()
        rotVel = spaceship.getRotVel()
        rotAccel = spaceship.getRotAcceleration()
        self.__x = np.bmat([[position], [velocity], [acceleration], [rotPos], [rotVel], [rotAccel]])
        self.__deltaT = deltaT
        self.__measurepoint = position

        self.__newStorageAvaible = False

        # Covarianz des SS
        self.__P = np.eye(18)
        
        self.__nPredict = predictPosition
        self.__newNPredict = self.__nPredict
        self.__predict = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]
        for i in range(predictPosition):
            for dim in range(18):
                self.__predict[dim].append(dim * predictPosition + i)

        self.__sigma = copy.deepcopy(self.__predict)
        self.__newPredict = copy.deepcopy(self.__predict)
        self.__newSigma = copy.deepcopy(self.__predict)
    
    #############################
    #### Getter/Setter

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
    def rotState(self):
        return self.__x[9:18]

    @property
    def rotPos(self):
        return self.__x[9:12]
    
    @property
    def rotVel(self):
        return self.__x[12:15]
    
    @property
    def rotAccel(self):
        return self.__x[15:18]

    @property
    def x(self):
        return self.__x     # current state of the system

    @property
    def P(self):
        return self.__P     # current variance of the system

    @property
    def sigma(self):
        return self.__sigma # provides the standard deviation*3 of the past n iteration

    @property
    def predictVal(self):
        return self.__predict   # provides the estimated position of the past n iteration

    @property
    def deltaT(self):
        return self.__deltaT

    @deltaT.setter
    def deltaT(self, var):
        self.__deltaT = var

    @property
    def nPrediction(self):
        #print("Boardcomputer->nPrediction: getter called")
        return len(self.__predict[0])
    
    @nPrediction.setter
    def nPrediction(self, val: int):
        #print("Boardcomputer->nPrediction: val: %d" % (val))
        diff = val - self.__nPredict
        #print(f"Boardcomputer->nPrediction.setter: target is: {val}, current amount: {self.__nPredict}")
        #print(f"Boardcomputer->nPrediction.setter: difference {diff}")
        self.__newSigma = copy.deepcopy(self.__sigma)
        self.__newPredict = copy.deepcopy(self.__predict)
        #print(f"Boardcomputer->nPrediction.setter: old dim: {len(self.__newPredict[0])}")
        for idx in range(len(self.__newPredict)):
            if diff > 0:
                for k in range(diff): # add entries who are missing
                    #print(f"Boardcomputer->nPrediction.setter: {k}-iter of {diff} in dim {idx}")
                    self.__newPredict[idx].append(0)
                    self.__newSigma[idx].append(0)
            elif diff < 0:
                for k in range(-1*diff): # remove entries who are too much
                    #print(f"Boardcomputer->nPrediction.setter: {k}-iter of {diff} in dim {idx}")
                    self.__newPredict[idx].pop()
                    self.__newSigma[idx].pop()
        #print(f"Boardcomputer->nPrediction.setter: new dim rows: {len(self.__newPredict)}")
        #print(f"Boardcomputer->nPrediction.setter: new dim cols: {len(self.__newPredict[0])}")
        #print(f"Boardcomputer->nPrediction.setter: target was: {val}")

        self.__newNPredict = val
        self.__newStorageAvaible = True

    @property
    def measurePoint(self):
        return self.__measurepoint

    ################################
    ### Calculation methods

    def  predict(self, deltaT: float, a_input: np.ndarray, aVariance, alpha_input: np.ndarray, alphaVariance) -> None:
        # Model is nonlinear. Extend it to unscented kalman filter!

        # inspired by CppMonk
        # x = F * x + G * u
        # P = F * P * F_t + G * G_t * a
        #print("Boardcomputer->predict: deltaT %f.1" % (deltaT))
        #print("Boardcomputer->predict: a_input:")
        #print(a_input)
        #print("Boardcomputer->predict: state vector x")
        #print(self.__x)
        #print(f"Boardcomputer->predict: Variance of aceleration: {aVariance}")
        #print(f"Boardcomputer->predict: Input of aceleration: {a_input}")
        
        F=np.bmat([[       np.eye(3), np.eye(3)*deltaT, np.zeros((3, 3)), np.zeros((3, 3)), np.zeros((3, 3)), np.zeros((3, 3))],
                   [np.zeros((3, 3)),        np.eye(3), np.zeros((3, 3)), np.zeros((3, 3)), np.zeros((3, 3)), np.zeros((3, 3))],
                   [np.zeros((3, 3)), np.zeros((3, 3)), np.zeros((3, 3)), np.zeros((3, 3)), np.zeros((3, 3)), np.zeros((3, 3))],
                   [np.zeros((3, 3)), np.zeros((3, 3)), np.zeros((3, 3)),      np.eye((3)), np.eye(3)*deltaT, np.zeros((3, 3))],
                   [np.zeros((3, 3)), np.zeros((3, 3)), np.zeros((3, 3)), np.zeros((3, 3)),        np.eye(3), np.zeros((3, 3))],
                   [np.zeros((3, 3)), np.zeros((3, 3)), np.zeros((3, 3)), np.zeros((3, 3)), np.zeros((3, 3)), np.zeros((3, 3))]])

        G = np.bmat([[0.5*np.eye(3)*deltaT**2,        np.zeros((3, 3))],
                     [       np.eye(3)*deltaT,        np.zeros((3, 3))],
                     [              np.eye(3),        np.zeros((3, 3))],
                     [       np.zeros((3, 3)), 0.5*np.eye(3)*deltaT**2],
                     [       np.zeros((3, 3)),        np.eye(3)*deltaT],
                     [       np.zeros((3, 3)),               np.eye(3)]])

        F_ = np.bmat([[       np.eye(3), np.eye(3)*deltaT, np.zeros((3, 3))],
                      [np.zeros((3, 3)),        np.eye(3), np.zeros((3, 3))],
                      [np.zeros((3, 3)), np.zeros((3, 3)), np.zeros((3, 3))]])
        G_ = np.bmat([[0.5*np.eye(3)*deltaT**2],
                      [np.eye(3)*deltaT],
                      [np.eye(3)]])

        Xrot = F_.dot(self.rotState) + G_.dot(alpha_input)

        a_mod = kinematic.bodyFrame2spaceFrame(Xrot[0:3]).dot(a_input)

        a = np.bmat([[a_mod],
                     [alpha_input]])

        new_x = F.dot(self.__x) + G.dot(a)

        new_P = F.dot(self.__P).dot(F.T) + G.dot(G.T)*aVariance

        self.__x = new_x
        self.__P = new_P

    def update(self, measPos: list, measVar: list, measRotPos: list, measRotVar: list):
        # Model is nonlinear. Extend it to unscented kalman filter

        # inspired by CppMonk
        # y = z - H * x
        # S = H * P * H_t
        # K = P * H_t * S_-1
        # x = x + K * y
        # P = (I - K * H) * P
        R = np.array([[   measVar[0], 0, 0, 0, 0, 0],
                      [0,    measVar[1], 0, 0, 0, 0],
                      [0, 0,    measVar[2], 0, 0, 0],
                      [0, 0, 0, measRotVar[0], 0, 0],
                      [0, 0, 0, 0, measRotVar[1], 0],
                      [0, 0, 0, 0, 0, measRotVar[2]]])

        self.__measurepoint = np.array([[   measPos[0]],
                                        [   measPos[1]],
                                        [   measPos[2]],
                                        [measRotPos[0]],
                                        [measRotPos[1]],
                                        [measRotPos[2]]])

        H = np.bmat([np.eye(6), np.zeros((6, 6)), np.zeros((6, 6))])

        #print("Boardcomputer->update: H:")
        #print(H)
        #print("Boardcomputer->update: measure x:")
        #print(self.__measurepoint)
        #print("Boardcomputer->update: x:")
        #print(self.__x)
        y = self.__measurepoint - H.dot(self.__x)
        #print(f"Boardcomputer->update: outcome y: {y}")
        S = H.dot(self.__P).dot(H.T) + R
        #print(f"Boardcomputer->update: shape of P: {np.shape(self.__P)}, shape of H: {np.shape(H)}, shape of S: {np.shape(S)}")
        K = self.__P.dot(H.T).dot(np.linalg.inv(S))
        new_x = self.__x + K.dot(y)
        new_P = (np.eye(18)-K.dot(H)).dot(self.__P)

        self.__x = new_x
        self.__P = new_P

        #print("Boardcomputer->update: x:")
        #print(self.__x)

        # credits to CppMonk for explaing and showing how to code and test the kalman filter
        # he was also the one, who showed it how to visualize it!
        # https://www.youtube.com/watch?v=m5Bw1m8jJuY
        # also credits to https://www.kalmanfilter.net/default.aspx for helping to develop the model
        # and providing the sources to learn the concepts of the kalman filters

    def compute(self, accelVar: float, accel: np.ndarray = None, rotAccelVar: float = 0.1, rotAccel: np.ndarray = None, all: bool = False):
        # updates the time for prediction and initialize the predictionAndFill
        # decide if just a new point gets calculated or all prediction gets updated
        if self.__newStorageAvaible:
            #print("Boardcomputer->compute: update variable containers")
            self.__predict = copy.deepcopy(self.__newPredict)
            self.__sigma = copy.deepcopy(self.__newSigma)
            self.__nPredict = self.__newNPredict
            self.__newStorageAvaible = False

        if all == False: # calculate just next one position
            #print("Boardcomputer->compute: deltaT: %f0.1" % (self.__deltaT))
            self.predictAndFill(self.__deltaT, accel, accelVar, rotAccel, rotAccelVar)

        else: # update all predictions and its cetrainty
            for k in range(self.__nPredict):
                #print("Boardcomputer->compute: deltaT: %f0.1 in %d iter" % (self.__deltaT, k))
                self.predictAndFill(self.__deltaT, accel, accelVar, rotAccel, rotAccelVar)
        #print("Boardcomputer->compute: return")

    def predictAndFill(self, deltaT: float, a_input: np.ndarray, a_variance: float, aRot_input: np.ndarray, aRot_variance: float):
        # calculate the prediction and store it in the vectors
        predictStorage = copy.deepcopy(self.__predict[:])
        sigmaStorage = copy.deepcopy(self.__sigma[:])
        self.predict(deltaT, a_input, a_variance, aRot_input, aRot_variance)
        #print("Boardcomputer->predictAndFill: predict vector:")
        #print(self.__predict)
        #print("Boardcomputer->predictAndFill: sigma vector:")
        #print(self.__sigma)
        for dim in range(18): # 0:x, 1:y, 2:z 3:vx, 4:vy, 5:vz, 6:ax, 7:ay, 8:az 9:phi, 10:theta, 11:psi 12:wr, 13:wp, 14:wy, 15:alphar, 16:alphap, 17:alphay
            #print(dim)
            #print(self.__x[dim, 0].item())
            #print(self.__predict[dim])
            predictStorage[dim].append(self.__x[dim, 0].item()) # append new position at the end
            #print(self.__predict[dim])
            predictStorage[dim].pop(0) # erase 1st element
            #print(self.__predict[dim])
            
            #print(self.__P[dim, dim].item())
            #print(self.__sigma[dim])
            sigmaStorage[dim].append(np.sqrt(np.abs(self.__P[dim, dim])).item() * 3) # convert to deviation and append 99% certainty of position at the end
            #print(self.__sigma[dim])
            sigmaStorage[dim].pop(0) # erase 1st element
            #print(self.__sigma[dim])
        #print(self.__predict)
        #print(self.__sigma)
        #print("return")

        self.__predict = copy.deepcopy(predictStorage[:])
        self.__sigma = copy.deepcopy(sigmaStorage[:])

        

if __name__ == '__main__':
    print('23')