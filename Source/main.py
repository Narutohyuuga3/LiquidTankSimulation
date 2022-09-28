from importlib import resources
import sys

from Model import Spaceship
from Model.gamefield import Gamefield
from View import resources

from PyQt6.QtGui import QGuiApplication
from PyQt6.QtQml import QQmlApplicationEngine
from PyQt6.QtQuick import QQuickView
from PyQt6.QtCore import QUrl, QObject

def on_keyLeft():
    print("Key left pressed!")

if __name__ == '__main__':
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()
    engine.quit.connect(app.quit)
    engine.load('Source/View/main.qml')

    spaceshipPosX = 200
    spaceshipPosY = 200
    gamefield = Gamefield
    engine.rootObjects()[0].setProperty('gamefield', gamefield)

    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec())