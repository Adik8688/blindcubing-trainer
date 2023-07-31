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
                    model: bridge.getFirstTargets()
                }
                Button {
                    id: addButton
                    text: "Add"
                    onClicked: casesList.model = bridge.modifyList('Add', firstTarget.currentValue, secondTarget.currentValue, casesList.model)
                }
            }
            ColumnLayout{
                ComboBox {
                    id: secondTarget
                    model: bridge.getSecondTargets()
                }
                Button {
                    id: removeButton
                    text: 'Remove'
                    onClicked: casesList.model = bridge.modifyList('Remove', firstTarget.currentValue, secondTarget.currentValue, casesList.model)
                }
            }
        }
        ColumnLayout{
            Text {
                Layout.alignment: Qt.AlignCenter
                text: "Current list"
                color: '#FFFFFF'
                font.pointSize: 30
            }
            ListView {
                id: casesList
                width: 160
                height: 240

                model: []

                delegate: ItemDelegate {
                    text: modelData
                    onClicked: console.log("clicked:", modelData)
                    required property string modelData
                }
                ScrollIndicator.vertical: ScrollIndicator { }
            }
        }
    }

    Button {
        id: backButton
        Layout.alignment: Qt.AlignCenter
        text: "Back"
        onClicked: {
            stackview.pop()
            casesList.model = bridge.addElement(casesList.model, firstTarget.currentValue + " " + secondTarget.currentValue)
        }
    }
}
