from turtle import position
import numpy as np
from ..Physics.kinematic import kinematic
from threading import Thread
import time
import random
class spaceship:
    """
    Shape of vals
                [x]                 [v_x]
    position =  [y] [m], velocity = [v_y] [m/s]
                [z]                 [v_z]

                    [(F_x), (F_-x)]
    boosterforce =  [(F_y), (F_-y)] [m/s**2], dims = [(dim_x) (dim_y) (dim_z)] ONLY + OR -, NO VALUES!
                    [(F_z), (t_-z)]

    boosterforce is absolute.

    mass = [m] [kg]

    clk [s] Computer clocktime of spaceship for calculations
    the orientation of spaceship in space is the last valid non-zero
        velcocity vector
    """

    def __init__(self, position, mass, boosterforce, velocity, clk):
        self._boosterforce = boosterforce # [N]
        self._mass = mass # [kg]
        self._position = position # Position vector 
        self._velocity = velocity # [m/s]
        self._boardcomputer = boardcomputer(self._position, clk)


    def setPosition(self, position):
        """
        expected input
                   [posX]
        position = [posY] [m]
                   [posZ]
        """
        self._position = position

    def setVelocity(self, velocity):
        """
        expected input
                   [veloX]
        velocity = [veloY] [m/s]
                   [veloZ]
        """
        self._velocity = velocity

    def setMass(self, mass):
        """
        expected input
        mass = m [kg]
        """
        self._mass = mass
    
    def setBoosterforce(self, boosterforce):
        """
        expected input
                       [(F_-x) (F_x)]
        boosterforce = [(F_-y) (F_y)]
                       [(F_-z) (F_z)]
        """
        self._boosterforce = boosterforce

    # getter
    def getPosition(self):
        """
        returns
            [x]
        p = [y] [m]
            [z]
        """
        return self._position
    
    def getEstimation(self):
        return self._boardcomputer.getEstimatedPosition()

    def getVelocity(self):
        """
        returns
            [v_x]
        v = [v_y] [m/s]
            [v_z]
        """
        return self._velocity

    def getAcceleration(self, dim):
        """
        expected input
        dim = [(dimX) (dimY) (dimZ)]

        returns
            [a_x]
        a = [a_y] [m/s**2]
            [a_z]
        """
        a = np.array([[0], [0], [0]])
        for idx in range(len(dim)):
            if dim[idx] == '-': 
                a[idx, 0] = -1*self._boosterforce[idx, 0]
            else:
                a[idx, 0] = self._boosterforce[idx, 1]

        return a/self._mass

    def _getAccelVal(self, idx, dim):
        """
        expected input
        dim = [(dimX) (dimY) (dimZ)]
        idx = skalar

        returns
        a = [a_dim] [m/s**2]
        """
        
    def getMass(self):
        """
        returns mass
        """
        return self._mass

    def getBoosterforce(self):
        """
        returns boosterforce matrix

                        [(F_x), (F_-x)]
        boosterforce =  [(F_y), (F_-y)] [m/s**2]
                        [(F_z), (t_-z)]

        """
        return self._boosterforce
        
    # calculating methods
    def calcVelocity(self, time, dim):
        """
        expected input:
               [timeX]
        time = [timeY] = time_general [s], dim =[(dimX) (dimY) (dimZ)]
               [timeZ]
        
        returns
                   [veloX]
        velocity = [veloY] [m/s]
                   [veloZ]
        """

        a = self.getAcceleration(dim)
        self._velocity = kinematic.acceleration2velocity(a, time, self._velocity)
        #print('Spaceship calculateVelocity: x=%f.1, y=%f.1, z=%f.1' %(self._velocity[0,0],self._velocity[1,0],self._velocity[2,0]))
        return self._velocity

    def calculatePosition(self, time):
        self._position = kinematic.velocity2position(self._velocity, time, self._position)
        #print('Spaceship calculatePosition: x=%f.1, y=%f.1, z=%f.1' %(self._position[0,0],self._position[1,0],self._position[2,0]))
        return self._position

    def sendTransmission(self, deltaTime):
        x = random.gauss(1, 0.025)
        y = random.gauss(1, 0.035)
        z = random.gauss(1, 0.0)
        position = np.array([[x],[y],[z]])*self._position
        self._boardcomputer.receiveTransmission(position, deltaTime)

    def getMeasurepoint(self):
        return self._boardcomputer.getMeasurepoint()

class boardcomputer:
    """
    Boadcomputer holds the current and last position
    It uses these information to estimate the current position and velocity
    Receives position updates
                [x]                     [x]
    position =  [y] [m], nextPosition = [y] [m]
                [z]                     [z]
    """

    def __init__(self, position, clk):
        self._position = position
        self._estimatedPosition = position    # x_k
        self._velocity = np.array([[0], [0], [0]])  # x_k-1
        self._clk = clk # [s]
        self._clkThread=Thread(target=self.compute, daemon=True)
        self._clkThread.start()

    # Model
    """
    x_k = A * x_k-1 + B * u_k
    y_k = C * x_k   + D * u_k

          [x_e]                  [x_n]
    y_k = [y_e] = x_k [m], u_k = [y_n] [m]
          [z_e]                  [z_n]

          [x_e]
    x_k = [y_e] [m]
          [z_e]

    x_k = estimated position
    x_k-1 = previous estimated position

        [-1/deltaT]            [1/deltaT]
    A = [-1/deltaT] [1/s], B = [1/deltaT]
        [-1/deltaT]            [1/deltaT]

    	[1]      [0]
    C = [1], D = [0]
        [1]      [0]
    """
    def receiveTransmission(self, position, deltaTime):
        # updates x_k-1 = A*x_k + B * u_k
        # x_k is our previous position
        # u_k is the received position
        #print("=====================================================================")
        #print("Boardcomputer receiveTransmission pre: v_x: %f.1, v_y: %f.1, v_z: %f.1" % (self._velocity[0, 0], self._velocity[1, 0], self._velocity[2, 0]))
        #print("Boardcomputer receiveTransmission pre: x: %f.1, y: %f.1, z: %f.1" % (position[0, 0], position[1, 0], position[2, 0]))
        self._velocity = kinematic.positions2velocity(self._position, position, deltaTime)
        self._position = position
        self._estimatedPosition = position
        #print("Boardcomputer receiveTransmission post: v_x: %f.1, v_y: %f.1, v_z: %f.1" % (self._velocity[0, 0], self._velocity[1, 0], self._velocity[2, 0]))

    def predictPosition(self, clk):
        # integration over time and gives x_k
        #print("=====================================================================")
        #print("Boardcomputer: calculate prediction")
        #print("Boardcomputer predictPosition: clk: %f.1" % (clk))
        #print("Boardcomputer predictPosition pre: x: %f.1, y: %f.1, z: %f.1" % (self._estimatedPosition[0, 0], self._estimatedPosition[1, 0], self._estimatedPosition[2, 0]))
        #print("Boardcomputer predictPosition pre: v_x: %f.1, v_y: %f.1, v_z: %f.1" % (self._velocity[0, 0], self._velocity[1, 0], self._velocity[2, 0]))
        self._estimatedPosition = kinematic.velocity2position(self._velocity, clk, self._estimatedPosition)
        #print("Boardcomputer predictPosition post: x: %f.1, y: %f.1, z: %f.1" % (self._estimatedPosition[0, 0], self._estimatedPosition[1, 0], self._estimatedPosition[2, 0]))
        #print("Boardcomputer predictPosition post: v_x: %f.1, v_y: %f.1, v_z: %f.1" % (self._velocity[0, 0], self._velocity[1, 0], self._velocity[2, 0]))

    def getEstimatedPosition(self):
        #print("Boardcomputer: send prediction")
        return self._estimatedPosition
    
    def getMeasurepoint(self):
        return self._position

    def compute(self):
        while True:
            time.sleep(self._clk)
            #print("Boardcomputer: making prediction")
            self.predictPosition(self._clk)
    # Kalman


if __name__ == '__main__':
    pass