import QtQuick 2.15
import QtQuick.Controls 2.15

ApplicationWindow {
    visible: true
    width: 1580
    height: 830
    title: "HelloApp"
    id: main

    Rectangle{
        id: background
        height: 800
        width: 1250
        color: "black"
    }
    Image{
        id: spaceship
        height: 50
        width: 50
        source: "qrc:/icons/spaceship.png"
    }
}