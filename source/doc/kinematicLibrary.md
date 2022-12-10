# Kinematic Library

This library contains the functions to calculate the position, velocity on basis of the acceleration, velocity and/or position.

## Table of contents

- [Kinematic Library](#kinematic-library)
  - [Table of contents](#table-of-contents)
- [1. Methods](#1-methods)
  - [No init function](#no-init-function)
  - [Calculation](#calculation)
    - [def velocity2position(velocity: float, time: float, position: float = 0):](#def-velocity2positionvelocity-float-time-float-position-float--0)
    - [def acceleration2velocity(acceleration: float, time: float, velocity: float = 0):](#def-acceleration2velocityacceleration-float-time-float-velocity-float--0)
    - [def acceleration2position(acceleration: float, time: float, velocity: float = 0, position: float = 0):](#def-acceleration2positionacceleration-float-time-float-velocity-float--0-position-float--0)
    - [def positions2velocity(previousPosition: float, currentPosition: float, deltaTime: float):](#def-positions2velocitypreviousposition-float-currentposition-float-deltatime-float)
- [2. Tests](#2-tests)

# 1. Methods

## No init function

## Calculation

### def velocity2position(velocity: float, time: float, position: float = 0):
Calculates $x = x_0 + v\cdot\Delta t$. Inputs can be scalars of vectors. Time should be scalar.

### def acceleration2velocity(acceleration: float, time: float, velocity: float = 0):
Calculates $v = v_0 + \Delta t\cdot a$. Inputs can be scalars of vectors. Time should be scalar.

### def acceleration2position(acceleration: float, time: float, velocity: float = 0, position: float = 0):
Calculates $x = x_0 + v\cdot\Delta t + \frac{1}{2}\cdot\Delta t\cdot a$. Inputs can be scalars of vectors. Time should be scalar.
     
    
### def positions2velocity(previousPosition: float, currentPosition: float, deltaTime: float):
Calculate the average velocity between two positions. $v=\frac{x_1-x_0}{\Delta t}$. **Untested with vectors!**

# 2. Tests

None done so far. Will be appended later.