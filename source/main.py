import sys

from model.gamefield import gamefield
from view import resources

from PyQt6.QtGui import QGuiApplication
from PyQt6.QtQml import QQmlApplicationEngine
from PyQt6.QtCore import QTimer, QDir

class MainWindow(QQmlApplicationEngine):
    def __init__(self, gamefield):
        self._field = gamefield
        QQmlApplicationEngine.__init__(self)
        self.quit.connect(app.quit)
        self.load('source/view/main.qml')

    def exit(self, event):
        print("Mainwindow exit: called")
        self._field.__del__()
        
def initResources(dir):
    #dir.addSearchPath('spaceship', 'source/view/img/Spaceship')
    dir.addSearchPath('icon', 'source/view/img')
    pass

if __name__ == '__main__':
    
    #dir = QDir
    dir = QDir()
    initResources(dir)
    #QDir.addSearchPath('icon', 'source/view/img')

    app = QGuiApplication(sys.argv)

    spaceshipPosX = 200
    spaceshipPosY = 200
    field = gamefield()
    engine = MainWindow(field)
    
    
    engine.rootObjects()[0].setProperty('gamefield', field)
    root = engine.rootObjects()[0]
    root.startKeyPressed.connect(field.on_keyPressed)
    root.stopKeyPressed.connect(field.on_keyReleased)
    #root.sendInput.connect(field.on_input)

    #field.updateInput.connect(root.onGetInput)
    field.updatePrediction.connect(root.onUpdateSpaceshipPrediction)
    field.updateSpaceshipPos.connect(root.onUpdateSpaceshipPos)
    app.lastWindowClosed.connect(field.__del__)

    timer = QTimer()
    timer.timeout.connect(lambda: None)
    timer.start(100)


    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec())