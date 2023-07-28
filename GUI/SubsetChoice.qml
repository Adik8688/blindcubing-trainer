import QtQuick 2.0
import QtQuick.Layouts 1.12
import QtQuick.Controls 2.12
ColumnLayout {
    Button {
        id: edgesButton
        Layout.alignment: Qt.AlignCenter
        text: "Edges"
        onClicked: stackview.pop()
    }
    Button {
        id: cornersButton
        Layout.alignment: Qt.AlignCenter
        text: "Corners"
        onClicked: stackview.pop()
    }

    Button {
        id: parityButton
        Layout.alignment: Qt.AlignCenter
        text: "Parity"
        onClicked: stackview.pop()
    }

    Button {
        id: wingsButton
        Layout.alignment: Qt.AlignCenter
        text: "Wings"
        onClicked: stackview.pop()
    }

    Button {
        id: xcentersButton
        Layout.alignment: Qt.AlignCenter
        text: "X-centers"
        onClicked: stackview.pop()
    }

    Button {
        id: tcentersButton
        Layout.alignment: Qt.AlignCenter
        text: "T-centers"
        onClicked: stackview.pop()
    }

    Button {
        id: midgesButton
        Layout.alignment: Qt.AlignCenter
        text: "Midges"
        onClicked: stackview.pop()
    }

    Button {
        id: midgesButton
        Layout.alignment: Qt.AlignCenter
        text: "Midges"
        onClicked: stackview.pop()
    }
}
