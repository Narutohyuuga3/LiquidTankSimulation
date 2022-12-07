import numpy as np
class kinematic():
    """
    expected inputs:
           [timeX]                                   [a_x]
    time = [timeY] = time_common [s], acceleration = [a_y] [m/s**2]
           [timeZ]                                   [a_z]
    
               [veloX]                   [x]
    velocity = [veloY] [m/s], position = [y] [m]
               [veloZ]                   [z]

             [phi]                   [w_r]
    rotPos = [theta] [rad], rotPos = [w_p] [rad/s]
             [psi]                   [w_y]

               [a_r]             r = roll, turn around x, cat roll
    rotAccel = [a_p] [rad/s**2], p = pitch, turn around y, pitcher
               [a_y]             y = yawn, turn around z, door

    Note:
    - Add jerk
    - Add tangular velocity
    """


    def velocity2position(velocity, time: float, position = np.zeros((3, 1))):
        #print('Kinematic velocity2position: x=%f.1, y=%f.1, z=%f.1' %(position[0,0],position[1,0],position[2,0]))
        return velocity * time + position

    def acceleration2velocity(acceleration, time: float, velocity = np.zeros((3, 1))):
        #print('Kinematic acceleration2velocity: x=%f.1, y=%f.1, z=%f.1' %(velocity[0,0], velocity[1,0], velocity[2,0]))
        return acceleration * time + velocity

    def acceleration2position(acceleration, time: float, velocity = np.zeros((3, 1)), position = np.zeros((3, 1))):
        return 0.5 * acceleration * time**2 + velocity * time + position
    
    def positions2velocity(currentPosition: float, deltaTime: float, previousPosition = np.zeros((3, 1))):
        return (currentPosition - previousPosition)/deltaTime

    # kombined movement of angular kinematic and kinematic
    def acceleration2velocityWBodyAngle(acceleration, rotAccel, time: float, timeRot: float, velocity = np.zeros((3, 1)), rotAngle = np.zeros((3, 1)), rotVel = np.zeros((3, 1))):
        return velocity + time * kinematic.bodyFrame2spaceFrame(rotAngle, timeRot, rotAccel, rotVel).dot(acceleration)

    def acceleration2positionWBodyAngle(acceleration, rotAccel, time: float, timeRot: float, velocity = np.zeros((3, 1)), position = np.zeros((3, 1)), rotAngle = np.zeros((3, 1)), rotVel = np.zeros((3, 1))):
        return position +  velocity * time + 0.5 * time**2 * kinematic.bodyFrame2spaceFrame(rotAngle, timeRot, rotAccel, rotVel).dot(acceleration)

    # rotation kinematic
    def rotVelocity2rotPos(rotVel, time: float, rotPos = np.zeros((3, 1))):
        return rotVel * time + rotPos

    def rotAcceleration2rotVelocity(rotAccel: float, time: float, rotVel = np.zeros((3, 1))):
        return rotAccel * time + rotVel
    
    def rotAcceleration2rotPos(rotAccel: float, time: float, rotVel = np.zeros((3, 1)), rotPos = np.zeros((3, 1))):
        return 0.5 * rotAccel * time**2 + rotVel * time + rotPos

    # body frame to space frame
    def bodyFrame2spaceFrame(rotPos: float, time: float = 0.0, rotAccel = np.zeros((3, 1)), rotVel = np.zeros((3, 1))):
        rotPos = kinematic.rotAcceleration2rotPos(rotAccel, time, rotVel, rotPos)
        
        phi = rotPos[0]
        theta = rotPos[1]
        psi = rotPos[2]
        
        sinPhi = np.sin(phi)
        cosPhi = np.cos(phi)

        sinTheta = np.sin(theta)
        cosTheta = np.cos(theta)

        sinPsi = np.sin(psi)
        cosPsi = np.cos(psi)

        conv = np.zeros((3, 3))
        
        #Rx = np.zeros((3, 3))
        #Ry = np.zeros((3, 3))
        #Rz = np.zeros((3, 3))
        #Rz[0, 0] = cosPsi
        #Rz[0, 1] = -sinPsi
        #Rz[0, 2] = 0
        #Rz[1, 0] = sinPsi
        #Rz[1, 1] = cosPsi
        #Rz[1, 2] = 0
        #Rz[2, 0] = 0
        #Rz[2, 1] = 0
        #Rz[2, 2] = 1
        #Ry[0, 0] = cosTheta
        #Ry[0, 1] = 0
        #Ry[0, 2] = sinTheta
        #Ry[1, 0] = 0
        #Ry[1, 1] = 1
        #Ry[1, 2] = 0
        #Ry[2, 0] = -sinTheta
        #Ry[2, 1] = 0
        #Ry[2, 2] = cosTheta
        #Rx[0, 0] = 1
        #Rx[0, 1] = 0
        #Rx[0, 2] = 0
        #Rx[1, 0] = 0
        #Rx[1, 1] = cosPhi
        #Rx[1, 2] = -sinPhi
        #Rx[2, 0] = 0
        #Rx[2, 1] = sinPhi
        #Rx[2, 2] = cosPhi
        #conv = Rz.dot(Ry.dot(Rx))

        conv[0, 0] = cosTheta*cosPsi
        conv[0, 1] = sinPhi*sinTheta*cosPsi-cosPhi*sinPsi
        conv[0, 2] = cosPhi*sinTheta*cosPsi+sinPhi*sinPsi
        
        conv[1, 0] = cosTheta*sinPsi
        conv[1, 1] = sinPhi*sinTheta*sinPsi+cosPhi*cosPsi
        conv[1, 2] = cosPhi*sinTheta*sinPsi-sinPhi*cosPsi

        conv[2, 0] = -sinTheta
        conv[2, 1] = sinPhi*cosTheta
        conv[2, 2] = cosPhi*cosTheta

        return conv

    # space frame to body frame
    def spaceFrame2bodyFrame(rotPos: float, time: float = 0, rotAccel = np.zeros((3, 1)), rotVel = np.zeros((3, 1))):
        rotPos = kinematic.rotAcceleration2rotPos(rotAccel, time, rotVel, rotPos)
        
        phi = rotPos[0]
        theta = rotPos[1]
        psi = rotPos[2]

        sinPhi = np.sin(phi)
        cosPhi = np.cos(phi)

        sinTheta = np.sin(theta)
        cosTheta = np.cos(theta)

        sinPsi = np.sin(psi)
        cosPsi = np.cos(psi)

        conv = np.zeros((3, 3))
        
        #Rx = np.zeros((3, 3))
        #Ry = np.zeros((3, 3))
        #Rz = np.zeros((3, 3))
        #Rx[0, 0] = 1
        #Rx[0, 1] = 0
        #Rx[0, 2] = 0
        #Rx[1, 0] = 0
        #Rx[1, 1] = cosPhi
        #Rx[1, 2] = sinPhi
        #Rx[2, 0] = 0
        #Rx[2, 1] = -sinPhi
        #Rx[2, 2] = cosPhi
        #Ry[0, 0] = cosTheta
        #Ry[0, 1] = 0
        #Ry[0, 2] = -sinTheta
        #Ry[1, 0] = 0
        #Ry[1, 1] = 1
        #Ry[1, 2] = 0
        #Ry[2, 0] = sinTheta
        #Ry[2, 1] = 0
        #Ry[2, 2] = cosTheta
        #Rz[0, 0] = cosPsi
        #Rz[0, 1] = sinPsi
        #Rz[0, 2] = 0
        #Rz[1, 0] = -sinPsi
        #Rz[1, 1] = cosPsi
        #Rz[1, 2] = 0
        #Rz[2, 0] = 0
        #Rz[2, 1] = 0
        #Rz[2, 2] = 1
        #conv = Rx.dot(Ry.dot(Rz))

        conv[0, 0] = cosTheta*cosPsi
        conv[0, 1] = cosTheta*sinPsi
        conv[0, 2] = -sinTheta

        conv[1, 0] = sinPhi*sinTheta*cosPsi-cosPhi*sinPsi
        conv[1, 1] = sinPhi*sinTheta*sinPsi+cosPhi*cosPsi
        conv[1, 2] = sinPhi*cosTheta

        conv[2, 0] = cosPhi*sinTheta*cosPsi+sinPhi*sinPsi
        conv[2, 1] = cosPhi*sinTheta*sinPsi-sinPhi*cosPsi
        conv[2, 2] = cosPhi*cosTheta

        return conv

