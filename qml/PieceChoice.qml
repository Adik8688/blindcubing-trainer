import QtQuick 2.0
import QtQuick.Layouts 1.12
import QtQuick.Controls 2.12
GridLayout {
    id: grid
    columns: 2
    ColumnLayout {
        Layout.alignment: Qt.AlignCenter
        spacing: 10
        Button {
            id: edgesButton
            Layout.alignment: Qt.AlignCenter
            text: "Edges"
            onClicked: {
                bridge.setPieceType('edges')
                stackview.push( "BufferChoice.qml" )
            }
        }

        Button {
            id: cornersButton
            Layout.alignment: Qt.AlignCenter
            text: "Corners"
            onClicked: {
                bridge.setPieceType('corners')
                stackview.push( "BufferChoice.qml" )
            }
        }

        Button {
            id: parityButton
            Layout.alignment: Qt.AlignCenter
            text: "Parity"
            onClicked: {
                bridge.setPieceType('parity')
                stackview.push( "BufferChoice.qml" )
            }
        }

        Button {
            id: wingsButton
            Layout.alignment: Qt.AlignCenter
            text: "Wings"
            onClicked: {
                bridge.setPieceType('wings')
                stackview.push( "BufferChoice.qml" )
            }
        }
    }
    ColumnLayout {
        spacing: 2
        Layout.alignment: Qt.AlignCenter
        Button {
            id: xcentersButton
            Layout.alignment: Qt.AlignCenter
            text: "X-centers"
            onClicked: {
                bridge.setPieceType('xcenters')
                stackview.push( "BufferChoice.qml" )
            }
        }

        Button {
            id: tcentersButton
            Layout.alignment: Qt.AlignCenter
            text: "T-centers"
            onClicked: {
                bridge.setPieceType('tcenters')
                stackview.push( "BufferChoice.qml" )
            }
        }

        Button {
            id: midgesButton
            Layout.alignment: Qt.AlignCenter
            text: "Midges"
            onClicked: {
                bridge.setPieceType('midges')
                stackview.push( "BufferChoice.qml" )
            }
        }

        Button {
            id: backButton
            Layout.alignment: Qt.AlignCenter
            text: "Back"
            onClicked: stackview.pop()
        }
    }
}