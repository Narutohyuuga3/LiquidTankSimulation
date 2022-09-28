"""
Manage gamefield
initialise spaceship
have it's real position
    - posX
    - posY
    - angle (calculating deltaX and deltaY and verctor orientation)
    - velocity (deltaX and deltaY and "onboard time")
    - boostpower (includes acceleration)
    - mass
transmit spaceship "measured" data from earthstation
    by applying a random factor between 0.9 to 1.1 on folowing parameters
    - posX
    - posY
    for easiness, it is estimated, that the transmission is perfectly timed every 1s
"""

from PyQt6.QtCore import QObject, pyqtSignal
@QObject
class Gamefield(QObject):
    updateSpaceshipPosX = pyqtSignal(int, arguments=['spaceshipPosX'])
    updateSpaceshipPosY = pyqtSignal(int, arguments=['spaceshipPosY'])

    def __init__(self):
        gamefieldSizeX = 1250
        gamefieldSizeY = 800
        shipsize = 50
        shipPosX = gamefieldSizeX/2
        shipPosY = gamefieldSizeY/2

    def transmission(self):
        self.updateSpaceshipPosX.emit()

    @Slot()
    def on_keyLeft():
        print("Key left pressed!")




if __name__ == '__main__':
    pass