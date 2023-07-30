import QtQuick 2.0
import QtQuick.Layouts 1.12
import QtQuick.Controls 2.12
import QtQuick.Dialogs 


ColumnLayout {
    Text {
        id: leftlabel
        Layout.alignment: Qt.AlignCenter
        color: "black"
        font.pointSize: 40
        text: "BLD Trainer"
    }


    FileDialog {
        id: fileDialog
        title: "Please choose a file"
        onAccepted: {
            console.log("You chose: " + fileDialog.selectedFile)
            bridge.openFile(fileDialog.selectedFile)
        }
        onRejected: {
            console.log("Canceled")
        }
    }   

    Button {
        id: fileButton
        Layout.alignment: Qt.AlignCenter
        text: "Open file"
        onClicked: fileDialog.open()
    }

    Button {
        id: backButton
        Layout.alignment: Qt.AlignCenter
        text: "Back"
        onClicked: stackview.pop()
    }
}