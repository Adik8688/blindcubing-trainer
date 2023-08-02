import QtQuick 2.0
import QtQuick.Layouts 1.12
import QtQuick.Controls 2.12

import 'components'

ColumnLayout {
    RowLayout {
        id: top
        Layout.preferredHeight: style.getInt('topHeight')
        Layout.fillWidth: true
        RectangleBox {
            Layout.fillWidth: true
            Layout.fillHeight: true
            BottomText {
                text: 'Blindcubing trainer'
                font.pointSize: 40
            }
        }
    }
    ColumnLayout {
        id: mid
        Layout.preferredHeight: style.getInt('midHeight')
        Layout.fillWidth: true
        RectangleBox {
            Layout.fillWidth: true
            Layout.fillHeight: true
        }
        RectangleBox {
            Layout.fillWidth: true
            Layout.fillHeight: true
            MyButton {
                id: playButton
                text: "Play"
                onClicked: {
                    stackview.push( "PieceChoice.qml" )
                }
            }
        }
        RectangleBox {
            Layout.fillWidth: true
            Layout.fillHeight: true
            MyButton {
                id: updateButton
                text: "Update comms"
                onClicked: stackview.push( "UpdateOptions.qml" )
            }
        }
        RectangleBox {
            Layout.fillWidth: true
            Layout.fillHeight: true
            MyButton {
                id: exportButton
                Layout.alignment: Qt.AlignCenter
                text: "Export data"
                onClicked: stackview.push( "ExportOptions.qml" )
            }
        }
        RectangleBox {
            Layout.fillWidth: true
            Layout.fillHeight: true
            MyButton {
                id: exitButton
                Layout.alignment: Qt.AlignCenter
                text: "Exit"
                onClicked: Qt.quit()
            }
        }
    }
    RowLayout {
        id: bottom
        Layout.preferredHeight: style.getInt('bottomHeight')
        Layout.fillWidth: true
    }
}