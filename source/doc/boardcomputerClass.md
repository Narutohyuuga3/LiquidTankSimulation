# Boardcomputer class

The boardcomputer class holds the [Kalman Filter](kalmanFilter.md), the state space model, the $n$ predictions and its deviations. It receives updates from the [Spaceship Class](spaceshipClass.md) class.

## Talbe of contents

- [Boardcomputer class](#boardcomputer-class)
  - [Talbe of contents](#talbe-of-contents)
- [1. Parameters](#1-parameters)
- [2. Methods](#2-methods)
  - [def __init__(self, spaceship: spaceship, predictPosition: int = 10, deltaT: float = 0.1):](#def-initself-spaceship-spaceship-predictposition-int--10-deltat-float--01)
  - [Getter/Setter](#gettersetter)
    - [def pos(self):](#def-posself)
    - [def vel(self):](#def-velself)
    - [def accel(self):](#def-accelself)
    - [def x(self):](#def-xself)
    - [def P(self):](#def-pself)
    - [def sigma(self):](#def-sigmaself)
    - [def predictVal(self):](#def-predictvalself)
    - [def deltaT(self):](#def-deltatself)
    - [def deltaT(self, var):](#def-deltatself-var)
    - [def nPrediction(self):](#def-npredictionself)
    - [def nPrediction(self, val: int):](#def-npredictionself-val-int)
    - [def measurePoint(self):](#def-measurepointself)
  - [Calculation Methods](#calculation-methods)
    - [def predict(self, deltaT: float, a\_input: np.ndarray, aDeviation: np.ndarray) -\> None:](#def-predictself-deltat-float-a_input-npndarray-adeviation-npndarray---none)
    - [def update(self, measPos: list, measDev: list):](#def-updateself-measpos-list-measdev-list)
    - [def compute(self, accelDev: np.ndarray = None, accel: np.ndarray = None, all: bool = False):](#def-computeself-acceldev-npndarray--none-accel-npndarray--none-all-bool--false)
    - [def predictAndFill(self, deltaT: float, a\_input: np.ndarray, a\_deviation: np.ndarray):](#def-predictandfillself-deltat-float-a_input-npndarray-a_deviation-npndarray)
- [3. Tests](#3-tests)


# 1. Parameters

State space vector 
$$x=\begin{bmatrix}
x\\
y\\
z\\
v_x\\
v_y\\
v_z\\
a_x\\
a_y\\
a_z\\
\end{bmatrix}$$

Time step $\Delta t$

Current measure point 
$$m=\begin{bmatrix}
m_x\\
m_y\\
m_z\\
\end{bmatrix}$$

Flag of new Storage $newStorageAvaible$

Covariance matrice of state $P \in \mathbb{R^{9\times 9}}$

Amount of predictions $nPredict$ as $n$

New amount of predictions $newNPredict$ as $m$

Storage of each prediction $predict$, as 2d python list with $[[x_1, ..., x_n], ..., [a_{z,1}, ..., a_{z, n}]]$

New storage of each prediction $newPredict$, as 2d python list with
$[[x_1, ..., x_m], ..., [a_{z, 1}, ..., a_{z, m}]]$

Storage of each deviation of the state space parameters of prediction $sigma$, as 2d python list with $[[\sigma_{x, 1}, ..., \sigma_{x, n}], ..., [\sigma_{az, 1}, ..., \sigma_{az, n}]]$

New storage of each deviationt of the state space parameters of prediction $newSigma$, as 2d python list with $[[\sigma_{x, 1}, ..., \sigma_{x, m}], ..., [\sigma_{az, 1}, ..., \sigma_{az, m}]]$


# 2. Methods

## def __init__(self, spaceship: spaceship, predictPosition: int = 10, deltaT: float = 0.1):
Initialize the boardcomputer. Requires [Spaceship Class](spaceshipClass.md).


## Getter/Setter

### def pos(self):
Get the position state x, y and z

### def vel(self):
Get the velocity state $v_x, v_y, v_z$

### def accel(self):
Get the acceleration state $a_x, a_y, a_z$

### def x(self):
Get the state space vector

### def P(self):
Get the covariance matrice of the state space

### def sigma(self):
Get the list of the deviation of each state space parameters

### def predictVal(self):
Get the list of predictions

### def deltaT(self):
### def deltaT(self, var):
Get/Set time step for the predictions. Input: float

### def nPrediction(self):
### def nPrediction(self, val: int):
Get/Set number of predictions. Initialize new storage with the required amount of predictions and sets flag if finished.

### def measurePoint(self):
Get current used measure point for update

## Calculation Methods

### def predict(self, deltaT: float, a_input: np.ndarray, aDeviation: np.ndarray) -> None:
Calculate the next prediction on basis of deltaT, input of acceleration and its deviation. For the used matrices and equation, see [Kalman Filter](kalmanFilter.md). Input as float and numpy array

### def update(self, measPos: list, measDev: list):
Update the [Kalman Filter](kalmanFilter.md) on basis of the measured position and its deviation. For the used equations and matrices, see [Kalman Filter](kalmanFilter.md). Inputs as 1d python list [val, val, val]

### def compute(self, accelDev: np.ndarray = None, accel: np.ndarray = None, all: bool = False):
Update the storage to fill. Delegates wheter just the next prediction is calculated of the whole list get refilled. Inputs as numpy array and boolean

### def predictAndFill(self, deltaT: float, a_input: np.ndarray, a_deviation: np.ndarray):
Calculates next prediction. Insert it at the end of the predict and sigma list.

# 3. Tests

Tests are appended but outdated. Focus of the tests was the boardcomputer and its [Kalman Filter](kalmanFilter.md) and state space model.