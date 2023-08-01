import QtQuick 2.0
import QtQuick.Layouts 1.12
import QtQuick.Controls 2.12

ColumnLayout {
    focus: true
    id: mainLayout
    property var startTime: bridge.getCurrentTime()
    property var endTime: bridge.getCurrentTime()

    Keys.onReleased: (event) => {
        if(event.key === Qt.Key_Space && !event.isAutoRepeat) {
            mainLayout.endTime = bridge.getCurrentTime()
            bridge.saveResults(mainLayout.startTime, mainLayout.endTime)
            if (bridge.getStudyMode()) {
                mainLoader.source = 'AlgScreen.qml'
            }
            else {
                bridge.incrementGameIndex()

                if (bridge.isGameFinished()) {
                    mainLoader.source = 'SavingScreen.qml'
                }
                else {
                    mainLoader.source = 'AlgScreen.qml'
                    mainLoader.source = 'GameScreen.qml'
                }
            }
        }
    }

    Text {
        id: title
        Layout.alignment: Qt.AlignCenter
        text: bridge.getCurrentMemo()
        color: '#FFFFFF'
        font.pointSize: 30
    }

    RowLayout{
        Layout.alignment: Qt.AlignBottom
        Layout.bottomMargin: 30
        Layout.rightMargin: 40
        Layout.leftMargin: 40
        Layout.preferredWidth: 1024
        
        ColumnLayout {
            Layout.alignment: Qt.AlignLeft
            Text {
                text: bridge.getLastResult() ? 'Last: ' + bridge.getLastResult() : ''
                color: '#FFFFFF'
                font.pointSize: 30
            } 
            Text {
                text: bridge.getCurrentAlgNo() + "/" + bridge.getAlgsCount()
                color: '#FFFFFF'
                font.pointSize: 30
            } 
        }
        
        Text {
            Layout.alignment: Qt.AlignRight
            text: bridge.getNextAlg() ? "Next: " + bridge.getNextAlg() : ''
            color: '#FFFFFF'
            font.pointSize: 30

        }
    }
    
}
