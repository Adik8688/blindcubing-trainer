import sys

from pathlib import Path
import os
from PySide6.QtCore import QObject, Slot
from PySide6.QtQml import QmlElement

sys.path.append('..')

from Code.SpreadsheetsManager import SpreadsheetsManager

QML_IMPORT_NAME = "io.qt.textproperties"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class Bridge(QObject):


    @Slot (str, str)
    def updateData(self, url, update_option):
        filepath = url[8:]
        sm = SpreadsheetsManager(filepath)
        if update_option == 'algs':
            sm.update_algs()
        elif update_option == 'memo':
            sm.update_memo()
        else:
            sm.update_lps()

    @Slot (str)
    def setPieceType(self, piece):
        self.pieceType = piece

    @Slot (result=str)
    def getPieceType(self):
        return self.pieceType

    @Slot (result=list)
    def getBuffersList(self):
        path_to_jsons = Path().absolute().parent / "json"

        jsons = []

        for filename in os.listdir(path_to_jsons):
            if filename.startswith(self.pieceType):
                jsons.append(filename)

        buffers = [i.split('.')[0].split('_')[1] for i in jsons]
        return buffers
    
    @Slot (str)
    def setBuffer(self, buffer):
        self.buffer = buffer

    @Slot (result=str)
    def getBuffer(self):
        return self.buffer
    
    @Slot ()
    def setAvailableTargets(self):
        print(self.pieceType)
        print(self.buffer)

        filepath = Path().absolute().parent / 'json' / f'{self.pieceType}_{self.buffer}.json'

        print(str(filepath))

        data = SpreadsheetsManager.get_data(filepath)

        self.first_targets = ['All'] + list(set([v['first_target'] for v in data.values()]))
        self.seconds_targets = ['All'] + list(set([v['second_target'] for v in data.values()]))


    @Slot (list, str, result=list)
    def modifyList(self, option, first_target, second_target, cases_list):
        pass