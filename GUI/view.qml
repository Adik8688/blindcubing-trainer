import QtQuick 2.12
import QtQuick.Window 2.12

Window {
    id: root
    width: 1024
    height: 680
    visible: true
    title: qsTr("InfotainmentExample")

    Loader {
        id: mainLoader
        anchors {
            left: parent.left
            right: parent.right
            top: parent.top
            bottom: parent.bottom
        }
        source: "StackViewPage.qml"
    }
}