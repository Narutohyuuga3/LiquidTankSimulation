# Spaceship class

The spaceship class describes the parameters of the spaceship and handle the position calculation. It posesses the real position x, y and z and the velocity vx, vy and vz. It also has the [boardcomputer](boardcomputerClass.md), which manages the [Kalman Filter](kalmanFilter.md) model. It uses the numpy-library of python and [Kinematic Library](kinematicLibrary.md).

## Table of contents

- [Spaceship class](#spaceship-class)
  - [Table of contents](#table-of-contents)
- [1. Variables](#1-variables)
- [2. Methods](#2-methods)
  - [def __init__(self, position: list = \[0, 0, 0\], mass: int = 1000, boosterforce: list = \[\[100, 100\], \[100, 100\], \[100, 100\]\], velocity: list = \[0, 0, 0\], boosterforceDev: list = \[10.3, 10.3, 10.3\], nPredict: int = 10, deltaT: float = 0.1):](#def-initself-position-list--0-0-0-mass-int--1000-boosterforce-list--100-100-100-100-100-100-velocity-list--0-0-0-boosterforcedev-list--103-103-103-npredict-int--10-deltat-float--01)
  - [Getter/Setter](#gettersetter)
    - [def setPosition(self, position):](#def-setpositionself-position)
    - [def getPositionList(self):](#def-getpositionlistself)
    - [def getPosition(self):](#def-getpositionself)
    - [def setVelocity(self, velocity):](#def-setvelocityself-velocity)
    - [def getVelocityList(self):](#def-getvelocitylistself)
    - [def getVelocity(self):](#def-getvelocityself)
    - [def setMass(self, mass):](#def-setmassself-mass)
    - [def getMass(self):](#def-getmassself)
    - [def setBoosterforce(self, boosterforce):](#def-setboosterforceself-boosterforce)
    - [def getBoosterforce(self):](#def-getboosterforceself)
    - [def getAcceleration(self, dims):](#def-getaccelerationself-dims)
    - [def setBoosterforceDeviation(self, var):](#def-setboosterforcedeviationself-var)
    - [def getBoosterforceDeviation(self):](#def-getboosterforcedeviationself)
    - [def getBoosterforceDeviationList(self):](#def-getboosterforcedeviationlistself)
    - [def setDeltaT(self, var):](#def-setdeltatself-var)
    - [def getDeltaT(self):](#def-getdeltatself)
    - [def setNPrediction(self, val):](#def-setnpredictionself-val)
    - [def getNPrediction(self):](#def-getnpredictionself)
    - [def getMeasurePoint(self):](#def-getmeasurepointself)
    - [def getMeasurePointList(self):](#def-getmeasurepointlistself)
    - [def getPrediction(self):](#def-getpredictionself)
    - [def getDeviation(self):](#def-getdeviationself)
  - [Calculation methods](#calculation-methods)
    - [def calculatePosition(self, time, dim):](#def-calculatepositionself-time-dim)
    - [def sendCompute(self, dims: list, all: bool = False):](#def-sendcomputeself-dims-list-all-bool--false)
    - [def sendUpdate(self, dims: list, measureDeviation: list = \[40, 40, 0\]):](#def-sendupdateself-dims-list-measuredeviation-list--40-40-0)
- [3. Tests](#3-tests)


# 1. Variables

Position
$$x=\begin{bmatrix}
x\\
y\\
z
\end{bmatrix}$$

Velocity 
$$v=\begin{bmatrix}
v_x\\
v_y\\
v_z
\end{bmatrix}$$

The parameters for the boosterforce are split into the positive and negative direction of of a dimension. Their values are absolute values!

Boosterforce
$$bf=\begin{bmatrix}
-F_x & +F_x\\
-F_y & +F_y\\
-F_z & +F_z
\end{bmatrix}$$

Boosterforce deviation
$$bfd=\begin{bmatrix}
\sigma_{Fx}\\
\sigma_{Fy}\\
\sigma_{Fz}
\end{bmatrix}$$

It will be soon changed to
$$bfd=\begin{bmatrix}
-\sigma_{Fx} & +\sigma_{Fx} \\
-\sigma_{Fy} & +\sigma_{Fy} \\
-\sigma_{Fz} & +\sigma_{Fz} 
\end{bmatrix}$$
to make it dimension direction dependend

Mass $m$

The acceleration can by calculated by $a = \frac{F}{m}$

For input purposes:

$dims$ is a python list and describes in which dimension the spaceship was steered. Is posses the following possible values +, - and else.

$dims = [dim_x, dim_y, dim_z]$

[$boardcomputer$](boardcomputerClass.md) is a own class for managing the predictions, its deviations and also the [Kalman Filter](kalmanFilter.md) update and prediction process.

# 2. Methods

## def __init__(self, position: list = [0, 0, 0], mass: int = 1000, boosterforce: list = [[100, 100], [100, 100], [100, 100]], velocity: list = [0, 0, 0], boosterforceDev: list = [10.3, 10.3, 10.3], nPredict: int = 10, deltaT: float = 0.1):
Initilize the variables of the spaceship. nPredict and deltaT are for the [boardcomputer](boardcomputerClass.md).

## Getter/Setter
### def setPosition(self, position):
### def getPositionList(self):
### def getPosition(self):
Set/Returns the position of the spaceship. Input: 2d python list [[val], [val], [val]]. Returns either as numpy array of as python list.

### def setVelocity(self, velocity):
### def getVelocityList(self):
### def getVelocity(self):
Set/Returns the position of the spaceship. Input: 2d python list [[val], [val], [val]]. Returns either as numpy array of python list.

### def setMass(self, mass):
### def getMass(self):
Set/Returns the mass of the spaceship.

### def setBoosterforce(self, boosterforce):
### def getBoosterforce(self):
Set/Returns the position of the spaceship. Input: 2d python list [[val, val], [val, val], [val, val]]. Returns either as numpy array.

### def getAcceleration(self, dims):
Returns the acceleration for each dimension(x/y/z) dependen from the entry (+/-/else) in dims.

### def setBoosterforceDeviation(self, var):
### def getBoosterforceDeviation(self):
### def getBoosterforceDeviationList(self):
Set/Returns vector of deviation of boosterforce. Input: 2d python list [[val], [val], [val]]. Returns either as python list of numpy array.

### def setDeltaT(self, var):
### def getDeltaT(self):
Set/returns the time step for the predictions from [boardcomputer](boardcomputerClass.md).
    
### def setNPrediction(self, val):
### def getNPrediction(self):
Set and returns the number of predictions. Transmitt it to [boardcomputer](boardcomputerClass.md). See doc to [boardcomputer](boardcomputerClass.md).

### def getMeasurePoint(self):
### def getMeasurePointList(self):
Returns the transmitted position to the [boardcomputer](boardcomputerClass.md) for the update step either as numpy array or python list.

### def getPrediction(self):
### def getDeviation(self):
Returns the list of predictions or their deviation to each prediction from the [boardcomputer](boardcomputerClass.md).

## Calculation methods

### def calculatePosition(self, time, dim):
Calculate and update spaceship position and velocity for each dimenstion x, y and z. Inputs: time as float and dim as 1d python list [val, val, val]. It uses the [Kinematic Library](kinematicLibrary.md) for it.

### def sendCompute(self, dims: list, all: bool = False):
Send command to [boardcomputer](boardcomputerClass.md) to calculate next prediction or recalculate all predictions.

### def sendUpdate(self, dims: list, measureDeviation: list = [40, 40, 0]):
Send update command to [boardcomputer](boardcomputerClass.md). Updates [Kalman Filter](kalmanFilter.md) and state space model. Inputs: dims as 1d python list [val, val, val] and measurment deviation as 1d python list [val, val, val]. Applies the deviation with gauss function of numpy to real position and send it with the deviation and the current acceleration and its deviation to the [boardcomputer](boardcomputerClass.md) to update and predict.

# 3. Tests

Tests are appended but outdated. Focus of the tests was the [boardcomputer](boardcomputerClass.md) and its [Kalman Filter](kalmanFilter.md) and state space model.