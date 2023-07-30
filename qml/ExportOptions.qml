import QtQuick 2.0
import QtQuick.Layouts 1.12
import QtQuick.Controls 2.12
ColumnLayout {
    Text {
        id: leftlabel
        Layout.alignment: Qt.AlignCenter
        color: "black"
        font.pointSize: 40
        text: "BLD Trainer"
    }


    Button {
        id: algsButton
        Layout.alignment: Qt.AlignCenter
        text: "Export stats"
        onClicked: stackview.pop()
    }

    Button {
        id: wordsButton
        Layout.alignment: Qt.AlignCenter
        text: "Export data"
        onClicked: stackview.pop()
    }

    Button {
        id: backButton
        Layout.alignment: Qt.AlignCenter
        text: "Back"
        onClicked: stackview.pop()
    }
}