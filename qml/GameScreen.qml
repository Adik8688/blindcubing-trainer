import QtQuick 2.0
import QtQuick.Layouts 1.12
import QtQuick.Controls 2.12
import "components"

ColumnLayout {
    focus: true
    property var getStartTime: bridge.setStartTime(), bridge.resetEndFlag()

    Keys.onPressed: (event) => {
    if (event.key === Qt.Key_Space)
        bridge.setEndTime()
}

    Keys.onReleased: (event) => {
    if (event.key === Qt.Key_Space && !event.isAutoRepeat)
    {
        bridge.saveResult()
        if (bridge.getStudyMode()) mainLoader.source = 'AlgScreen.qml'

        else {
            bridge.incrementGameIndex()
            if (bridge.isGameFinished()) {
                bridge.endGame()
                mainLoader.source = 'SavingScreen.qml'
            } 
            else {
                mainLoader.source = 'AlgScreen.qml'
                mainLoader.source = 'GameScreen.qml'
            }
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
            // remove in production
            TopText {
                text: bridge.getCurrentAlg()
                font.pointSize: Math.max(20, Math.min(60, parent.width * 1.5 / text.length))
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