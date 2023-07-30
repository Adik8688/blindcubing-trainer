import QtQuick 2.0
import QtQuick.Layouts 1.12
import QtQuick.Controls 2.12

ColumnLayout  {
    Text {
        id: leftlabel
        Layout.alignment: Qt.AlignCenter
        color: "black"
        font.pointSize: 40
        text: "BLD Trainer"
    }

    Button {
        id: playButton
        Layout.alignment: Qt.AlignCenter
        text: "Play"
        onClicked: {
            stackview.push( "PieceChoice.qml" )
        }
    }

    Button {
        id: updateButton
        Layout.alignment: Qt.AlignCenter
        text: "Update comms"
        onClicked: stackview.push( "UpdateOptions.qml" )
    }

    Button {
        id: exportButton
        Layout.alignment: Qt.AlignCenter
        text: "Export data"
        onClicked: stackview.push( "ExportOptions.qml" )
    }
}
