import unittest
import numpy as np
from source.model.physics.kinematic import kinematic
import matplotlib
import copy

class TestKinematic(unittest.TestCase):
    def test_rotationMatrix(self):
        alpha = np.array([[0], [0], [0]])
        omega = copy.deepcopy(alpha)
        theta = copy.deepcopy(omega)
        
        bodyFrame = np.array([[1], [1], [1]])

        conversion = kinematic.bodyFrame2spaceFrame(theta, 0, alpha, omega)
        spaceFrame = conversion.dot(bodyFrame)
        
        #expected = np.array([[1], [1], [1]])
        #if self.checkInputAndExpectedBody2space(theta, bodyFrame, expected) == False:
        #    self.assertFalse("Case 1")
        #
        #theta = np.array([[np.pi], [np.pi], [np.pi]])
        #expected = np.array([[1], [1], [1]])
        #if self.checkInputAndExpectedBody2space(theta, bodyFrame, expected) == False:
        #    self.assertFalse("Case 2")
#
        #theta = np.array([[np.pi], [0], [0]])
        #expected = np.array([[1], [-1], [-1]])
        #if self.checkInputAndExpectedBody2space(theta, bodyFrame, expected) == False:
        #    self.assertFalse("Case 3")
        #
        #theta = np.array([[0], [np.pi], [0]])
        #expected = np.array([[-1], [1], [-1]])
        #if self.checkInputAndExpectedBody2space(theta, bodyFrame, expected) == False:
        #    self.assertFalse("Case 4")
#
        #theta = np.array([[0], [0], [np.pi]])
        #expected = np.array([[-1], [-1], [1]])
        #if self.checkInputAndExpectedBody2space(theta, bodyFrame, expected) == False:
        #    self.assertFalse("Case 5")


        theta = np.array([[0], [0], [np.pi]])
        expected = np.array([[-1], [1], [1]])
        if self.checkInputAndExpectedBody2space(theta, bodyFrame, expected) == False:
            self.assertFalse("Case")
        
        theta = np.array([[0], [0], [(3 * np.pi)/2]])
        expected = np.array([[-1], [-1], [1]])
        if self.checkInputAndExpectedBody2space(theta, bodyFrame, expected) == False:
            self.assertFalse("Case")




        # reverse
        #spaceFrame = np.array([[1], [1], [1]])
        #theta = np.array([[0], [0], [0]])
        #expected = np.array([[1], [1], [1]])
        #if self.checkInputAndExpectedSpace2body(theta, spaceFrame, expected) == False:
        #    self.assertFalse("Case 6")
        #
        #theta = np.array([[np.pi], [np.pi], [np.pi]])
        #expected = np.array([[1], [1], [1]])
        #if self.checkInputAndExpectedSpace2body(theta, spaceFrame, expected) == False:
        #    self.assertFalse("Case 7")
        #
        #theta = np.array([[np.pi], [0], [0]])
        #expected = np.array([[1], [-1], [-1]])
        #if self.checkInputAndExpectedSpace2body(theta, spaceFrame, expected) == False:
        #    self.assertFalse("Case 8")
        #
        #theta = np.array([[0], [np.pi], [0]])
        #expected = np.array([[-1], [1], [-1]])
        #if self.checkInputAndExpectedSpace2body(theta, spaceFrame, expected) == False:
        #    self.assertFalse("Case 9")
#
        #theta = np.array([[0], [0], [np.pi]])
        #expected = np.array([[-1], [-1], [1]])
        #if self.checkInputAndExpectedSpace2body(theta, spaceFrame, expected) == False:
        #    self.assertFalse("Case 10")
        

    def checkInputAndExpectedSpace2body(self, theta, spaceFrame, expected):
        bodyFrame = kinematic.spaceFrame2bodyFrame(theta, 0).dot(spaceFrame)
        np.testing.assert_almost_equal(bodyFrame, expected, 5)

    def checkInputAndExpectedBody2space(self, theta, bodyFrame, expected):
        spaceFrame = kinematic.bodyFrame2spaceFrame(theta, 0).dot(bodyFrame)
        np.testing.assert_almost_equal(spaceFrame, expected, 5)