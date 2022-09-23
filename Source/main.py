from importlib import resources
import sys

from Model import Spaceship
from View import resources

from PyQt6.QtGui import QGuiApplication
from PyQt6.QtQml import QQmlApplicationEngine

app = QGuiApplication(sys.argv)

engine = QQmlApplicationEngine()
engine.quit.connect(app.quit)
engine.load('Source/View/main.qml')

sys.exit(app.exec())