import QtQuick 
import QtQuick.Layouts 1.11
import QtQuick.Controls 2.1
import QtQuick.Window 2.1
import QtQuick.Controls.Material 2.1
import QtQuick.Dialogs 

import io.qt.textproperties 1.0
import 'components'

ApplicationWindow {
    id: root
    width: 1024
    height: 680
    visible: true
    title: qsTr("Blindcubing trainer")

    Material.theme: Material.Dark
    Material.accent: Material.Red
 
    Bridge {
        id: bridge
    }

    Style {
        id: style
    }
    
    Loader {
        id: mainLoader
        anchors.fill: parent
        anchors.margins: 30
        source: "StackViewPage.qml"
    }
}