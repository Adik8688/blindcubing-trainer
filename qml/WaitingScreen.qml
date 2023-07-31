import QtQuick 2.0
import QtQuick.Layouts 1.12
import QtQuick.Controls 2.12

ColumnLayout {
    focus: true
    Text {
        id: title
        Layout.alignment: Qt.AlignCenter
        text: "Press space to start"
        color: '#FFFFFF'
        font.pointSize: 40
    }
    Keys.onReleased: (event) => {
        if(event.key === Qt.Key_Space && !event.isAutoRepeat) {
            mainLoader.source = 'GameScreen.qml'
        }
    }
}
