import sys

from Model.gamefield import Gamefield
from View import resources

from PyQt6.QtGui import QGuiApplication
from PyQt6.QtQml import QQmlApplicationEngine

def on_keyLeft():
    print("Key left pressed!")

if __name__ == '__main__':
    app = QGuiApplication(sys.argv)

    engine = QQmlApplicationEngine()
    engine.quit.connect(app.quit)
    engine.load('Source/View/main.qml')

    spaceshipPosX = 200
    spaceshipPosY = 200
    gamefield = Gamefield()
    engine.rootObjects()[0].setProperty('gamefield', gamefield)
    root = engine.rootObjects()[0]
    root.startKeyPressed.connect(gamefield.on_keyPressed)
    root.stopKeyPressed.connect(gamefield.on_keyReleased)
    gamefield.updateSpaceshipPos.connect(root.onUpdateSpaceshipPos)
    gamefield.updateSpaceshipEstimation.connect(root.onUpdateSpaceshipEstimation)
    gamefield.updateSpaceshipMeasurepoint.connect(root.onUpdateSpaceshipMeasurepoint)

    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec())