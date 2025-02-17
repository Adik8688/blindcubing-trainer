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

        data = dict(sorted(data.items()))

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
    def df_to_alg_dict(sheet_name, df):
        """
        Converts a DataFrame (read from an Excel sheet) into the new JSON schema.
        
        The sheet_name is expected to contain two parts separated by whitespace:
            <piece_type> <buffer>
        
        Two formats are supported:
          1. Table format (NxN grid):
             - The first cell (A1) holds the buffer.
             - The rest of the first row (B1, C1, ...) contains the first target values.
             - The first column (A2, A3, ...) contains the second target values.
             - The inner grid contains algorithm entries.
             - Detected by checking if cell A2 equals B1.
          2. List format:
             - Expected to have exactly 3 columns: target1, target2, and alg.
             - Each row (after a possible header) represents one case.
             
        Returns a dictionary in the form:
          { 
              <piece_type>: { 
                  "<buffer>;<target1>;<target2>": { "alg": <cleaned alg> }
                  ... (more cases)
              }
          }
          
        If the DataFrame structure is not recognized, returns None.
        """
        # Expect the sheet name to contain two parts: piece_type and buffer
        try:
            piece_type, buffer = sheet_name.split(maxsplit=1)
        except ValueError:
            print("Sheet name must contain both a piece type and a buffer, separated by space.")
            return None

        # Basic validation: need at least 2 rows and 2 columns and a non-empty cell at (0,1)
        if df.shape[0] < 2 or df.shape[1] < 2 or not df.iloc[0, 1]:
            return None

        new_schema = {}
        entries = {}  # Temporary dict mapping case keys to their records

        # --- CASE 1: Table format ---
        # Detect table format by checking if the cell at A2 equals B1
        if df.iloc[1, 0] == df.iloc[0, 1]:
            # In a table:
            # - First row: col0 is buffer, col1...N are first_target values.
            # - First column: row0 is buffer, row1...N are second_target values.
            # - Data cells at (row, col) for row>=1 and col>=1 contain the algorithm.
            for col in range(1, df.shape[1]):
                first_target = df.iloc[0, col]
                for row in range(1, df.shape[0]):
                    second_target = df.iloc[row, 0]
                    cell_value = df.iloc[row, col]
                    if pd.notna(cell_value) and cell_value != "":
                        alg = SpreadsheetsManager.clean_alg_entry(cell_value)
                        # Construct the key as "<buffer>;<first_target>;<second_target>"
                        key = ";".join([str(buffer), str(first_target), str(second_target)])
                        entries[key] = {"alg": alg}
            new_schema[f"{piece_type}_{buffer}"] = entries
            return new_schema

        # --- CASE 2: List format ---
        # In the list format, we expect exactly 3 columns: [target1, target2, alg]
        if df.shape[1] == 3:
            # Iterate over each row (optionally skip header if needed)
            for idx, row in df.iterrows():
                # If needed, you can skip a header row here (e.g., if idx == 0: continue)
                # Stop when the first cell is empty (assuming that marks the end)
                if not row[0]:
                    break
                target1 = row[0]
                target2 = row[1]
                cell_value = row[2]
                if pd.notna(cell_value) and cell_value != "":
                    alg = SpreadsheetsManager.clean_alg_entry(cell_value)
                    key = ";".join([str(buffer), str(target1), str(target2)])
                    entries[key] = {"alg": alg}
            new_schema[f"{piece_type}_{buffer}"] = entries
            return new_schema

        # If none of the valid formats are recognized, return None.
        return None

    def update_algs(self):
        sheets = self.excel_to_dict_of_dfs()
        algs = dict()

        for sheet_name, df in sheets.items():
            algs_dict = SpreadsheetsManager.df_to_alg_dict(sheet_name, df)

            if algs_dict is None:
                continue

            algs.update(algs_dict)

        # Process each piece type's JSON file.
        for piece_type, cases in algs.items():
            filepath = Path().absolute().parent / "Json3" / f"{piece_type}.json"
            data = SpreadsheetsManager.get_data(str(filepath))
            
            # For each case key (e.g. "UF;UB;UL") in our new data:
            for case_key, new_record in cases.items():
                new_alg = new_record["alg"]

                if case_key not in data:
                    # Case doesn't exist: add a new entry with one algorithm record.
                    data[case_key] = {
                        "algorithms": [
                            {
                                "alg": new_alg,
                                "results": [],
                                "latest": True,
                                "lp": ""
                            }
                        ]
                    }
                else:
                    # Case exists: update the existing algorithms list.
                    alg_list = data[case_key].get("algorithms", [])
                    found = False
                    for record in alg_list:
                        if record["alg"] == new_alg:
                            # Found an existing record with the same algorithm.
                            record["latest"] = True
                            found = True
                        else:
                            # Mark other records as not latest.
                            record["latest"] = False
                    if not found:
                        # New algorithm is not in the list; add it.
                        # Ensure all existing records are marked as not latest.
                        for record in alg_list:
                            record["latest"] = False
                        alg_list.append({
                            "alg": new_alg,
                            "results": [],
                            "latest": True,
                            "lp": ""
                        })
                    data[case_key]["algorithms"] = alg_list

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