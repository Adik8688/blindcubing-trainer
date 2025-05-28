import sys
from pathlib import Path
import os
from typing import Optional
from datetime import datetime

from PySide6.QtCore import QObject, Slot
from PySide6.QtQml import QmlElement
import numpy as np

from .SpreadsheetsManager import SpreadsheetsManager
from .GameManager import GameManager
from .ExportManager import ExportManager
from .project_paths import JSON_DIR, STYLE_DIR
from .utils import get_data, save_data

from urllib.parse import urlparse, unquote
import os

QML_IMPORT_NAME = "io.qt.textproperties"
QML_IMPORT_MAJOR_VERSION = 1 

@QmlElement
class Style(QObject):
    '''
    This class is used for emulating stylesheet
    '''

    @Slot ()
    def __init__(self):
        super().__init__(None)

        # style file stores sizes, proportions etc
        stylepath = STYLE_DIR / 'style.json'
        self.styleDict = get_data(stylepath)
   

    @Slot (str, result=int)
    def getInt(self, property):
        '''
        Gets numeric attr from stylefile
        '''
        return self.styleDict[property]
    
    @Slot (str, result=str)
    def getStr(self, property):
        '''
        Gets string attr from stylefile
        '''
        return self.styleDict[property]


@QmlElement
class Bridge(QObject):
    '''
    This class is used for communication between QML and Python
    '''

    @Slot (str, str)
    def updateData(self, url, update_option):
        '''
        Calls method to update algs/memo/lps depending on the chosen option
        '''

        def qml_url_to_path(url):
            # Parse and decode URL
            parsed = urlparse(url)
            path = unquote(parsed.path)

            # macOS: remove leading '/' if it's followed by a drive letter (e.g., '/C:/...')
            if os.name == 'nt' and path.startswith('/') and ':' in path[1:3]:
                path = path[1:]

            return path
        
        # works no windows, might not work on mac
        filepath = qml_url_to_path(url)


        sm = SpreadsheetsManager(filepath)

        functions_map = {
            "algs": sm.update_algs,
            "memo": sm.update_memo,
            "memo_remove": sm.remove_memo,
        }

        functions_map[update_option]()
        

    @Slot (str)
    def setPieceType(self, piece):
        '''
        Sets piece type depending on the user's choice eg. edges
        '''
        self.pieceType = piece

    @Slot (result=str)
    def getPieceType(self):
        '''
        Returns piece type set before 
        '''
        return self.pieceType

    @Slot (result=list)
    def getBuffersList(self):
        '''
        Produces list of available buffers for given piece type
        '''

        jsons = []

        for filename in os.listdir(JSON_DIR):
            if filename.startswith(self.pieceType):
                jsons.append(filename)

        buffers = sorted([i.split('.')[0].split('_')[1] for i in jsons])
        return buffers
    
    @Slot (str)
    def setBuffer(self, buffer):
        ''' 
        Sets buffer depending on the user's choice
        '''
        self.buffer = buffer

    @Slot (result=str)
    def getBuffer(self):
        '''
        Returns buffer set before
        '''
        return self.buffer
    
    @Slot ()
    def setAvailableTargets(self):
        '''
        Produces lists of first and second targets for given piece type and buffer.
        '''
        filepath = JSON_DIR / f'{self.pieceType}_{self.buffer}.json'
        data = get_data(filepath)

        first_targets = set()
        second_targets = set()
        for k in data.keys():
            b, t1, t2 = k.split(";")
            first_targets.add(t1)
            second_targets.add(t2)

        self.first_targets = ['All'] + sorted(list(first_targets))
        self.second_targets = ['All'] + sorted(list(second_targets))
        self.cases_set = set()

    @Slot (result=list)
    def getFirstTargets(self):
        '''
        Returns list of available first targets
        '''
        
        return self.first_targets
    
    @Slot ()
    def setFirstTargets(self):
        results_list = self.getResultsList()
        first_targets = []
        for i in results_list:
            j = i.split()[0]
            if j not in first_targets:
                first_targets.append(j)
        if first_targets:
            self.first_targets = [first_targets[0]] + sorted(first_targets[1:])
        else:
            self.first_targets = []

    
    @Slot (result=list)
    def getSecondTargets(self):
        '''
        Returns list of available second targets
        '''
        return self.second_targets
    
    @Slot ()
    def setSecondTargets(self):
        results_list = self.getResultsList()
        second_targets = []
        for i in results_list:
            j = i.split()[1]
            if j not in second_targets:
                second_targets.append(j)
        if second_targets:
            self.second_targets = [second_targets[0]] + sorted(second_targets[1:])
        else:
            self.second_targets = []

    @Slot (str, str, str, result=list)
    def modifyList(self, option, first_target, second_target):
        '''
        Allows modification of the cases list in order to produce expected subset
        '''

        # if choice is 'All' get everything
        if first_target == 'All':
            first_target = [i for i in self.first_targets if i != 'All']
        else:
            first_target = [first_target]

        if second_target == 'All':
            second_target = [i for i in self.second_targets if i != 'All']
        else:
            second_target = [second_target]

        # produce set of all possible combination except for xy xy and xy yx
        new_set = set()
        for i in first_target:
            for j in second_target:
                if i != j and i != j[::-1]:
                    new_set.add(f'{i} {j}')

        # add or remove depending on the option
        if option == 'Add':
            self.cases_set.update(new_set)
        else:
            self.cases_set.difference_update(new_set)

        # if set is empty display info
        if not self.cases_set:
            return ['Click + to add comms']

        return list(self.cases_set)
    
    @Slot (str, result=list)
    def listFromFile(self, url):
        '''
        Sets subset based on provided .txt file
        '''
        filepath = url[8:]
        targets = set()
        with open(filepath) as f:
            for line in f:
                targets.add(line.strip())

        print("From file: ")
        print(targets)
        # store set in the field
        self.cases_set = targets

        # return list to update UI
        return list(targets)
    
    @Slot (str, result=list)
    def getPredefinedCasesSet(self, option="slow"):
        '''
        Sets subset based on the chosen option
        '''

        filename = f"Json/{self.pieceType}_{self.buffer}.json"
        em = ExportManager()

        functions_map = {
            'slow': em.get_top_n_cases(filename, 40, np.mean, True),
            'unstable': em.get_top_n_cases(filename, 40, np.std, True),
            'fast': em.get_top_n_cases(filename, 40, np.mean),
            'difficult': em.get_difficult_cases(filename)
        }

        targets = functions_map.get(option, [])

        if targets:
            self.cases_set = set(targets)

        # return list to update UI
        return list(self.cases_set)

    @Slot (list)
    def startGame(self, targets):
        '''
        Initializes GameManager with proper json file
        '''
        self.gm = GameManager(self.pieceType, self.buffer, targets)
        self.study_mode = False

    @Slot ()
    def incrementGameIndex(self):
        '''
        Increment index value to keep track of case number 
        '''
        self.gm.increment_index()

    @Slot (result=str)
    def getNextCase(self):
        '''
        Returns next case to be displayed (if exists)
        '''
        return self.gm.get_next_case()
    
    @Slot (result=str)
    def getCurrentAlg(self):
        '''
        Returns current alg
        '''
        return self.gm.get_current_alg()

    @Slot (result=str)
    def getCurrentMemo(self):
        '''
        Returns current case to be displayed 
        '''
        return self.gm.get_current_case()
    
    @Slot (result=str)
    def getCurrentAlgNo(self):
        '''
        Returns current alg number
        '''

        return str(self.gm.get_current_case_no())
    
    @Slot (result=str)
    def getAlgsCount(self): 
        '''
        Return total number of algs in the session
        '''
        return str(self.gm.get_cases_count())
    
    @Slot ()
    def saveResult(self):
        '''
        Calculates time delta and save it as a result for given case
        '''
        delta = (self.end - self.start).total_seconds()
        self.gm.save_result(round(delta, 2))

    @Slot (result=float)
    def getStudyMode(self):
        '''
        Returns study_mode value
        '''
        return self.study_mode

    @Slot (result=bool)
    def isGameFinished(self):
        '''
        Returns True if session is done
        '''
        return self.gm.is_game_finished()
    
    @Slot (result=str)
    def getLastResult(self):
        '''
        Returns result got for the previous case (if exists)
        '''
        return str(self.gm.get_last_result())
    
    @Slot ()
    def setStartTime(self):
        '''
        Saves current time
        '''
        self.start = datetime.now()
    
    @Slot ()
    def setEndTime(self):
        '''
        Saves current time to 'end' if endFlag is False
        '''

        if not self.endFlag:
            self.end = datetime.now()
            self.endFlag = True

    @Slot ()
    def resetEndFlag(self):
        '''
        Resets endflag
        '''
        self.endFlag = False

    @Slot ()
    def endGame(self):
        '''
        Generates lists of first and second targets to allow user modifying results before saving them
        '''
        self.setFirstTargets()
        self.setSecondTargets()


    @Slot (result = list)
    def getResultsList(self):
        '''
        Returns results list
        '''
        return self.gm.get_results_list()
    
    @Slot (str, bool, result=list)
    def removeFromResultsList(self, key, onclick=False):
        '''
        Removes result with given key from the result list
        '''

        if onclick:
            key = ' '.join(key.split()[:2])
        
        key = f"{self.buffer};{key.split()[0]};{key.split()[1]}"
        self.gm.remove_pair(key)
        self.setFirstTargets()
        self.setSecondTargets()

        return self.getResultsList()
    
    @Slot ()
    def saveResults(self):
        '''
        Saves results to the .json file
        '''
        self.gm.save_results()

    @Slot ()
    def resetGame(self):
        '''
        Resets game attributes to the initial values
        '''
        self.gm._set_game()

    @Slot ()
    def exportStats(self):
        '''
        Calls export manager to export stats
        '''
        em = ExportManager()
        em.export_stats()

    @Slot (result=str)
    def getSessionAvg(self):
        rl = self.gm.get_results_list()
        rl = [float(i.split()[2]) for i in rl]
        avg = np.mean(rl) if rl else 0
        return f"Avg: {avg:.2f}"
    
    @Slot (result=int)
    def getNumberOfExecutedAlgs(self):
        em = ExportManager()
        return em.get_algs_count()
    

    @Slot (result=str)
    def getTimeSpent(self):
        em = ExportManager()
        return em.get_time_spent()
    
    @Slot (result=str)
    def getGlobalAvg(self):
        em = ExportManager()
        return em.get_global_avg()
    
    @Slot (result=bool)
    def getDiff(self):
        self.gm.get_difficulty()
    
    @Slot ()
    def flipDiff(self):
        self.gm.flip_difficulty()