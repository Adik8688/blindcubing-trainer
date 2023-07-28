import QtQuick 2.0
import QtQuick.Layouts 1.12
import QtQuick.Controls 2.12
GridLayout {
    id: grid
    columns: 2
    ColumnLayout {
        Layout.alignment: Qt.AlignCenter
        Button {
            id: edgesButton
            Layout.alignment: Qt.AlignCenter
            text: "Edges"
            onClicked: stackview.push( "SubsetChoice.qml" )
        }

        Button {
            id: cornersButton
            Layout.alignment: Qt.AlignCenter
            text: "Corners"
            onClicked: stackview.push( "SubsetChoice.qml" )
        }

        Button {
            id: parityButton
            Layout.alignment: Qt.AlignCenter
            text: "Parity"
            onClicked: stackview.push( "SubsetChoice.qml" )
        }

        Button {
            id: wingsButton
            Layout.alignment: Qt.AlignCenter
            text: "Wings"
            onClicked: stackview.push( "SubsetChoice.qml" )
        }
    }
    ColumnLayout {
        Layout.alignment: Qt.AlignCenter
        Button {
            id: xcentersButton
            Layout.alignment: Qt.AlignCenter
            text: "X-centers"
            onClicked: stackview.push( "SubsetChoice.qml" )
        }

        Button {
            id: tcentersButton
            Layout.alignment: Qt.AlignCenter
            text: "T-centers"
            onClicked: stackview.push( "SubsetChoice.qml" )
        }

        Button {
            id: midgesButton
            Layout.alignment: Qt.AlignCenter
            text: "Midges"
            onClicked: stackview.push( "SubsetChoice.qml" )
        }
    }
}