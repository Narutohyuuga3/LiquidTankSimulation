import numpy as np
from ..physics.kinematic import kinematic


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

    def __init__(self, position, mass, boosterforce, velocity, clk):
        self._boosterforce = boosterforce # [N]
        self._mass = mass # [kg]
        self._position = position # Position vector 
        self._velocity = velocity # [m/s]

    def setPosition(self, position):
        self._position = position

    def setVelocity(self, velocity):
        self._velocity = velocity

    def setMass(self, mass):
        self._mass = mass
    
    def setBoosterforce(self, boosterforce):
        self._boosterforce = boosterforce

    # getter
    def getPosition(self):
        return self._position
    
    def getEstimation(self):
        return self._boardcomputer.getEstimatedPosition()

    def getVelocity(self):
        return self._velocity

    def getAcceleration(self, dims):
        a = np.array([[0], [0], [0]])
        for idx in range(len(dims)):
            if dims[idx] == '-': 
                a[idx, 0] = -1*self._boosterforce[idx, 0]
            else:
                a[idx, 0] = self._boosterforce[idx, 1]

        return a/self._mass

    def getMass(self):
        return self._mass

    def getBoosterforce(self):
        return self._boosterforce
        
    # calculating methods
    def calcVelocity(self, time, dim):
        a = self.getAcceleration(dim)
        self._velocity = kinematic.acceleration2velocity(a, time, self._velocity)
        #print('Spaceship calculateVelocity: x=%f.1, y=%f.1, z=%f.1' %(self._velocity[0,0],self._velocity[1,0],self._velocity[2,0]))
        return self._velocity

    def calculatePosition(self, time):
        self._position = kinematic.velocity2position(self._velocity, time, self._position)
        #print('Spaceship calculatePosition: x=%f.1, y=%f.1, z=%f.1' %(self._position[0,0],self._position[1,0],self._position[2,0]))
        return self._position

class boardcomputer:
    def __init__(self, position: np.ndarray = None, velocity: np.ndarray = None, acceleration: np.ndarray = None, accelInput: np.ndarray = None,  accel_variance: float = None):
        """
        position, velocity, acceleration and accel_variance must be a 3-row vector, containing infos about x, y and z!
        """
        if position is not None and velocity is not None and acceleration is not None and accel_variance is not None and accelInput is not None:
            if position.shape == (3, 1) and  velocity.shape == (3, 1) and  acceleration.shape == (3, 1) and accelInput.shape == (3, 1): 
                # Mittelwert des Systemzustandes
                self.__x = np.bmat([[position], [velocity], [acceleration]])
                self.__a_input = accelInput
                self.__a_var = accel_variance

                # Covarianz des SS
                self.__P = np.eye(9)
            else:
                return TypeError('Dimensions are not correct!')

        else:
            return TypeError("Input types not appropiate! Check value types and content!")


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

    def predict(self, deltaT: float) -> None:
        # inspired by CppMonk
        # x = F * x + G * u
        # P = F * P * F_t + G * G_t * a
        F=np.bmat([[np.eye(3), np.eye(3)*deltaT, np.zeros((3, 3))],
                   [np.zeros((3, 3)), np.eye(3), np.zeros((3, 3))],
                   [np.zeros((3, 3)), np.zeros((3, 3)), np.zeros((3, 3))]])

        G = np.bmat([[0.5*np.eye(3)*deltaT**2],
                     [np.eye(3)*deltaT],
                     [np.eye(3)]])
                     
        new_x = F.dot(self.__x) + G.dot(self.__a_input)

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

        z = np.array([[measPos[0]],
                      [measPos[1]],
                      [measPos[2]]])

        H = np.bmat([np.eye(3), np.zeros((3, 3)), np.zeros((3, 3))])

        #print(H)
        #print(self.__x)
        y = z - H.dot(self.__x)
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

if __name__ == '__main__':
    print('23')