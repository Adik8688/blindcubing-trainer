import sys

from pathlib import Path
import os
from typing import Optional
from PySide6.QtCore import QObject, Slot
from PySide6.QtQml import QmlElement
from datetime import datetime

sys.path.append('..')

from Code.SpreadsheetsManager import SpreadsheetsManager
from Code.GameManager import GameManager
from Code.ExportManager import ExportManager

QML_IMPORT_NAME = "io.qt.textproperties"
QML_IMPORT_MAJOR_VERSION = 1 

@QmlElement
class Style(QObject):
    @Slot ()
    def __init__(self):
        super().__init__(None)
        stylepath = Path().absolute().parent / 'Style' / 'style.json'
        self.styleDict = SpreadsheetsManager.get_data(stylepath)
   

    @Slot (str, result=int)
    def getInt(self, property):
        return self.styleDict[property]
    
    @Slot (str, result=str)
    def getStr(self, property):
        return self.styleDict[property]


@QmlElement
class Bridge(QObject):
    @Slot (str, result=object)
    def getStyleProperty(self, property):
        return self.styleDict[property]
    

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

    @Slot (str, result=list)
    def listFromFile(self, url):
        filepath = url[8:]
        targets = set()
        with open(filepath) as f:
            for line in f:
                targets.add(line.strip())

        self.cases_set = targets
        return list(targets)

    @Slot (str)
    def setPieceType(self, piece):
        self.pieceType = piece

    @Slot (result=str)
    def getPieceType(self):
        return self.pieceType

    @Slot (result=list)
    def getBuffersList(self):
        path_to_jsons = Path().absolute().parent / "Json"

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
        self.cases_set = set()

    @Slot (result=list)
    def getFirstTargets(self):
        return sorted(self.first_targets)
    
    @Slot (result=list)
    def getSecondTargets(self):
        return sorted(self.second_targets)


    @Slot (str, str, str, result=list)
    def modifyList(self, option, first_target, second_target):
        if first_target == 'All':
            first_target = [i for i in self.first_targets if i != 'All']
        else:
            first_target = [first_target]

        if second_target == 'All':
            second_target = [i for i in self.second_targets if i != 'All']
        else:
            second_target = [second_target]

        new_set = set()
        for i in first_target:
            for j in second_target:
                if i != j and i != j[::-1]:
                    new_set.add(f'{i} {j}')


        if option == 'Add':
            self.cases_set.update(new_set)
        else:
            self.cases_set.difference_update(new_set)

        
        if not self.cases_set:
            return ['Click + to add comms']

        return list(self.cases_set)
    
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
    
    @Slot ()
    def saveResult(self):
        delta = (self.end - self.start).total_seconds()
        self.gm.save_result(round(delta, 2))

    @Slot (result=float)
    def getStudyMode(self):
        return self.study_mode

    @Slot (result=bool)
    def isGameFinished(self):
        return self.gm.is_game_finished()
    
    @Slot (result=str)
    def getLastResult(self):
        return str(self.gm.get_last_result())
    
    @Slot ()
    def setStartTime(self):
        self.start = datetime.now()
    
    @Slot ()
    def setEndTime(self):
        if not self.endFlag:
            self.end = datetime.now()
            self.endFlag = True

    @Slot ()
    def resetEndFlag(self):
        self.endFlag = False

    @Slot ()
    def endGame(self):
        results_list = self.gm.get_results_list()
        self.first_targets = list(set([i.split()[0] for i in results_list]))
        self.second_targets = list(set([i.split()[1] for i in results_list]))


    @Slot (result = list)
    def getResultsList(self):
        return self.gm.get_results_list()
    
    @Slot (str, list, result=list)
    def removeFromResultsList(self, key, results_list):
        results_list = [i for i in results_list if not key.split() == i.split()[:2]]
        self.first_targets = list(set([i.split()[0] for i in results_list]))
        self.second_targets = list(set([i.split()[1] for i in results_list]))

        self.gm.remove_from_targets_map(key)

        return results_list
    
    @Slot ()
    def saveResults(self):
        self.gm.save_results()

    @Slot ()
    def resetGame(self):
        self.gm.set_game()

    @Slot ()
    def exportStats(self):
        em = ExportManager()
        em.export_stats()