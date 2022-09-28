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
    property QtObject gamefield

    Connections {
        target: gamefield

        function onUpdated(x, y) {
            spaceshipPosX = x
            spaceshipPosY = y
        }
    }

    Item {
        anchors.fill: parent
        focus: true
        Keys.onLeftPressed: (event)=>{
            if (event.key == Qt.Key_Left) {
                gamefield.on_keyLeft()
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