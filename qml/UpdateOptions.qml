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
        text: "Update algs"
        onClicked: stackview.push('UpdateAlgs.qml')
    }

    Button {
        id: wordsButton
        Layout.alignment: Qt.AlignCenter
        text: "Update words"
        onClicked: stackview.pop()
    }

    Button {
        id: lpButton
        Layout.alignment: Qt.AlignCenter
        text: "Update LPs"
        onClicked: stackview.pop()

    }

    Button {
        id: backButton
        Layout.alignment: Qt.AlignCenter
        text: "Back"
        onClicked: stackview.pop()
    }
}