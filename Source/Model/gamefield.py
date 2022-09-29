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

from PyQt6.QtCore import QObject, pyqtSignal, pyqtProperty


class Gamefield(QObject):

    updateSpaceshipPos = pyqtSignal(int, int)
    
    def __init__(self):
        super().__init__()

        self.gamefieldSizeX = 1250
        self.gamefieldSizeY = 800
        self.shipsize = 50
        self.spaceshipPosX = self.gamefieldSizeX/2
        self.spaceshipPosY = self.gamefieldSizeY/2

    def transmission(self):
        self.updateSpaceshipPosX.emit()

    def on_keyLeft(self, val):
        print(f'Gamefield on_keyLeft: called {val}' )
        self.spaceshipPosY-= 40
        self.updateSpaceshipPos.emit(self.spaceshipPosX ,self.spaceshipPosY)

if __name__ == '__main__':
    pass