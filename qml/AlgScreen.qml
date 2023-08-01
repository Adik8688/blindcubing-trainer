import QtQuick 2.0
import QtQuick.Layouts 1.12
import QtQuick.Controls 2.12

ColumnLayout {
    focus: true

    Keys.onReleased: (event) => {
        if(event.key === Qt.Key_Space && !event.isAutoRepeat) {
            bridge.incrementGameIndex()
            if (bridge.isGameFinished()) {
                    mainLoader.source = 'SavingScreen.qml'
                }
                else {
                    mainLoader.source = 'GameScreen.qml'
                }
        }
    }

    
    ColumnLayout{
        Layout.preferredHeight: 900
        Layout.fillWidth: true
        Rectangle {
            Layout.fillWidth: true
            Layout.fillHeight: true
            color: "transparent"
            Text {
                id: title
                anchors {
                    horizontalCenter: parent.horizontalCenter
                    bottom: parent.bottom
                } 
                text: bridge.getCurrentMemo()
                color: '#FFFFFF'
                font.pointSize: 30
            }

        }
        Rectangle {
            Layout.fillWidth: true
            Layout.fillHeight: true
            color: "transparent"
            Text {
                id: alg
                anchors {
                    horizontalCenter: parent.horizontalCenter
                    top: parent.top
                } 
                text: bridge.getCurrentAlg()
                color: '#FFFFFF'
                font.pointSize: 30
            }
        }
        
    }
    RowLayout{
        Layout.alignment: Qt.AlignBottom
        Layout.bottomMargin: 30
        Layout.rightMargin: 40
        Layout.leftMargin: 40
        Layout.fillWidth: true
        Layout.preferredHeight: 150

        
        Rectangle {
            Layout.fillWidth: true
            Layout.fillHeight: true
            color: "transparent"
            Text {
                text: bridge.getLastResult() ? 'Last: ' + bridge.getLastResult() : ''
                color: '#FFFFFF'
                font.pointSize: 30
                anchors {
                    horizontalCenter: parent.horizontalCenter
                    bottom: parent.bottom
                }
            }
        }
        Rectangle {
            Layout.fillWidth: true
            Layout.fillHeight: true
            color: "transparent"
            Text {
                text: bridge.getCurrentAlgNo() + "/" + bridge.getAlgsCount()
                color: '#FFFFFF'
                font.pointSize: 30
                anchors {
                    horizontalCenter: parent.horizontalCenter
                    bottom: parent.bottom
                }
            }
        }
        Rectangle {
            Layout.fillWidth: true
            Layout.fillHeight: true
            color: "transparent"
            Text {
                text: bridge.getNextAlg() ? "Next: " + bridge.getNextAlg() : ''
                color: '#FFFFFF'
                font.pointSize: 30
                anchors {
                    horizontalCenter: parent.horizontalCenter
                    bottom: parent.bottom
                }
            }
        }      
    }
    
}
