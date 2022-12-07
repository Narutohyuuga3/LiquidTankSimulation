import unittest
import numpy as np
from source.model.spaceship.spaceship import boardcomputer, spaceship
from source.model.physics.kinematic import kinematic

from matplotlib import pyplot as plt

class TestBoardcomputer(unittest.TestCase):
        
    def test_can_predict(self):
        x_init = [[0], [0], [0]]
        v_init = [[0], [0], [0]]
        a_init = [[0], [0], [0]]

        xRot_init = [[0], [0], [0]]
        vRot_init = [[0], [0], [0]]
        aRot_init = [[0], [0], [0]]
        
        checkState = np.bmat([[x_init], [v_init], [a_init], [xRot_init], [vRot_init], [aRot_init]]).reshape((18, 1))

        a_var = 0.01
        aRot_var = 0.1
        
        mass=1
        diameter=1
        heigth = 1
        boosterforce = np.array([[1, 1, 1],[1, 1, 1], [1, 1, 1]])
        
        m_spaceship = spaceship(x_init, mass, diameter, heigth, boosterforce, v_init, xRot_init, vRot_init, a_var)
        m_computer = m_spaceship.getComputer()

        deltaT = 0.01
        n = 5000
        a_input = np.array([[1], [0], [0]]).reshape((3, 1))
        aRot_input = np.array([[0], [0], [0]]).reshape((3, 1))
        
        stateList = []
        checkStateList = []
        newState = checkState

        stateList.append(m_computer.x)
        checkStateList.append(newState)

        for i in range(n):
            #if  i == 5:
            #    a_input = np.array([[0], [0], [0]]).reshape((3, 1))
            #elif i > 6:
            #    a_input = np.array([[2], [4], [8]]).reshape((3, 1))

            if i == 0:
                aRot_input = np.array([[0], [5*np.pi], [0]]).reshape((3, 1))
            else:
                aRot_input = np.array([[0], [0], [0]]).reshape((3, 1))

            m_computer.predict(deltaT, a_input, a_var, aRot_input, aRot_var)
            stateList.append(m_computer.x)
            newState = self.progressCheckState(newState, deltaT, a_input, aRot_input)
            checkStateList.append(newState)

        # plot
        time = [deltaT*i for i in range(n+1)]

        fig, ax = plt.subplots(6, 3)
        for dim in range(18):
            x = self.extractDim(stateList, dim)
            xCheck = self.extractDim(checkStateList, dim)

            ax[int(dim/3), dim%3].plot(time, x)
            ax[int(dim/3), dim%3].plot(time, xCheck)
            ax[int(dim/3), dim%3].legend(['prediction', 'checkState'])
            ax[int(dim/3), dim%3].grid()
        
        fig1 = plt.figure()
        x = self.extractDim(stateList, 0)
        xCheck = self.extractDim(checkStateList, 0)
        y = self.extractDim(stateList, 1)
        yCheck = self.extractDim(checkStateList, 1)
        z = self.extractDim(stateList, 2)
        zCheck = self.extractDim(checkStateList, 2)
        ax = plt.axes(projection= '3d')
        ax.plot3D(x, y, z)
        ax.plot3D(xCheck, yCheck, zCheck)
        ax.legend(['prediction', 'checkState'])
        plt.show()
        plt.ginput(20)
        print("Test end")

    def extractDim(self, l_list, dim):
        list = []
        for elem in l_list:
            list.append(elem[dim, 0].item())
        return list

    def progressCheckState(self, state, time, a_input, aRot_input):
        pos = kinematic.acceleration2positionWBodyAngle(a_input, aRot_input, time, time, state[3:6], state[:3], state[9:12], state[12:15])
        vel = kinematic.acceleration2velocityWBodyAngle(a_input, aRot_input, time, time, state[3:6], state[9:12], state[12:15])
        acc = kinematic.bodyFrame2spaceFrame(state[9:12], time, aRot_input, state[12:15]).dot(a_input)
        rotPos = kinematic.rotAcceleration2rotPos(aRot_input, time, state[12:15], state[9:12])
        rotVel = kinematic.rotAcceleration2rotVelocity(aRot_input, time, state[12:15])
        rotAcc = aRot_input

        return np.bmat([[pos], [vel], [acc], [rotPos], [rotVel], [rotAcc]]).reshape((18, 1))

    def test_canUpdate(self):
        return
        x=np.array([[200],[500],[0]])
        v=np.array([[0],[0],[0]])
        a=np.array([[1],[1],[0]])
        a_var = 1.2
        bc = boardcomputer(x, v, a, a, a_var)
        for i in range(10):
            bc.predict(1)


        det_before = np.linalg.det(bc.P)
        bc.update((202, 507, 0), (30.2, 45.7, 0))
        det_after = np.linalg.det(bc.P)

        self.assertLess(det_after, det_before)
        print(det_before)
        print(det_after)

    def test_canBoth(self):
        return
        a_var = 1.2
        steps = 1000
        realX = 0
        realY = 0
        realVx = 5
        realVy = 5
        realAx = 0
        realAy = -1
        m_deltaT = 0.01
        m_spaceship = spaceship(position = [realX, realY, 0], mass = 100, velocity= [realVx, realVy, 0], nPredict= steps, deltaT=m_deltaT)
        
        messVarX = 0.23
        messVarY = 0.23

        posX = []
        posY = []
        velX = []
        velY = []
        aX = []
        aY = []
        realXlist = []
        realYlist = []
        realVxlist = []
        realVylist = []
        realAx = []
        realAy = []

        m_spaceship.sendUpdate(['0', '-', '0'])
        pos = m_spaceship.getPrediction()
        posX = pos[0]
        posY = pos[1]
        velX = pos[3]
        velY = pos[4]
        aX = pos[6]
        aY = pos[7]

        plt.ion()
        plt.figure()
        plt.subplot(3, 3, 1)
        plt.title('Position X')
        plt.plot(posX, 'r')

        plt.subplot(3, 3, 2)
        plt.title('Velocity X')
        plt.plot(velX, 'r')

        plt.subplot(3, 3, 3)
        plt.title('Acceleration X')
        plt.plot(aX, 'r')


        plt.subplot(3, 3, 4)
        plt.title('Position Y')
        plt.plot(posY, 'b')

        plt.subplot(3, 3, 5)
        plt.title('Velocity Y')
        plt.plot(velY, 'b')

        plt.subplot(3, 3, 6)
        plt.title('Acceleration Y')
        plt.plot(aY, 'b')

        plt.subplot(3, 3, (7, 9))
        plt.title('Position')
        plt.plot(posX, posY, 'b')

        plt.show()
        plt.ginput(1)

        print("end")