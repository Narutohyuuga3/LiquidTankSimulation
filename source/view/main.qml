import QtQuick 2.15
import QtQuick.Controls 2.15

ApplicationWindow {
    visible: true
    width: 1580
    //width: 800
    height: 830
    title: "pySpace"
    id: main

    property int spaceshipPosX: 500
    property int spaceshipPosY: 500

    property var spaceshipMeasurepointX: 500
    property var spaceshipMeasurepointY: 500

    property var spaceshipEstimationX: [500, 525, 550, 575, 600, 625, 650, 675, 700, 725, 750]
    property var spaceshipEstimationY: [500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500]

    property int numberPredictors: 10

    signal keyLeft(int val)
    signal startKeyPressed(string key)
    signal stopKeyPressed(string key)
    
    function onUpdateSpaceshipPos(x, y, z) {
        spaceshipPosX = x
        spaceshipPosY = y
        //console.log("Main.qml onUpdateSpaceshipPos: x=", x, "y=", y)
    }

    function onUpdateSpaceshipEstimation(pos) {
        spaceshipEstimationX = pos[0]
        spaceshipEstimationY = pos[1]
        //console.log("Main.qml onUpdateSpaceshipEstimation: x=", spaceshipEstimationX, "y=", spaceshipEstimationY)
        for (var i in main.spaceshipEstimationX){
            //console.log(i)
            id_predictorRepeater.itemAt(i).x = spaceshipEstimationX[i] - id_predictorRepeater.itemAt(i).width * 0.5
            id_predictorRepeater.itemAt(i).y = spaceshipEstimationY[i] - id_predictorRepeater.itemAt(i).height * 0.5
        }
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
        id: id_background
        height: 800
        width: 1250
        color: "black"
    }
    
    // Here everything to draw on Display
    Repeater{
        id: id_predictorRepeater
        model: 10
        Rectangle {
            height: 10
            width: 10
            radius: width*0.5
            color: "red"
            x: 25 * (index + 1) + main.spaceshipPosX
            y: 25 * (index + 1) + main.spaceshipPosY
        }
    }

    Image {
        id: id_spaceship
        height: 40
        width: 40
        x: main.spaceshipPosX - width/2
        y: main.spaceshipPosY - height/2
        //source: "qrc:/icons/spaceship.png"
        //source: "spaceship:spaceship.png"
        source: "icon:Spaceship/spaceship.png"
        fillMode: Image.PreserveAspectFit
    }


    Rectangle {
        id: id_spaceshipRealPosition
        height: 10
        width: 10
        radius: width*0.5
        color: "green"
        x: main.spaceshipPosX - width/2
        y: main.spaceshipPosY - height/2
    }

    Rectangle {
        id: id_spaceshipMeasurement
        height: 10
        width: 10
        radius: width*0.5
        color: "blue"
        x: main.spaceshipMeasurepointX - width/2
        y: main.spaceshipMeasurepointY - height/2
    }
}