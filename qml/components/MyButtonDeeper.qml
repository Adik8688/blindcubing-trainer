import QtQuick 2.0
import QtQuick.Controls 2.12

Button {
    height: parent.parent.parent.height * 0.15
    anchors {
        verticalCenter: parent.verticalCenter
        horizontalCenter: parent.horizontalCenter
    }
    font.pixelSize: height * 0.5
}