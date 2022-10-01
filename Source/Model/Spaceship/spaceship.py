import numpy as np
"""
Shape of vals
            [x]                 [v_x]
position =  [y] [m], velocity = [v_y] [m/s]
            [z]                 [v_z]

                [(F_x), (F_-x)]
boosterforce =  [(F_y), (F_-y)] [m/s**2]
                [(F_z), (t_-z)]

boosterforce is absolute.

mass = [m] [kg]
the orientation of spaceship in space is the last valid non-zero
    velcocity vector
"""
class spaceship:
    _mass = None
    _boosterforce = None
    _position = None
    _velocity = None

    def __init__(self, position, mass, boosterforce, velocity):
        self._boosterforce = boosterforce # [N]
        self._mass = mass # [kg]
        self._position = position # Position vector 
        self._velocity = velocity # [m/s]

    def setPosition(self, val):
        """
        expected input
                   [posX]
        position = [posY] [m]
                   [posZ]
        """

    def setVelocity(self, val):
        """
        expected input
                   [veloX]
        velocity = [veloY] [m/s]
                   [veloZ]
        """

    def setMass(self, mass):
        """
        expected input
        mass [kg]
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
        return self._position
    
    def getVelocity(self):
        """
        returns
                   [veloX]
        velocity = [veloY] [m/s]
                   [veloZ]
        """
        return self._velocity

    def getAcceleration(self, dim):
        """
        expected input
        dim = [(dimX) (dimY) (dimZ)]

        returns
                       [accelX]
        acceleration = [accelY] [m/s**2]
                       [accelZ]
        """
        accelX = self._getAccelVal(0, dim)
        accelY = self._getAccelVal(1, dim)
        accelZ = self._getAccelVal(2, dim)
        
        accel = np.array([[accelX], [accelY], [accelZ]])/self._mass
        return accel

    def _getAccelVal(self, idx, dim):
        if dim[idx] == '-': 
            return -1*self._boosterforce[idx, 0]
        else:
            return self._boosterforce[idx, 1]

    def getMass(self):
        return self._mass

    def getBoosterforce(self):
        return self._boosterforce
        
    # calculating methods
    def calcVelocity(self, time, dim):
        """
        expected input:
               [timeX]
        time = [timeY] [s], dim =[(dimX) (dimY) (dimZ)]
               [timeZ]
        
        returns
                   [veloX]
        velocity = [veloY] [m/s]
                   [veloZ]
        """

        accel = self.getAcceleration(dim)
        self._velocity = accel * time + self._velocity
        #print('Spaceship calculateVelocity: x=%f.1, y=%f.1, z=%f.1' %(self._velocity[0,0],self._velocity[1,0],self._velocity[2,0]))
        return self._velocity

    def calculatePosition(self, time):
        self._position = self._velocity * time + self._position
        #print('Spaceship calculatePosition: x=%f.1, y=%f.1, z=%f.1' %(self._position[0,0],self._position[1,0],self._position[2,0]))
        return self._position


if __name__ == '__main__':
    pass