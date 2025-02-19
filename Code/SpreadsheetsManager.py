import json
import os
import pandas as pd
import numpy as np
from pathlib import Path
from .project_paths import JSON_DIR


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
    def iterate_table_cells(df):
        for col in range(1, df.shape[1]):
            first_target = df.iloc[0, col]
            for row in range(1, df.shape[0]):
                second_target = df.iloc[row, 0]
                cell_value = df.iloc[row, col]
                yield first_target, second_target, cell_value

    @staticmethod
    def iterate_list_rows(df, num_cols=3):
        for idx, row in df.iterrows():
            if not row[0]:
                break
            yield tuple(row.iloc[:num_cols])
    

    def generic_df_to_dict(self, df, option):
        if df.shape[0] < 2 or df.shape[1] < 2 or not df.iloc[0, 1]:
            return None
    
        option_map = {
            'algs': self.df_to_alg,
            'words': self.df_to_words,
            'lps': self.df_to_lps
        }
        processing_function = option_map[option]

        entries = dict()

        # table
        if df.iloc[1, 0] == df.iloc[0, 1]:
            for first_target, second_target, cell_value in self.iterate_table_cells(df):
                if cell_value != "":
                    processing_function(entries, first_target, second_target, cell_value)
            return entries
        
        # list
        if option == "algs" and not df.shape[1] == 3:
                return None
        
        if option == "lps":
            for col1, col2 in self.iterate_list_rows(df, 2):
                if col2 != "":
                    processing_function(entries, col1, col2)
            return entries
        
        for col1, col2, col3 in self.iterate_list_rows(df):
            if col3 != "":
                processing_function(entries, col1, col2, col3)
        return entries
    
    @staticmethod
    def df_to_alg(entries, first_target, second_target, cell_value):
        alg = SpreadsheetsManager.clean_alg_entry(cell_value)
        key = ";".join([str(first_target), str(second_target)])
        entries[key] = {"alg": alg}

    @staticmethod
    def df_to_words(entries, first_target, second_target, cell_value):
        key = f"{first_target};{second_target}"
        entries[key] = cell_value

    @staticmethod
    def df_to_lps(entries, first_target, cell_value):
        key = first_target
        entries[key] = cell_value
   

    def update_algs(self):
        sheets = self.excel_to_dict_of_dfs()
        algs = dict()

        for sheet_name, df in sheets.items():
            try:
                _, buffer = sheet_name.split("_")
            except ValueError:
                print("Sheet name must contain both a piece type and a buffer, separated by _ e.g. edges_UF.")
                break
            
            print(f"Processing {sheet_name}")

            algs_dict = {}
            for k, v in self.generic_df_to_dict(df, 'algs').items():
                t1, t2 = k.split(';')
                key = f"{self.canonical_representation(buffer)};{self.canonical_representation(t1)};{self.canonical_representation(t2)}"
                algs_dict[key] = v



            if algs_dict is None:
                continue

            algs.update({sheet_name: algs_dict})

        # Process each piece type's JSON file.
        for piece_type, cases in algs.items():
            filepath = JSON_DIR / f"{piece_type}.json"
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
                    data[case_key]["algorithms"] = sorted(alg_list, key=lambda x: not x['latest'])

            SpreadsheetsManager.save_data(data, str(filepath))

    @staticmethod
    def process_metadata(mapping, process_func):
        for filename in os.listdir(JSON_DIR):
            if not filename.endswith('.json'):
                continue

            file_path = JSON_DIR / filename
            data = SpreadsheetsManager.get_data(str(file_path))
            
            for key, record in data.items():
                parts = key.split(";")
                if len(parts) < 3:
                    continue
                process_func(record, parts, mapping)
            
            SpreadsheetsManager.save_data(data, str(file_path))
    
    def get_df_to_dict(self, df, option):
        excel = self.excel_to_dict_of_dfs()
        df = excel[list(excel.keys())[0]]
        return self.generic_df_to_dict(df, option)

    def update_memo(self):
        # Gather words from Excel sheets into a dict:
        # words_dict will be like:
        # { "first_target;second_target": word, ... }
      
        words_dict = self.get_df_to_dict(self, 'words')

        def update(record, parts, words_dict):  
            target_key = f"{parts[1]};{parts[2]}"
            if target_key in words_dict:
                memo_word = words_dict[target_key]
                # Update every algorithm record in this case with the 'memo'
                if "algorithms" in record:
                    for alg_record in record["algorithms"]:
                        alg_record["memo"] = memo_word

        self.process_metadata(words_dict, update)

    def remove_memo(self):
        def remove(record, parts, words_dict):
            for alg in record['algorithms']:
                alg.pop("memo", None)
        
        self.process_metadata({}, remove)

    def update_lps(self):
        # Load LP mapping(s) from Excel. Expecting a mapping of the form: { "UB": "A", "UL": "B", ... }
        lps_dict = self.get_df_to_dict(self, 'lps')

        def update(record, parts, lps_dict):
            first_target = parts[1]
            second_target = parts[2]

            # Look up the letters from the LP mapping.
            letter1 = lps_dict.get(first_target, "")
            letter2 = lps_dict.get(second_target, "")
            lp_value = letter1 + letter2

            # Update each algorithm record in the 'algorithms' list with the LP.
            if "algorithms" in record:
                for alg_record in record["algorithms"]:
                    alg_record["lp"] = lp_value

        self.process_metadata(lps_dict, update)
    
    def remove_lps(self):
        def remove(record, parts, lps_dict):
            for alg in record['algorithms']:
                alg.pop("lp", None)
        
        self.process_metadata({}, remove)

    @staticmethod
    def canonical_representation(piece_name):
        if not piece_name:
            return ""
        
        if piece_name.upper() != piece_name or len(piece_name) != 3:
            return piece_name
        
        order = ['U', 'D', 'F', 'B', 'R', 'L']
        order_index = {letter: index for index, letter in enumerate(order)}


        active = piece_name[0]
        rest = sorted(piece_name[1:], key=lambda letter: order_index[letter])
        return active + ''.join(rest)