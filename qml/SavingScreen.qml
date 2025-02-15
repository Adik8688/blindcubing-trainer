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
                text: "Review your results"
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
                    id: removeButton
                    text: '-'
                    onClicked: {
                        if (casesList.model.length > 0 ){
                            casesList.model = bridge.removeFromResultsList(firstTarget.currentValue + ' ' + secondTarget.currentValue, false)
                            firstTarget.model = bridge.getFirstTargets()
                            secondTarget.model = bridge.getSecondTargets()
                            avg.text = bridge.getSessionAvg()
                        }
                    }

                }
            }
        }
        
        RectangleBox {
            Layout.fillWidth: true
            Layout.preferredHeight: 30
            BottomText {
                id: avg
                text: bridge.getSessionAvg()
            }

        RectangleBox {
            Layout.fillWidth: true
            Layout.preferredHeight: 15
        }
        }
        RectangleBox {
            Layout.fillWidth: true
            Layout.preferredHeight: 230
            ListView {
                anchors.horizontalCenter: parent.horizontalCenter
                id: casesList
                width: 160
                height: parent.height

                model: bridge.getResultsList()

                delegate: ItemDelegate {
                    text: modelData
                    required property string modelData
                    onClicked: { 
                        // casesList.model = bridge.removeFromResultsList(modelData, true)
                        // firstTarget.model = bridge.getFirstTargets()
                        // secondTarget.model = bridge.getSecondTargets()
                        // avg.text = bridge.getSessionAvg()
                    }
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
                text: "Exit"
                onClicked: mainLoader.source = 'StackViewPage.qml'
            }
        }
        RectangleBox {
            Layout.fillWidth: true
            Layout.fillHeight: true
            MyButtonDeeper {
                text: "Save and exit"
                onClicked: {
                    bridge.saveResults()
                    mainLoader.source = 'StackViewPage.qml'
                }
            }
        }
        RectangleBox {
            Layout.fillWidth: true
            Layout.fillHeight: true
            MyButtonDeeper {
                text: "Save and play again"
                onClicked: {
                    bridge.saveResults()
                    bridge.resetGame()
                    mainLoader.source = 'WaitingScreen.qml'
                }
            }
        }
    }
}
