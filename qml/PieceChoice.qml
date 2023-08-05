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
                text: "Choose piece type"
                font.pointSize: 40
            }
        }
    }
    ColumnLayout {
        id: mid
        Layout.preferredHeight: style.getInt('midHeight')
        Layout.fillWidth: true

        RowLayout{
            Layout.fillWidth: true
            Layout.fillHeight: true
            RectangleBox {
                Layout.fillWidth: true
                Layout.fillHeight: true
            }
        }
        // 2nd row
        RowLayout{
            Layout.fillWidth: true
            Layout.fillHeight: true
            RectangleBox {
                Layout.fillWidth: true
                Layout.fillHeight: true
                MyButtonDeeper {
                    text: "Edges"
                    onClicked: {
                        bridge.setPieceType('edges')
                        stackview.push( "BufferChoice.qml" )
                    }
                }
            }
            RectangleBox {
                Layout.fillWidth: true
                Layout.fillHeight: true
                MyButtonDeeper {
                    text: "Corners"
                    onClicked: {
                        bridge.setPieceType('corners')
                        stackview.push( "BufferChoice.qml" )
                    }
                }
            }
        }
        
        // 3rd row
        RowLayout{
            RectangleBox {
                Layout.fillWidth: true
                Layout.fillHeight: true
                MyButtonDeeper {
                    text: "Parity"
                    onClicked: {
                        bridge.setPieceType('parity')
                        stackview.push( "BufferChoice.qml" )
                    }
                }
            }
            RectangleBox {
                Layout.fillWidth: true
                Layout.fillHeight: true
                MyButtonDeeper {
                    text: "Wings"
                    onClicked: {
                        bridge.setPieceType('wings')
                        stackview.push( "BufferChoice.qml" )
                    }
                }
            }
        }
        // 4th row
        RowLayout{
            RectangleBox {
                Layout.fillWidth: true
                Layout.fillHeight: true
                MyButtonDeeper {
                    text: "X-centers"
                    onClicked: {
                        bridge.setPieceType('xcenters')
                        stackview.push( "BufferChoice.qml" )
                    }
                }
            }
            RectangleBox {
                Layout.fillWidth: true
                Layout.fillHeight: true
                MyButtonDeeper {
                    text: "T-centers"
                    onClicked: {
                        bridge.setPieceType('tcenters')
                        stackview.push( "BufferChoice.qml" )
                    }
                }
            }
        }
        // 5th row
        RowLayout{
            Layout.fillWidth: true
            Layout.fillHeight: true
            RectangleBox {
                Layout.fillWidth: true
                Layout.fillHeight: true
                MyButtonDeeper {
                    text: 'Midges'
                    onClicked: {
                        bridge.setPieceType('midges')
                        stackview.push( "BufferChoice.qml" )
                    }
                }
            }
            RectangleBox {
                Layout.fillWidth: true
                Layout.fillHeight: true
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
    }
}