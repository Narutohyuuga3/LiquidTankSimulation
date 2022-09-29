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
    
    function onUpdateSpaceshipPos(x, y) {
        spaceshipPosX = x
        spaceshipPosY = y
        console.log("Main.qml onUpdateSpaceshipPos: x=", x, "y=", y)
    }

    Rectangle {
        anchors.fill: parent
        focus: true

        Keys.onLeftPressed: keyLeft(10)
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