import QtQuick 2.15
import QtQuick.Controls 2.15

ApplicationWindow {
    visible: true
    width: 1580
    height: 830
    title: "pySpace"
    id: main

    property int spaceshipPosX: 500
    property int spaceshipPosY: 500

    property int spaceshipEstimationX: 500
    property int spaceshipEstimationY: 500

    property int spaceshipMeasurepointX: 500
    property int spaceshipMeasurepointY: 500

    signal keyLeft(int val)
    signal startKeyPressed(string key)
    signal stopKeyPressed(string key)
    
    function onUpdateSpaceshipPos(x, y, z) {
        spaceshipPosX = x
        spaceshipPosY = y
        //console.log("Main.qml onUpdateSpaceshipPos: x=", x, "y=", y)
    }
    function onUpdateSpaceshipEstimation(x, y, z) {
        spaceshipEstimationX = x
        spaceshipEstimationY = y
        //console.log("Main.qml onUpdateSpaceshipEstimation: x=", x, "y=", y)
    }
    function onUpdateSpaceshipMeasurepoint(x, y, z) {
        spaceshipMeasurepointX = x
        spaceshipMeasurepointY = y
        //console.log("Main.qml onUpdateSpaceshipMeasurepoint: x=", x, "y=", y)
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
        height: 40
        width: 40
        x: spaceshipPosX - width/2
        y: spaceshipPosY - height/2
        source: "qrc:/icons/spaceship.png"
        fillMode: Image.PreserveAspectFit
    }
    Rectangle {
        id: spaceshipRealPosition
        height: 10
        width: 10
        radius: width*0.5
        color: "green"
        x: spaceshipPosX - width/2
        y: spaceshipPosY - height/2
    }
    Rectangle {
        id: spaceshipEstimation
        height: 10
        width: 10
        radius: width*0.5
        color: "red"
        x: spaceshipEstimationX - width/2
        y: spaceshipEstimationY - height/2
    }
    Rectangle {
        id: spaceshipMeasurement
        height: 10
        width: 10
        radius: width*0.5
        color: "blue"
        x: spaceshipMeasurepointX - width/2
        y: spaceshipMeasurepointY - height/2
    }
}