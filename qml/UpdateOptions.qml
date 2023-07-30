import QtQuick 2.0
import QtQuick.Layouts 1.12
import QtQuick.Controls 2.12
ColumnLayout {
    Text {
        id: leftlabel
        Layout.alignment: Qt.AlignCenter
        color: "white"
        font.pointSize: 40
        text: "Update options"
    }


    Button {
        id: algsButton
        Layout.alignment: Qt.AlignCenter
        text: "Update algs"
        onClicked: stackview.push('UpdateAlgs.qml')
    }

    Button {
        id: memoButton
        Layout.alignment: Qt.AlignCenter
        text: "Update memo"
        onClicked: stackview.push('UpdateMemo.qml')
    }

    Button {
        id: lpButton
        Layout.alignment: Qt.AlignCenter
        text: "Update LPs"
        onClicked: stackview.push('UpdateLPs.qml')

    }

    Button {
        id: backButton
        Layout.alignment: Qt.AlignCenter
        text: "Back"
        onClicked: stackview.pop()
    }
}