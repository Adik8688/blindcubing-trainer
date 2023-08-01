import sys

from pathlib import Path
import os
from PySide6.QtCore import QObject, Slot
from PySide6.QtQml import QmlElement
from datetime import datetime

sys.path.append('..')

from Code.SpreadsheetsManager import SpreadsheetsManager
from Code.GameManager import GameManager

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
        filepath = Path().absolute().parent / 'json' / f'{self.pieceType}_{self.buffer}.json'
        data = SpreadsheetsManager.get_data(filepath)

        self.first_targets = ['All'] + list(set([v['first_target'] for v in data.values()]))
        self.second_targets = ['All'] + list(set([v['second_target'] for v in data.values()]))

    @Slot (result=list)
    def getFirstTargets(self):
        return self.first_targets
    
    @Slot (result=list)
    def getSecondTargets(self):
        return self.second_targets


    @Slot (str, str, str, list, result=list)
    def modifyList(self, option, first_target, second_target, cases_list):
        if first_target == 'All':
            first_target = self.first_targets
        else:
            first_target = [first_target]

        if second_target == 'All':
            second_target = self.second_targets
        else:
            second_target = [second_target]

        new_set = set()
        for i in first_target:
            for j in second_target:
                if i != j:
                    new_set.add(f'{i} {j}')

        cases_list = set(cases_list)

        if option == 'Add':
            cases_list.update(new_set)
        else:
            cases_list.difference_update(new_set)

        return list(cases_list)
    
    @Slot (list, int)
    def startGame(self, targets, study_mode):
        self.gm = GameManager(f'{self.pieceType}_{self.buffer}.json', targets)
        self.study_mode = study_mode

    @Slot ()
    def incrementGameIndex(self):
        self.gm.increment_index()

    @Slot (result=str)
    def getNextAlg(self):
        return self.gm.get_next_alg()
    
    @Slot (result=str)
    def getCurrentAlg(self):
        return self.gm.get_current_alg()

    @Slot (result=str)
    def getCurrentMemo(self):
        return self.gm.get_current_memo()
    
    @Slot (result=str)
    def getCurrentAlgNo(self):
        return str(self.gm.get_current_alg_no())
    
    @Slot (result=str)
    def getAlgsCount(self): 
        return str(self.gm.get_algs_count())
    
    @Slot (object, object)
    def saveResults(self, start_time, end_time):
        delta = (end_time - start_time).total_seconds()
        self.gm.save_result(round(delta, 2))

    @Slot (result=float)
    def getStudyMode(self):
        return self.study_mode

    @Slot (result=bool)
    def isGameFinished(self):
        return self.gm.is_game_finished()
    
    @Slot (result=object)
    def getCurrentTime(self):
        return datetime.now()
    
    @Slot (result=str)
    def getLastResult(self):
        return self.gm.get_last_result()