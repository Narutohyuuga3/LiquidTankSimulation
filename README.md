# pySpace

## Table of contents

  - [1. What is it about?](#1-what-is-it-about)
    - [To do:](#to-do)
  - [2. Further ideas](#2-further-ideas)
  - [3. License](#3-license)
- [pySpace](#pyspace)
  - [Table of contents](#table-of-contents)
- [1. What is it about?](#1-what-is-it-about)
  - [To do:](#to-do)
- [2. Further ideas](#2-further-ideas)
- [3. License](#3-license)
- [About the Author](#about-the-author)
    - [Knowledge/Recently used:](#knowledgerecently-used)
      - [Basic Knowledge/Got in touch with:](#basic-knowledgegot-in-touch-with)
      - [Interests/Want to do:](#interestswant-to-do)

# 1. What is it about?

This small game emulates the Spaceship behavior in a force free space. The player can control the space ship by applying forces via booster. By using the Kalman filter, the spaceship estimates the applied force and therefore the acceleration, current velocity, position in space and the mass of the spaceship. It should predict the trajectory of the spaceship in the space. The player can collect power-ups, which increases the mass as load of the spaceship or the power of the booster. The spaceship can just measure the position directly through the radar connection to the earth. This and the applied booster have some noise.

## To do:

Goals for V1:
- [ ] UI
  - [ ] Playground
    - [x] Ship
      - [x] Real position
      - [ ] Estimation cloud
      - [ ] Transmitted position
    - [ ] Boosterflame
  - [ ] "Cockpit"-Computer view with estimated values such as
    - [ ] Position (x/y)
    - [ ] Velocity
    - [ ] Booster force
    - [ ] Graphplot with real and estimated values for:
      - [ ] Current position (x/y) vs. estimated position (x/y) over time
      - [ ] Current velocity vs. estimated velocity over time
      - [ ] Current booster power vs. estimated booster power over time
- [ ] Kernel
  - [ ] Spaceship
    - [x] Ship
    - [ ] Kalman filter/Boardcomputer
      - [ ] Position (x/y)
      - [ ] further expansion (details are coming)
  - [ ] Power Ups
    - [ ] Loads
    - [ ] Booster


# 2. Further ideas
Goals for V2:
Offer 3d Space"simulator" as own game type
- [ ] Menu
  - [ ] Offer V1
  - [ ] Add V2
- [ ] UI
  - [ ] Add 3d Game Engine (Panda3d?)
  - [ ] Playground
    -[ ] Add Planets
    -[ ] Astroids
  - [ ] Cockpit view with boardcomputer displaying estimated values such as
    - [ ] Mass/Load
    - [ ] Velocity
    - [ ] Booster force
    - [ ] Current position (x/y/z)
    - [ ] Orientation
  - [ ] Moving Graphplot to submenu
- [ ] Kernel
  - [ ] Spaceship
    - [ ] different ship types
    - [ ] Warp engine
  - [ ] Galaxies
  - [ ] Planets
    - [ ] Movement
    - [ ] Rotation
    - [ ] Gravity

Goals for V3:

Add as further mode "Orrery" where you can watch movement of Plantes just like in a **orrery** with date


- AI calculating route and auto pilot
- expand view to a 3d box (maybe Qt 3D or OpenCV/GL) (planned for V2)
- implement solar system and gravitational forces (planned for V2)
- add interstellar travelling (with fast forward) (planned for V2)

Sidenote: Imagine how awesome it would be, having a own created physic model of solar system and galaxy. Visualize it! Plus, you learning about interstellar physics.

# 3. License

This project uses the GPLv3 [License](LICENSE.md)
# About the Author


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
* Study Maxwell's Equations (<- Maybe do a numerical solver to it as project)
* Using Object Identifier/Face Recognition of OpenCV
* Linux programming
* Building small robots based on a Raspberry Pi
* Expanding knowledge in astronomy

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