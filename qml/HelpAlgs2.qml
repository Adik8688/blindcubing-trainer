import QtQuick 2.0
import QtQuick.Layouts 1.12
import QtQuick.Controls 2.12
import QtQuick.Dialogs 


ColumnLayout {
    RowLayout{
        Layout.alignment: Qt.AlignCenter
        Layout.bottomMargin: 30
        Layout.rightMargin: 40
        Layout.leftMargin: 40
        Layout.preferredWidth: 1024
        ColumnLayout{
            Text {
                id: leftlabel
                Layout.alignment: Qt.AlignHCenter
                color: "white"
                font.pointSize: 30
                text: "Buffer must be at A1"
            }
        }
        ColumnLayout{
            Text {
                id: content
                Layout.alignment: Qt.AlignHCenter
                color: "white"
                font.pointSize: 30
                text: "Proper formats"
            }
            Image {
                source: 'img/buffers.png'
            }
        }
    }


    RowLayout{
        Layout.alignment: Qt.AlignBottom
        Layout.bottomMargin: 30
        Layout.rightMargin: 40
        Layout.leftMargin: 40
        Layout.preferredWidth: 1024
        
        Button {
            Layout.alignment: Qt.AlignLeft
            id: previousButton
            text: "Previous"
            onClicked: stackview.pop()
        } 
        Button {
            Layout.alignment: Qt.AlignRight
            id: finishButton
            text: "Finish"
            onClicked: {
                stackview.pop()
                stackview.pop()
            }
        }
    }
}