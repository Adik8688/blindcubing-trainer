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
                text: "Choose your buffer"
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
            ComboBox {
                id: bufferBox
                model: bridge.getBuffersList()
                anchors {
                    verticalCenter: parent.verticalCenter
                    horizontalCenter: parent.horizontalCenter
                }
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
                    if (bufferBox.currentValue) {
                        bridge.setBuffer(bufferBox.currentValue)
                        bridge.setAvailableTargets()
                        stackview.push('SubsetChoice.qml')
                    }
                }
            }
        }
    }
}
