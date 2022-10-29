import unittest
import numpy as np
from source.model.spaceship.spaceship import boardcomputer, spaceship
from source.model.physics.kinematic import kinematic

from matplotlib import pyplot as plt

class TestBoardcomputer(unittest.TestCase):
    def test_findTest(self):
        self.assertAlmostEqual(3, 3)

    def test_can_construct_with_x_v_and_a(self):
        x=np.array([[200],[500],[0]])
        v=np.array([[0],[0],[0]])
        a=np.array([[0],[0],[0]])
        aVar = 1.2
        bc = boardcomputer(x, v, a, a, aVar)
        
        pos = bc.pos
        self.assertAlmostEqual(pos.shape, (3, 1))
        
        vel = bc.vel
        self.assertAlmostEqual(vel.shape, (3, 1))
        
        accel = bc.accel
        self.assertAlmostEqual(accel.shape, (3, 1))
        
        if not np.array_equal(pos, x):
            return False
        if not np.array_equal(vel, v):
            return False
        if not np.array_equal(accel, a):
            return False

    def test_canFindMismatchedInput(self):
        position = np.array([[3], [2], [1]])
        velocity = np.array([[3], [2], [1]])
        acceleration = np.array([[3], [2], [1]])
        accelerationVar = 1.2

        try:
            boardcomputer(position[0:2], velocity, acceleration, acceleration, accelerationVar)
            return False
        except TypeError as e:
            print(e)
            print('test_mismatchedInput: Prove for vectorsize successful!')

        try:
            boardcomputer(position, velocity, acceleration, acceleration, accelerationVar)
            return False
        except TypeError as e:
            print(e)
            print('test_mismatchedInput: Prove for missing vector successful!')

        
    def test_can_predict(self):
        x=np.array([[200],[500],[0]])
        v=np.array([[0],[0],[0]])
        a=np.array([[0],[0],[0]])
        a_var = 1.2
        bc = boardcomputer(x, v, a, a, a_var)

        self.assertEqual(bc.P.shape, (9, 9))
        self.assertEqual(bc.x.shape, (9, 1))

        bc.predict(deltaT=0.1)
        self.assertEqual(bc.P.shape, (9, 9))
        self.assertEqual(bc.x.shape, (9, 1))
        
        # check if prediction matches physics
        bc1 = boardcomputer(x, v, a, a, a_var)
        pos_before = bc1.pos
        vel_before = bc1.vel
        accel_before = bc1.accel
        print('Initial state:')
        print('pos:')
        print(pos_before)
        print('compare model:')
        print(x)

        print('vel:')
        print(vel_before)
        print('compare model:')
        print(v)

        print('accel:')
        print(accel_before)
        print('compare model:')
        print(a)
        
        if not np.array_equal(pos_before, x):
            return False    
        if not np.array_equal(vel_before, v):
            return False
        if not np.array_equal(accel_before, a):
            return False

        for i in range(10):
            p = bc1.P
            det_before = np.linalg.det(p)
            pos_before = bc1.pos
            vel_before = bc1.vel
            accel_before = bc1.accel

            bc1.predict(0.1)
            p = bc1.P
            det_after = np.linalg.det(p)
            print('===================')
            print(f'Det before: {det_before}')
            print(f'Det after: {det_after}')
            self.assertGreater(det_after, det_before)

            pos_after = bc1.pos
            vel_after = bc1.vel
            accel_after = bc1.accel

            # check value by another model

            x = kinematic.acceleration2position(a, 0.1, v, x)
            v = kinematic.acceleration2velocity(a, 0.1, v)

            print('-------------------')
            print('pos:')
            print(pos_before)
            print('after:')
            print(pos_after)
            print('compare model:')
            print(x)

            print('vel:')
            print(vel_before)
            print('after:')
            print(vel_after)
            print('compare model:')
            print(v)

            print('accel:')
            print(accel_before)
            print('after:')
            print(accel_after)
            print('compare model:')
            print(a)
            
            p_after = bc1.P
            print('uncertainty X: +/-%f.1' % (np.sqrt(p_after[0, 0])))
            print('uncertainty Y: +/-%f.1' % (np.sqrt(p_after[1, 1])))
            print('uncertainty velX: +/-%f.1' % (np.sqrt(p_after[3, 3])))
            print('uncertainty velY: +/-%f.1' % (np.sqrt(p_after[4, 4])))
            
        
        if not np.array_equal(pos_after, x):
            return False    
        if not np.array_equal(vel_after, v):
            return False
        if not np.array_equal(accel_after, a):
            return False

    def test_canUpdate(self):
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