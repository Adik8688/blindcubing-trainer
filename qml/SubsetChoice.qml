import QtQuick 2.0
import QtQuick.Layouts 1.12
import QtQuick.Controls 2.12
ColumnLayout {
    Text {
        Layout.alignment: Qt.AlignCenter
        text: "Choose subset"
        color: '#FFFFFF'
        font.pointSize: 40
    }

    RowLayout{
        Layout.alignment: Qt.AlignCenter
        Layout.bottomMargin: 30
        Layout.rightMargin: 40
        Layout.leftMargin: 40
        Layout.preferredWidth: 1024
        RowLayout{
            Layout.preferredWidth: parent.preferredWidth / 3
            ColumnLayout{
                ComboBox{
                    id: firstTarget
                    model: ['All', 'UB', 'UL', 'UR']
                }
                Button {
                    id: addButton
                    text: "Add"
                }
            }
            ColumnLayout{
                ComboBox {
                    id: secondTarget
                    model: ['All', 'UB', 'UL', 'UR']
                }
                Button {
                    id: removeButton
                    text: 'Remove'
                }
            }
        }
        ColumnLayout{
            ListView {
                width: 180; height: 200

                model: ['UB', 'UL', 'UR']

                
            }
        }
    }

    Button {
        id: backButton
        Layout.alignment: Qt.AlignCenter
        text: "Back"
        onClicked: {
            stackview.pop()
        }
    }
}
