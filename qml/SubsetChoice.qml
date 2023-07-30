import QtQuick 2.0
import QtQuick.Layouts 1.12
import QtQuick.Controls 2.12
ColumnLayout {
    Text {
        Layout.alignment: Qt.AlignCenter
        text: "Choose subset"
        color: '#FFFFFF'
        font.pointSize: 40
    }

    Text {
        Layout.alignment: Qt.AlignCenter
        text: "Type: " + bridge.getPieceType()
        color: '#FFFFFF'
        font.pointSize: 20
    }

    Text {
        Layout.alignment: Qt.AlignCenter
        text: "Buffer: " + bridge.getBuffer()
        color: '#FFFFFF'
        font.pointSize: 20
    }

    Button {
        id: backButton
        Layout.alignment: Qt.AlignCenter
        text: "Back"
        onClicked: {
            stackview.pop()
        }
    }
}
