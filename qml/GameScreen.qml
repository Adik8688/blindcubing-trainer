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
            if (bridge.isGameFinished()) mainLoader.source = 'SavingScreen.qml'
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
            }
        }
        RectangleBox {
            Layout.fillWidth: true
            Layout.fillHeight: true
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
                text: bridge.getNextAlg() ? "Next: " + bridge.getNextAlg() : ''
            }
        }
    }
}