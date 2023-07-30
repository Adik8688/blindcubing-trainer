import json
import os
import pandas as pd
import numpy as np
from pathlib import Path


class SpreadsheetsManager:
    VALID_CHARS = " UDFBRLMESudfbrlw'/:,2xyz"

    def __init__(self, filepath):
        self.filepath = filepath

    @staticmethod
    def get_data(file_path):
        if not os.path.exists(file_path):
            return {}

        with open(file_path, "r") as f:
            return json.load(f)

    @staticmethod
    def save_data(data, file_path):
        with open(file_path, "w") as f:
            json.dump(data, f, indent=2)

    @staticmethod
    def clean_alg_entry(alg):
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
        return [k for k in data if key.split(";")[:-1] == k.split(";")[:-1]]

    @staticmethod
    def new_record_from_key(key):
        key = key.split(";")
        record = {
            "buffer": key[0],
            "first_target": key[1],
            "second_target": key[2],
            "results": [],
            "latest": True,
        }

        if len(key) == 4:
            record["alg"] = key[3]
            return record

        record["third_target"] = key[3]
        record["alg"] = key[4]
        return record

    def excel_to_dict_of_dfs(self):
        my_dict = pd.read_excel(self.filepath, header=None, sheet_name=None)
        my_dict = {k: df.replace(np.nan, "", regex=True) for k, df in my_dict.items()}
        return my_dict

    @staticmethod
    def df_to_alg_list(df):
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
        if df.shape[1] == 4:
            row = 1
            while df.iloc[row][0]:
                alg = SpreadsheetsManager.clean_alg_entry(df.iloc[row][3])
                key = ";".join([df.iloc[row][0], df.iloc[row][1], df.iloc[row][2], alg])
                result.append(key)
                row += 1
            return {piece_type: result}

        # parity
        row = 1
        while df.iloc[row][0]:
            alg = clean_alg_entry(df.iloc[row][4])
            key = ";".join(
                [
                    df.iloc[row][0],
                    df.iloc[row][1],
                    df.iloc[row][2],
                    df.iloc[row][3],
                    alg,
                ]
            )
            result.append(key)
            row += 1
        return {"parity": result}

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
            filepath = Path().absolute().parent / "json" / f"{piece_type}.json"
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

        piece_type = SpreadsheetsManager.buffer_to_type(df.iloc[0][1])

        result = dict()
        if df.iloc[1][0] == df.iloc[0][1]:
            for i in range(1, df.shape[1]):
                for j in range(1, df.shape[0]):
                    if df.iloc[i][j]:
                        key = f'{df.iloc[0][j]};{df.iloc[i][0]}'
                        result[key] = df.iloc[i][j]
            return {piece_type: result}


        row = 1
        while df.iloc[row][0]:
            key = f'{df.iloc[row][0]};{df.iloc[row][1]}'
            result[key] = df.iloc[row][2]
            row += 1
        return {piece_type: result}


    def update_words(self):
        words = SpreadsheetsManager.excel_to_dict_of_df(self.filepath)
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
            path_to_jsons = Path().absolute().parent / "json"

            jsons = []

            for filename in os.listdir(path_to_jsons):
                if filename.startswith(piece_type):
                    jsons.append(filename)

            print(jsons)
            for filename in jsons:
                data = SpreadsheetsManager.get_data(path_to_jsons / filename)

                for k, v in data.items():
                    try:
                        targets = f"{v['first_target']};{v['second_target']}"
                        data[k]['word'] = words[targets]
                    except KeyError:
                        pass
                
                SpreadsheetsManager.save_data(data, path_to_jsons / filename)