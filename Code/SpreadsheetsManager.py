import json
import os
import pandas as pd
import numpy as np
from pathlib import Path


class SpreadsheetsManager:
    '''
    This class deals with reading and processing BLD spreadsheets
    '''

    VALID_CHARS = " UDFBRLMESudfbrlw'/:,2xyz"

    def __init__(self, filepath):
        self.filepath = filepath

    @staticmethod
    def get_data(filepath):
        '''
        Returns content of json file
        '''
        if not os.path.exists(filepath):
            return {}

        with open(filepath, "r") as f:
            return json.load(f)

    @staticmethod
    def save_data(data, filepath):
        '''
        Saves data to the json file
        '''

        # data = dict(sorted(data))

        with open(filepath, "w") as f:
            json.dump(data, f, indent=2)

    @staticmethod
    def clean_alg_entry(alg):
        '''
        Filters out invalid chars and extra whitespaces before using alg
        '''

        # filtering out invalid chars
        alg = "".join([i for i in alg if i in SpreadsheetsManager.VALID_CHARS])

        # cleaning multiple spaces
        alg = " ".join(alg.split())

        # cleaning whitespaces before , : '
        i = 0
        while i < len(alg):
            if alg[i] in "':," and i > 0 and alg[i - 1] == " ":
                alg = alg[: i - 1] + alg[i:]
            else:
                i += 1

        return alg
    
    @staticmethod
    def buffer_to_type(buffer, suffix = False):
        '''
        Returns piece name depending of the buffer

        Scheme is:
        UF - edges
        UFR - corners
        UFr - wings
        Ufr - xcenters
        Uf - tcenters
        uF - midges
        '''

        if len(buffer) < 2 or len(buffer) > 3:
            return "error"
        
        piece_type = ''

        if buffer[0].islower():
            piece_type = "midges"

        elif len(buffer) == 2 and buffer[1].islower():
            piece_type = "tcenters"

        elif len(buffer) == 2:
            piece_type = "edges"
        elif buffer[1].islower():
            piece_type = "xcenters"

        elif buffer[2].islower():
            piece_type = "wings"
        
        else:
            piece_type = "corners"

        if suffix:
            piece_type = f'{piece_type}_{buffer}'
        
        return piece_type
     
    @staticmethod
    def keys_with_different_algs(data, key):
        '''
        Returns list of records which covers the same case, but might have different algorithm
        '''
        return [k for k in data if key.split(";")[:-1] == k.split(";")[:-1]]

    @staticmethod
    def new_record_from_key(key):
        '''
        Creates new record to be appended to the file from the given key
        '''

        key = key.split(";")
        return {
            "buffer": key[0],
            "first_target": key[1],
            "second_target": key[2],
            "alg": key[3],
            "results": [],
            "latest": True,
        }


    def excel_to_dict_of_dfs(self):
        '''
        Reads excel file and returns dict of pd dataframes
        '''
        my_dict = pd.read_excel(self.filepath, header=None, sheet_name=None)
        my_dict = {k: df.replace(np.nan, "", regex=True) for k, df in my_dict.items()}
        return my_dict

    @staticmethod
    def df_to_alg_list(df):
        '''
        Returns dict with piece type as a key and list of cases keys as values
        '''
        # buffer is expected to be in A1

        buffer = df.iloc[0][0]
        if not buffer or df.shape[0] < 2 or df.shape[1] < 2 or not df.iloc[0][1]:
            return None

        piece_type = SpreadsheetsManager.buffer_to_type(buffer, True)
        result = []

        # table
        if df.iloc[1][0] == df.iloc[0][1]:
            for i in range(1, df.shape[1]):
                for j in range(1, df.shape[0]):
                    if df.iloc[i][j]:
                        alg = SpreadsheetsManager.clean_alg_entry(df.iloc[i][j])
                        key = ";".join(
                            [df.iloc[0][0], df.iloc[0][j], df.iloc[i][0], alg]
                        )
                        result.append(key)
            return {piece_type: result}

        if not (df.shape[1] == 4 or df.shape[1] == 5):
            return None
        
        # list
        if df.shape[1] == 3:
            row = 1
            while df.iloc[row][0]:
                alg = SpreadsheetsManager.clean_alg_entry(df.iloc[row][2])
                key = ";".join([buffer, df.iloc[row][0], df.iloc[row][1], alg])
                result.append(key)
                row += 1
            return {piece_type: result}

    def update_algs(self):
        sheets = self.excel_to_dict_of_dfs()
        algs = dict()
        for k, df in sheets.items():
            algs_list = SpreadsheetsManager.df_to_alg_list(df)

            if algs_list is None:
                continue

            for piece_type, alg_list in algs_list.items():
                algs[piece_type] = algs.get(piece_type, []) + alg_list

        for piece_type, algs_list in algs.items():
            filepath = Path().absolute().parent / "Json" / f"{piece_type}.json"
            data = SpreadsheetsManager.get_data(str(filepath))

            for key in algs_list:
                existing_algs = SpreadsheetsManager.keys_with_different_algs(data, key)

                for k in existing_algs:
                    data[k]["latest"] = False

                if key in data:
                    data[key]["latest"] = True
                else:
                    data[key] = SpreadsheetsManager.new_record_from_key(key)

            SpreadsheetsManager.save_data(data, str(filepath))

    

    @staticmethod
    def df_to_words_dict(df):
        if df.shape[0] < 2 or df.shape[1] < 2 or not df.iloc[0][1]:
            return None

        piece_type = SpreadsheetsManager.buffer_to_type(df.iloc[1][0])

        result = dict()
        if df.iloc[1][0] == df.iloc[0][1]:
            for i in range(1, df.shape[1]):
                for j in range(1, df.shape[0]):
                    if df.iloc[i][j]:
                        key = f'{df.iloc[0][j]};{df.iloc[i][0]}'
                        result[key] = df.iloc[i][j]
            return {piece_type: result}


        for i in range(df.shape[0]):
            key = f'{df.iloc[i][0]};{df.iloc[i][1]}'
            result[key] = df.iloc[i][2]
  
        return {piece_type: result}


    def update_memo(self):
        words = self.excel_to_dict_of_dfs()
        words_dict = dict()
        for df in words.values():
            
            words_grouped_by_type = SpreadsheetsManager.df_to_words_dict(df)
            
            if words_grouped_by_type is None:
                continue
            
            for piece_type, words_grouped_by_case in words_grouped_by_type.items():
                if piece_type in words_dict:
                    words_dict[piece_type].update(words_grouped_by_case)
                else:
                    words_dict[piece_type] = words_grouped_by_case
        

        for piece_type, words in words_dict.items():
            path_to_jsons = Path().absolute().parent / "Json"

            jsons = []

            for filename in os.listdir(path_to_jsons):
                if filename.startswith(piece_type):
                    jsons.append(filename)

            for filename in jsons:
                data = SpreadsheetsManager.get_data(path_to_jsons / filename)

                for k, v in data.items():
                    try:
                        targets = f"{v['first_target']};{v['second_target']}"
                        data[k]['word'] = words[targets]
                    except KeyError:
                        pass
                
                SpreadsheetsManager.save_data(data, path_to_jsons / filename)

    @staticmethod
    def df_to_lps_dict(df):
        if df.shape[0] < 2 or df.shape[1] < 2 or not df.iloc[0][1]:
            return None

        piece_type = SpreadsheetsManager.buffer_to_type(df.iloc[1][0])

        result = dict()
        for i in range(df.shape[0]):
            result[df.iloc[i][0]] = df.iloc[i][1]
        return {piece_type: result}


    def update_lps(self):
        lps = self.excel_to_dict_of_dfs()
        lps_dict = dict()
        for df in lps.values():
            
            lps_grouped_by_type = SpreadsheetsManager.df_to_lps_dict(df)
            
            if lps_grouped_by_type is None:
                continue
            
            for piece_type, words_grouped_by_case in lps_grouped_by_type.items():
                if piece_type in lps_dict:
                    lps_dict[piece_type].update(words_grouped_by_case)
                else:
                    lps_dict[piece_type] = words_grouped_by_case
        

        for piece_type, lps in lps_dict.items():
            path_to_jsons = Path().absolute().parent / "Json"

            jsons = []

            for filename in os.listdir(path_to_jsons):
                if filename.startswith(piece_type):
                    jsons.append(filename)

            for filename in jsons:
                data = SpreadsheetsManager.get_data(path_to_jsons / filename)

                for k, v in data.items():
                    try:
                        targets = [v['first_target'], v['second_target']]
                        data[k]['lp'] = ''.join([lps[i] for i in targets])
                    except KeyError:
                        pass
                
                SpreadsheetsManager.save_data(data, path_to_jsons / filename)