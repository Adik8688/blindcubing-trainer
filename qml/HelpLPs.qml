import QtQuick 2.0
import QtQuick.Layouts 1.12
import QtQuick.Controls 2.12
import QtQuick.Dialogs 


ColumnLayout {
    Text {
        id: leftlabel
        Layout.alignment: Qt.AlignHCenter
        color: "white"
        font.pointSize: 30
        text: "File must be 2xN list"
    }
    
    RowLayout{
        Layout.alignment: Qt.AlignCenter
        Layout.bottomMargin: 30
        Layout.rightMargin: 40
        Layout.leftMargin: 40
        Layout.preferredWidth: 1024
        Image{
            Layout.alignment: Qt.AlignCenter
            source: 'img/listLPs.png'
        }
    }

    RowLayout{
        Layout.alignment: Qt.AlignBottom
        Layout.bottomMargin: 30
        Layout.rightMargin: 40
        Layout.leftMargin: 40
        Layout.preferredWidth: 1024

        Button {
            Layout.alignment: Qt.AlignRight
            id: finishButton
            text: "Finish"
            onClicked: {
                stackview.pop()
            }
        }
    }

}