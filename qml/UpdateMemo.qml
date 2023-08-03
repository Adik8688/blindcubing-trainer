import QtQuick 2.0
import QtQuick.Layouts 1.12
import QtQuick.Controls 2.12
import QtQuick.Dialogs 

import 'components'

ColumnLayout {

    FileDialog {
        id: fileDialog
        title: "Please choose a file"
        nameFilters: ["Excel files (*.xlsx *.xls)"]
        onAccepted: {
            bridge.updateData(fileDialog.selectedFile, 'memo') 
            stackview.pop()
            stackview.pop()
        }
    } 

    RowLayout {
        id: top
        Layout.preferredHeight: style.getInt('topHeight')
        Layout.fillWidth: true
        RectangleBox {
            Layout.fillWidth: true
            Layout.fillHeight: true
            BottomText {
                text: "Choose file"
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
        }
        RectangleBox {
            Layout.fillWidth: true
            Layout.fillHeight: true
            MyButton {
                id: fileButton
                text: "Open file"
                onClicked: fileDialog.open()
            }
        }
        RectangleBox {
            Layout.fillWidth: true
            Layout.fillHeight: true
            MyButton {
                id: helpButton
                text: "Help"
                onClicked: stackview.push('HelpMemo.qml')
            }
        }
        RectangleBox {
            Layout.fillWidth: true
            Layout.fillHeight: true
            MyButton {
                id: backButton
                text: "Back"
                onClicked: stackview.pop()
            }
        }  
    }

    RowLayout {
        id: bottom
        Layout.preferredHeight: style.getInt('bottomHeight')
        Layout.fillWidth: true
    }
}