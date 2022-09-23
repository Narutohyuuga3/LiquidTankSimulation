pySpace
=================

This small game emulates the Spaceship behavior in a force free space. The player can control the space ship by applying forces via booster. By using the Kalman filter, the spaceship estimates the applied force and therefore the acceleration, current velocity, position in space and the mass of the spaceship. The player can collect power-ups, which increases the mass as load of the spaceship or the power of the booster. The spaceship can just measure the position directly through the radar connection to the earth. This and the applied booster have some noise.

### To do:

- [ ] UI
  - [ ] Playground
  - [ ] Cockpit view with estimated values such as
    - [ ] Mass/Load
    - [ ] Velocity
    - [ ] Booster force
    - [ ] Current position (x/y)
  - [ ] Graphplot with real and estimated values for:
    - [ ] Position (x/y)
    - [ ] Velocity
    - [ ] Booster power
- [ ] Kernel
  - [ ] Kalman filter
  - [ ] Spaceship
  - [ ] Power Ups
    - [ ] Loads
    - [ ] Booster

### Further ideas

- AI calculating route


About the Authors
=================

Michael Johannes Unseld is 25 years old and study [Medical Devices](https://studium.hs-ulm.de/de/Seiten/Studiengang_MT.aspx)  at the [Ulm University of Applied Sciences](https://studium.hs-ulm.de/en) (THU). The focus of his studies is software development for Medical Devices, image acquisition and image analysis. During his internship and bachelor thesis, he has already wrote software for the [Institute for Laser Technologies in Medicine and Metrology at the University of Ulm](https://www.ilm-ulm.de/en/index.html) (ILM).

These are some software he has already realized :computer::

* :camera: Hyperspectral-Camera: Gaining images in realtime, read out their spectral data and compressed it into a three-dimensional data cube for data analysis in MATLAB.

* :camera: Optical Coherence Tomography: Control interfaces for a laser diode, spectrometer and three dimensional linear stage as probe table united in one Software. Establishing four different image acquisition procedures with their variants and a save system for data analysis afterwards.

### Knowledge/Recently used:

1. C++
2. Qt
3. MATLAB
4. CMake

#### Basic Knowledge/Got in touch with:

1. Java
2. C#
3. Python
4. OpenCV

#### Interests/Want to do:

* CUDA/GPU-Programming
* Learning Chess
* Study Maxwell's Equations
* Using Object Identifier/Face Recognition of OpenCV
* Linux programming
* Building small robots based on a Raspberry Pi

``` C++
void WorkLifeBalance() {
  do {
    doSleep();
    startWork();
    while(work) {
      if(coffee == CoffeeState::empty) {
        getCoffee();
      }
    }
  } while(isAlive == true);
}
```