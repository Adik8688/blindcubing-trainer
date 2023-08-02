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
                text: "Update options"
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
                id: algsButton
                text: "Update algs"
                onClicked: stackview.push('UpdateAlgs.qml')
            }
        }
        RectangleBox {
            Layout.fillWidth: true
            Layout.fillHeight: true
            MyButton {
                id: memoButton
                text: "Update memo"
                onClicked: stackview.push('UpdateMemo.qml')
            }
        }
        RectangleBox {
            Layout.fillWidth: true
            Layout.fillHeight: true
            MyButton {
                id: lpButton
                text: "Update LPs"
                onClicked: stackview.push('UpdateLPs.qml')
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