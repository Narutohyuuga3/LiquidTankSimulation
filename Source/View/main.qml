import QtQuick 2.15
import QtQuick.Controls 2.15

ApplicationWindow {
    visible: true
    width: 1580
    height: 830
    title: "HelloApp"
    id: main

    property int spaceshipPosX: 500
    property int spaceshipPosY: 500
    signal keyLeft(int val)
    signal startKeyPressed(string key)
    signal stopKeyPressed(string key)
    
    function onUpdateSpaceshipPos(x, y, z) {
        spaceshipPosX = x
        spaceshipPosY = y
        //console.log("Main.qml onUpdateSpaceshipPos: x=", x, "y=", y)
    }

    Rectangle {
        anchors.fill: parent
        focus: true

        Keys.onPressed: (event)=>{
            switch (event.key){
                case Qt.Key_W:
                    startKeyPressed("w")
                    break
                case Qt.Key_S:
                    startKeyPressed("s")
                    break
                case Qt.Key_A:
                    startKeyPressed("a")
                    break
                case Qt.Key_D:
                    startKeyPressed("d")
                    break
                case Qt.Key_Q:
                    startKeyPressed("q")
                    break
                case Qt.Key_E:
                    startKeyPressed("e")
                    break
                default:
                    break
            }
        }
        Keys.onReleased: (event)=>{
            switch (event.key){
                case Qt.Key_W:
                    stopKeyPressed("w")
                    break
                case Qt.Key_S:
                    stopKeyPressed("s")
                    break
                case Qt.Key_A:
                    stopKeyPressed("a")
                    break
                case Qt.Key_D:
                    stopKeyPressed("d")
                    break
                case Qt.Key_Q:
                    stopKeyPressed("q")
                    break
                case Qt.Key_E:
                    stopKeyPressed("e")
                    break
                default:
                    break
            }
        }
    }

    Rectangle {
        id: background
        height: 800
        width: 1250
        color: "black"
    }
    Image {
        id: spaceship
        height: 50
        width: 50
        x: spaceshipPosX
        y: spaceshipPosY
        source: "qrc:/icons/spaceship.png"
        fillMode: Image.PreserveAspectFit
    }
}