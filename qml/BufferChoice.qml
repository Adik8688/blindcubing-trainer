import QtQuick 2.0
import QtQuick.Layouts 1.12
import QtQuick.Controls 2.12
ColumnLayout {
    Text {
        Layout.alignment: Qt.AlignCenter
        text: "Choose your buffer"
        color: '#FFFFFF'
        font.pointSize: 40
    }


    ComboBox {
        id: bufferBox
        Layout.alignment: Qt.AlignCenter
        model: bridge.getBuffersList()
    }

    Button {
        id: submitButton
        Layout.alignment: Qt.AlignCenter
        text: "Submit"
        onClicked: {
            if (bufferBox.currentValue) {
                bridge.setBuffer(bufferBox.currentValue)
                stackview.push('SubsetChoice.qml')
            }
        }
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
