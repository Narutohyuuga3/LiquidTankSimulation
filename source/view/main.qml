import QtQuick
import QtQuick.Controls
//import QtCharts



ApplicationWindow {
    visible: true
    width: 1580
    height: 830
    title: "pySpace"

    signal startKeyPressed(string key)
    signal stopKeyPressed(string key)
    signal sendInput(int numberPredictors, double updateTime, double boosterforceDevX, double boosterforceDevY, double measXDev, double measYDev, int mass, double boosterforceNegX, double boosterforcePosX, double boosterforceNegY, double boosterforcePosY)
    
    function onUpdateSpaceshipPos(pos, vel, meas) {
        // position
        id_spaceship.x = pos[0] - id_spaceship.width * 0.5
        id_spaceship.y = pos[1] - id_spaceship.height * 0.5
        //interface
        id_output.itemAt(0).children[0].children[0].children[1].text = Math.round(id_spaceship.x * 100) / 100
        id_output.itemAt(1).children[0].children[0].children[1].text = Math.round(id_spaceship.y * 100) / 100
        id_output.itemAt(2).children[0].children[0].children[1].text = Math.round(vel[0] * 100) / 100
        id_output.itemAt(3).children[0].children[0].children[1].text = Math.round(-1 * vel[1] * 100) / 100
        // measurment
        id_spaceshipMeasurement.x = meas[0] - id_spaceshipMeasurement.width * 0.5
        id_spaceshipMeasurement.y = meas[1] - id_spaceshipMeasurement.height * 0.5
    }

    function onUpdateSpaceshipPrediction(prediction, predictDeviation) {
        // prediction
        var l_spaceshipEstimationX = prediction[0]
        var l_spaceshipEstimationY = prediction[1]
        var l_spaceshipDeviationX = predictDeviation[0]
        var l_spaceshipDeviationY = predictDeviation[1]
        //console.log("Main.qml->onUpdateSpaceshipPrediction: Prediction input-array length: ", prediction[0].length)
        //console.log("Main.qml->onUpdateSpaceshipPrediction: PredictionDeviation input-array: ", predictDeviation)
        //console.log("Main.qml->onUpdateSpaceshipEstimation: position    estimation length: ", predictDeviation[0].length)
        //console.log("Main.qml->onUpdateSpaceshipEstimation: x=", l_spaceshipEstimationX, "y=", l_spaceshipEstimationY)
        for (var i=0; i < id_predictorRepeater.model; i++){
            id_predictorRepeater.itemAt(i).visible = false
        }
        for (var i in l_spaceshipEstimationX){
            id_predictorRepeater.itemAt(i).visible = true
            //console.log("Main.qml->onUpdateSpaceshipEstimation: index i: "i)
            //id_predictorRepeater.itemAt(i).x = l_spaceshipEstimationX[i] - id_predictorRepeater.itemAt(i).width * 0.5
            //id_predictorRepeater.itemAt(i).y = l_spaceshipEstimationY[i] - id_predictorRepeater.itemAt(i).height * 0.5
            
            id_predictorRepeater.itemAt(i).width = l_spaceshipDeviationX[i] + 1
            id_predictorRepeater.itemAt(i).height = l_spaceshipDeviationY[i] + 1
            id_predictorRepeater.itemAt(i).x = l_spaceshipEstimationX[i]- id_predictorRepeater.itemAt(i).width * 0.5 
            id_predictorRepeater.itemAt(i).y = l_spaceshipEstimationY[i]- id_predictorRepeater.itemAt(i).height * 0.5
            
        }
        //console.log("Main.qml->onUpdateSpaceshipPos: x=", x, "y=", y)
    }

    function onGetInput(uiList) {
        //console.log("Main.qml->onGetInput", uiList)
        id_input.itemAt(0).children[0].children[0].children[1].text = uiList[0]
        id_input.itemAt(1).children[0].children[0].children[1].text = Math.round(1000 * uiList[1]) / 1000
        id_input.itemAt(2).children[0].children[0].children[1].text = Math.round(1000 * uiList[2]) / 1000
        id_input.itemAt(3).children[0].children[0].children[1].text = Math.round(1000 * uiList[3]) / 1000
        id_input.itemAt(4).children[0].children[0].children[1].text = Math.round(1000 * uiList[4]) / 1000
        id_input.itemAt(5).children[0].children[0].children[1].text = Math.round(1000 * uiList[5]) / 1000
        id_input.itemAt(6).children[0].children[0].children[1].text = Math.round(1000 * uiList[6]) / 1000
        id_inBoosterforce.itemAt(0).children[0].children[0].children[1].text = Math.round(1000 * uiList[6]) / 1000
        id_inBoosterforce.itemAt(0).children[0].children[0].children[3].text = Math.round(1000 * uiList[7]) / 1000
        id_inBoosterforce.itemAt(1).children[0].children[0].children[1].text = Math.round(1000 * uiList[8]) / 1000
        id_inBoosterforce.itemAt(1).children[0].children[0].children[3].text = Math.round(1000 * uiList[9]) / 1000
        //console.log("Main.qml->onGetInput: Update: nPredict, updateTime, accelDev, measXDev, measYDev: ", nPredict, updateTime, accelVar, measXVar, measYVar)
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
        width: 300
        height: parent.height
        color: "black"
        Column {
            height: parent.height
            width: parent.width
            
            Repeater {
                id: id_input
                model: 7
                Row {
                    height: 25
                    width: parent.width
                    //Component.onCompleted: print("Main.qml->Repeater Input: "x, y, width, height)
                    Rectangle {
                        height: parent.height
                        width: parent.width
                        color: "white"
                        //Component.onCompleted: print("Main.qml->Rect Input: ", x, y, width, height)
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
                    itemAt(0).children[0].children[0].children[0].text = "No. Predictors"
                    itemAt(0).children[0].children[0].children[1].text = "10"
                    itemAt(0).children[0].children[0].children[1].validator.bottom = 1.0
                    itemAt(0).children[0].children[0].children[1].validator.decimals = 0
                    itemAt(1).children[0].children[0].children[0].text = "Updatetime [s]"
                    itemAt(1).children[0].children[0].children[1].text = "1.5"
                    itemAt(2).children[0].children[0].children[0].text = "Standard deviation boosterforce x"
                    itemAt(2).children[0].children[0].children[1].text = "150"
                    itemAt(3).children[0].children[0].children[0].text = "Standard deviation boosterforce y"
                    itemAt(3).children[0].children[0].children[1].text = "150"
                    itemAt(4).children[0].children[0].children[0].text = "Standard deviation measurement x"
                    itemAt(4).children[0].children[0].children[1].text = "2" 
                    itemAt(5).children[0].children[0].children[0].text = "Standard deviation measurement y"
                    itemAt(5).children[0].children[0].children[1].text = "3"
                    itemAt(6).children[0].children[0].children[0].text = "Mass"
                    itemAt(6).children[0].children[0].children[1].text = "4"
                }
            }
            Row{
                height:25
                width: parent.width
                Rectangle{
                    height: 25
                    width: parent.width
                    color: "white"
                    Text{
                        text: "Bosterforce"
                    }
                }
            }
            Repeater{
                id: id_inBoosterforce
                model: 2
                Row{
                    height: 25
                    width: parent.width
                    Rectangle{
                        height: parent.height
                        width: parent.width
                        color: "white"
                        Row {
                            spacing: 3
                            Text {
                                text: "Placeholder"
                            }
                            TextField {
                                text: "Placeholder"
                                validator: DoubleValidator{bottom: 0.0; decimals: 3}
                            }
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
                    itemAt(0).children[0].children[0].children[0].text = "X:"
                    itemAt(0).children[0].children[0].children[1].text = "1"
                    itemAt(0).children[0].children[0].children[2].text = ":"
                    itemAt(0).children[0].children[0].children[3].text = "2"
                    itemAt(1).children[0].children[0].children[0].text = "Y:"
                    itemAt(1).children[0].children[0].children[1].text = "3"
                    itemAt(1).children[0].children[0].children[2].text = ":"
                    itemAt(1).children[0].children[0].children[3].text = "4"
                    
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
                    itemAt(0).children[0].children[0].children[1].text = id_spaceship.x
                    itemAt(1).children[0].children[0].children[0].text = "Pos Y:"
                    itemAt(1).children[0].children[0].children[1].text = id_spaceship.y
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
                        console.log("Button update: nPredict: ", nPredict)
                        if (nPredict > 25){
                            nPredict = 25
                            id_input.itemAt(0).children[0].children[0].children[1].text = nPredict
                        }
                        else if (nPredict < 1){
                            nPredict = 1
                            id_input.itemAt(0).children[0].children[0].children[1].text = nPredict
                        }
                        var updateTime = id_input.itemAt(1).children[0].children[0].children[1].text
                        var accelVarX = id_input.itemAt(2).children[0].children[0].children[1].text
                        var accelVarY = id_input.itemAt(3).children[0].children[0].children[1].text
                        var measXVar = id_input.itemAt(4).children[0].children[0].children[1].text
                        var measYVar = id_input.itemAt(5).children[0].children[0].children[1].text
                        var mass = id_input.itemAt(6).children[0].children[0].children[1].text

                        var boosterforce_negx = id_inBoosterforce.itemAt(0).children[0].children[0].children[1].text
                        var boosterforce_posx = id_inBoosterforce.itemAt(0).children[0].children[0].children[3].text
                        var boosterforce_negy = id_inBoosterforce.itemAt(1).children[0].children[0].children[1].text
                        var boosterforce_posy = id_inBoosterforce.itemAt(1).children[0].children[0].children[3].text
                        //var boosterforceArray = new Array(0)
                        //boosterforceArray.push(boosterforce_negx)
                        //boosterforceArray.push(boosterforce_posx)
                        //boosterforceArray.push(boosterforce_negy)
                        //boosterforceArray.push(boosterforce_posy)
                        //console.log("Main.qml->UpdateButton: nPredict, updateTime, accelVar, measXVar, measYVar: ", nPredict, updateTime, accelVar, measXVar, measYVar)
                        //console.log("Main.qml->UpdateButton: boosterforce: ", boosterforceArray)
                        sendInput(nPredict, updateTime, accelVarX, accelVarY, measXVar, measYVar, mass, boosterforce_negx, boosterforce_posx, boosterforce_negy, boosterforce_posy)
                    }
                }
            }
            /*
            Rectangle{
                width: parent.width
                height: parent.width
                color: "white"
                ChartView {
                    title: "r_x and p_x to deviation_x"
                    anchors.fill: parent
                    antialiasing: true
                    ScatterSeries{
                        name: "errorX"
                        XYPoint{x: 0.0; y: 1}
                        XYPoint{x: 0.1; y: 2}
                        XYPoint{x: 0.2; y: 3}
                        XYPoint{x: 0.3; y: 4}
                        XYPoint{x: 0.4; y: 5}
                        XYPoint{x: 0.5; y: 6}
                        XYPoint{x: 0.6; y: 7}
                        XYPoint{x: 0.7; y: 8}
                        XYPoint{x: 0.8; y: 9}
                        XYPoint{x: 0.9; y: 10}
                    }
                    ScatterSeries{
                        name: "deviationX"
                        XYPoint{x: 0.0; y: 10}
                        XYPoint{x: 0.1; y: 9}
                        XYPoint{x: 0.2; y: 8}
                        XYPoint{x: 0.3; y: 7}
                        XYPoint{x: 0.4; y: 6}
                        XYPoint{x: 0.5; y: 5}
                        XYPoint{x: 0.6; y: 4}
                        XYPoint{x: 0.7; y: 3}
                        XYPoint{x: 0.8; y: 2}
                        XYPoint{x: 0.9; y: 1}
                    }
                }
            }
            Rectangle{
                width: parent.width
                height: parent.width
                color: "white"
                ChartView {
                    title: "r_y and p_y to deviation_y"
                    anchors.fill: parent
                    antialiasing: true
                    ScatterSeries{
                        name: "errorY"
                        XYPoint{x: 0.0; y: 1}
                        XYPoint{x: 0.1; y: 2}
                        XYPoint{x: 0.2; y: 3}
                        XYPoint{x: 0.3; y: 4}
                        XYPoint{x: 0.4; y: 5}
                        XYPoint{x: 0.5; y: 6}
                        XYPoint{x: 0.6; y: 7}
                        XYPoint{x: 0.7; y: 8}
                        XYPoint{x: 0.8; y: 9}
                        XYPoint{x: 0.9; y: 10}
                    }
                    ScatterSeries{
                        name: "deviationY"
                        XYPoint{x: 0.0; y: 10}
                        XYPoint{x: 0.1; y: 9}
                        XYPoint{x: 0.2; y: 8}
                        XYPoint{x: 0.3; y: 7}
                        XYPoint{x: 0.4; y: 6}
                        XYPoint{x: 0.5; y: 5}
                        XYPoint{x: 0.6; y: 4}
                        XYPoint{x: 0.7; y: 3}
                        XYPoint{x: 0.8; y: 2}
                        XYPoint{x: 0.9; y: 1}
                    }
                }
            }*/
        }
    }

    // Here everything to draw on Display
    Repeater{
        id: id_predictorRepeater
        model: 25
        Item {
            height: 10
            width: 10
            //radius: width*0.5
            x: 20
            y: 20
            visible: false
            Canvas{
                anchors.fill: parent
                onPaint:{
                    var ctx = getContext('2d');
                    ctx.reset()

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
        x: 5
        y: 5
        //source: "qrc:/icons/spaceship.png"
        //source: "spaceship:spaceship.png"
        source: "icon:Spaceship/spaceship.png"
        fillMode: Image.PreserveAspectFit
    }

    Rectangle {
        height: 10
        width: 10
        radius: width*0.5
        color: "green"
        x: id_spaceship.x + (id_spaceship.width - width) * 0.5
        y: id_spaceship.y + (id_spaceship.height - height) * 0.5
    }

    Rectangle {
        id: id_spaceshipMeasurement
        height: 10
        width: 10
        radius: width*0.5
        color: "blue"
        x: 5
        y: 5
    }
}