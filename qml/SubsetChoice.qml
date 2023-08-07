import QtQuick 2.0
import QtQuick.Layouts 1.12
import QtQuick.Controls 2.12

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
                text: "Choose subset"
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
            Layout.preferredHeight: 15
        }
        RectangleBox {
            Layout.fillWidth: true
            Layout.preferredHeight: 100
            RowLayout {
                Layout.fillWidth: true
                Layout.fillHeight: true
                anchors.horizontalCenter: parent.horizontalCenter
                ComboBox{
                    id: firstTarget
                    model: bridge.getFirstTargets()
                }
                ComboBox {
                    id: secondTarget
                    model: bridge.getSecondTargets()
                }
                Button {
                    id: addButton
                    text: "+"
                    onClicked: casesList.model = bridge.modifyList('Add', firstTarget.currentValue, secondTarget.currentValue)
                }
                Button {
                    id: removeButton
                    text: '-'
                    onClicked: casesList.model = bridge.modifyList('Remove', firstTarget.currentValue, secondTarget.currentValue)
                }
            }
            Switch {
                anchors.right: parent.right
                id: studySwitch
                text: 'Study mode'
            }
        }
        RectangleBox {
            Layout.fillWidth: true
            Layout.preferredHeight: 15
        }
        RectangleBox {
            Layout.fillWidth: true
            Layout.preferredHeight: 270
            ListView {
                anchors.horizontalCenter: parent.horizontalCenter
                id: casesList
                width: 160
                height: parent.height

                model: ['Click + to add comms']

                delegate: ItemDelegate {
                    text: modelData
                    onClicked: console.log("clicked:", modelData)
                    required property string modelData
                }
                ScrollIndicator.vertical: ScrollIndicator { }
            }
        }
    }
    RowLayout {
        id: bottom
        Layout.preferredHeight: style.getInt('bottomHeight')
        Layout.fillWidth: true
        RectangleBox {
            Layout.fillWidth: true
            Layout.fillHeight: true
            MyButtonDeeper {
                text: "Back"
                onClicked: stackview.pop()
            }
        }
        RectangleBox {
            Layout.fillWidth: true
            Layout.fillHeight: true
            MyButtonDeeper {
                text: "Submit"
                onClicked: {
                    if (casesList.model){
                        bridge.startGame(casesList.model, studySwitch.position)
                        mainLoader.source = 'WaitingScreen.qml'
                    }
                }
            }
        }
    }
}
