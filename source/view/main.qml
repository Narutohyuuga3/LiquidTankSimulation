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
    
    property var spaceshipVarianceX: [500, 525, 550, 575, 600, 625, 650, 675, 700, 725, 750]
    property var spaceshipVarianceY: [500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500]

    property int numberPredictors: 10

    signal startKeyPressed(string key)
    signal stopKeyPressed(string key)
    signal sendInput(int numberPredictors, double updateTime, double accelVar, double measXVar, double measYVar)
    
    function onUpdateSpaceshipPos(pos, vel, meas) {
        // position
        spaceshipPosX = pos[0]
        spaceshipPosY = pos[1]
        //interface
        id_output.itemAt(0).children[0].children[0].children[1].text = Math.round(spaceshipPosX * 100) / 100
        id_output.itemAt(1).children[0].children[0].children[1].text = Math.round(spaceshipPosX * 100) / 100
        id_output.itemAt(2).children[0].children[0].children[1].text = Math.round(vel[0] * 100) / 100
        id_output.itemAt(3).children[0].children[0].children[1].text = Math.round(-1 * vel[1] * 100) / 100
        // measurment
        spaceshipMeasurepointX = meas[0]
        spaceshipMeasurepointY = meas[1]
    }

    function onUpdateSpaceshipPrediction(prediction, predictVariance) {
        // prediction
        spaceshipEstimationX = prediction[0]
        spaceshipEstimationY = prediction[1]
        spaceshipVarianceX = predictVariance[0]
        spaceshipVarianceY = predictVariance[1]
        //console.log(spaceshipVarianceX)
        //console.log("Main.qml onUpdateSpaceshipEstimation: x=", spaceshipEstimationX, "y=", spaceshipEstimationY)
        for (var i in main.spaceshipEstimationX){
            //console.log(i)
            //id_predictorRepeater.itemAt(i).x = spaceshipEstimationX[i] - id_predictorRepeater.itemAt(i).width * 0.5
            //id_predictorRepeater.itemAt(i).y = spaceshipEstimationY[i] - id_predictorRepeater.itemAt(i).height * 0.5
            
            id_predictorRepeater.itemAt(i).width = spaceshipVarianceX[i] + 1
            id_predictorRepeater.itemAt(i).height = spaceshipVarianceY[i] + 1
            id_predictorRepeater.itemAt(i).x = spaceshipEstimationX[i]- id_predictorRepeater.itemAt(i).width * 0.5 
            id_predictorRepeater.itemAt(i).y = spaceshipEstimationY[i]- id_predictorRepeater.itemAt(i).height * 0.5
            
        }
        //console.log("Main.qml onUpdateSpaceshipPos: x=", x, "y=", y)
    }

    function onGetInput(uiList) {
        console.log("onGetInput", uiList)
        id_input.itemAt(0).children[0].children[0].children[1].text = uiList[0]
        id_input.itemAt(1).children[0].children[0].children[1].text = Math.round(1000 * uiList[1]) / 1000
        id_input.itemAt(2).children[0].children[0].children[1].text = Math.round(1000 * uiList[2]) / 1000
        id_input.itemAt(3).children[0].children[0].children[1].text = Math.round(1000 * uiList[3]) / 1000
        id_input.itemAt(4).children[0].children[0].children[1].text = Math.round(1000 * uiList[4]) / 1000
        //console.log("Update: nPredict, updateTime, accelVar, measXVar, measYVar: ", nPredict, updateTime, accelVar, measXVar, measYVar)
    }

    Rectangle {
        width: parent.width
        height: parent.height
        id: id_background
        focus: true
        color: "black"

        // remove switch-case and use int-Value to identify key
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

    Rectangle{
        id: id_areaIO
        x: parent.width - width
        y: 0
        width: 200
        height: parent.height
        color: "black"
        Column {
            height: parent.height
            width: parent.width
            
            Repeater {
                id: id_input
                model: 5
                Row {
                    height: 25
                    width: parent.width
                    //Component.onCompleted: print(x, y, width, height)
                    Rectangle {
                        height: parent.height
                        width: parent.width
                        color: "white"
                        //Component.onCompleted: print("Rect: ", x, y, width, height)
                        Row{
                            spacing: 3
                            Text {
                                text: "Placeholder"
                            }
                            TextField {
                                text: "Placeholder"
                                validator: DoubleValidator{bottom: 0.0; decimals: 3}
                            }
                        }
                    }
                }
                Component.onCompleted: {
                    itemAt(0).children[0].children[0].children[0].text = "No. Predictors" // häää?
                    itemAt(0).children[0].children[0].children[1].text = "10"
                    itemAt(0).children[0].children[0].children[1].validator.decimals = 0
                    itemAt(1).children[0].children[0].children[0].text = "Updatetime [s]"
                    itemAt(1).children[0].children[0].children[1].text = "1.5"
                    itemAt(2).children[0].children[0].children[0].text = "Variance acceleration"
                    itemAt(2).children[0].children[0].children[1].text = "1" 
                    itemAt(3).children[0].children[0].children[0].text = "Variance measurement x"
                    itemAt(3).children[0].children[0].children[1].text = "2" 
                    itemAt(4).children[0].children[0].children[0].text = "Variance measurement y"
                    itemAt(4).children[0].children[0].children[1].text = "3" 
                }
            }
            
            Repeater {
                id: id_output
                model: 4
                Row {
                    height: 25
                    width: parent.width
                    //Component.onCompleted: print(x, y, width, height)
                    Rectangle {
                        height: parent.height
                        width: parent.width
                        color: "white"
                        //Component.onCompleted: print("Rect: ", x, y, width, height)
                        Row{
                            spacing: 3
                            Repeater{
                                model: 2
                                Text {
                                    text: "Placeholder"
                                }
                            }
                        }
                    }
                }
                Component.onCompleted: {
                    itemAt(0).children[0].children[0].children[0].text = "Pos X:" // häää?
                    itemAt(0).children[0].children[0].children[1].text = spaceshipPosX
                    itemAt(1).children[0].children[0].children[0].text = "Pos Y:"
                    itemAt(1).children[0].children[0].children[1].text = spaceshipPosY
                    itemAt(2).children[0].children[0].children[0].text = "Vel X:"
                    itemAt(2).children[0].children[0].children[1].text = "0"
                    itemAt(3).children[0].children[0].children[0].text = "Vel Y:"
                    itemAt(3).children[0].children[0].children[1].text = "0"
                }
            }
            Rectangle{
                width: parent.width
                height: 25
                color: "white"
                Button {
                    id: id_update
                    text: "Update"
                    onClicked: {
                        id_background.focus = true
                        var nPredict = Math.round(id_input.itemAt(0).children[0].children[0].children[1].text)
                        if (nPredict < 26){
                            nPredict = 25
                            id_input.itemAt(0).children[0].children[0].children[1].text = nPredict
                        }
                        var updateTime = id_input.itemAt(1).children[0].children[0].children[1].text
                        var accelVar = id_input.itemAt(2).children[0].children[0].children[1].text
                        var measXVar = id_input.itemAt(3).children[0].children[0].children[1].text
                        var measYVar = id_input.itemAt(4).children[0].children[0].children[1].text
                        //console.log("Update: nPredict, updateTime, accelVar, measXVar, measYVar: ", nPredict, updateTime, accelVar, measXVar, measYVar)
                        sendInput(nPredict, updateTime, accelVar, measXVar, measYVar)
                    }
                }
            }
        }
    }

    // Here everything to draw on Display
    Repeater{
        id: id_predictorRepeater
        model: 10
        Rectangle {
            height: 10
            width: 10
            //radius: width*0.5
            x: 20
            y: 20
            Canvas{
                id: id_canvas
                anchors.fill: parent
                onPaint:{
                    var ctx = id_canvas.getContext('2d');
                    ctx.reset()
                    ctx.fillStyle= "rgba(0, 0, 0, 1)"
                    ctx.fillRect(0, 0, parent.width + 1, parent.height + 1)
                    ctx.closePath()
                    
                    ctx.ellipse(1, 1, parent.width - 2, parent.height - 2)
                    ctx.fillStyle= "red"
                    ctx.fill()
                    ctx.closePath()

                    ctx.arc(parent.width * 0.5, parent.height * 0.5, 2, 0, 2*Math.PI)
                    ctx.fillStyle= "yellow"
                    ctx.fill()
                    ctx.closePath()
                }

            }
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