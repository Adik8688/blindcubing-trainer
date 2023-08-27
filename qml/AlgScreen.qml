import QtQuick 2.0
import QtQuick.Layouts 1.12
import QtQuick.Controls 2.12

import 'components'

ColumnLayout {
    focus: true

    Keys.onReleased: (event) => {
        if(event.key === Qt.Key_Space && !event.isAutoRepeat) {
            bridge.incrementGameIndex()
            if (bridge.isGameFinished()) {
                    bridge.endGame()
                    mainLoader.source = 'SavingScreen.qml'
                }
                else {
                    mainLoader.source = 'GameScreen.qml'
                }
        }
    }
    RowLayout {
        id: top
        Layout.preferredHeight: style.getInt('topHeight')
        Layout.fillWidth: true
    }
    ColumnLayout {
        id: mid
        Layout.preferredHeight: style.getInt('midHeight')
        Layout.fillWidth: true
        RectangleBox {
            Layout.fillWidth: true
            Layout.fillHeight: true
            BottomText {
                text: bridge.getCurrentMemo()
                font.pointSize: 60
            }
        }
        RectangleBox {
            Layout.fillWidth: true
            Layout.fillHeight: true
            TopText {
                text: bridge.getCurrentAlg()
                font.pointSize: 60
            }
        }

    }
    RowLayout {
        id: bottom
        Layout.preferredHeight: style.getInt('bottomHeight')
        Layout.fillWidth: true

        RectangleBox {
            Layout.fillWidth: true
            Layout.fillHeight: true
            BottomText {
                text: bridge.getLastResult() ? 'Last: ' + bridge.getLastResult() : ''
            }
        }
        RectangleBox {
            Layout.fillWidth: true
            Layout.fillHeight: true
            BottomText {
                text: bridge.getCurrentAlgNo() + "/" + bridge.getAlgsCount()
            }
        }
        RectangleBox {
            Layout.fillWidth: true
            Layout.fillHeight: true
            BottomText {
                text: bridge.getNextCase() ? "Next: " + bridge.getNextCase() : ''
            }
        }
    }  
}
