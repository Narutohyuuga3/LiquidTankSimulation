import sys

from model.gamefield import gamefield
from view import resources

from PyQt6.QtGui import QGuiApplication
from PyQt6.QtQml import QQmlApplicationEngine
from PyQt6.QtCore import QTimer

class MainWindow(QQmlApplicationEngine):
    def __init__(self, gamefield):
        self._field = gamefield
        QQmlApplicationEngine.__init__(self)
        self.quit.connect(app.quit)
        self.load('Source/View/main.qml')

    def exit(self, event):
        print("Mainwindow exit: called")
        self._field.__del__()
        

if __name__ == '__main__':
    app = QGuiApplication(sys.argv)

    spaceshipPosX = 200
    spaceshipPosY = 200
    field = gamefield()
    engine = MainWindow(field)

    engine.rootObjects()[0].setProperty('gamefield', field)
    root = engine.rootObjects()[0]
    root.startKeyPressed.connect(field.on_keyPressed)
    root.stopKeyPressed.connect(field.on_keyReleased)
    field.updateSpaceshipPos.connect(root.onUpdateSpaceshipPos)
    field.updateSpaceshipEstimation.connect(root.onUpdateSpaceshipEstimation)
    field.updateSpaceshipMeasurepoint.connect(root.onUpdateSpaceshipMeasurepoint)
    app.lastWindowClosed.connect(field.__del__)

    timer = QTimer()
    timer.timeout.connect(lambda: None)
    timer.start(100)


    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec())