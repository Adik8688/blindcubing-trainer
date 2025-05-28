import os
import pandas as pd
import numpy as np
from .project_paths import JSON_DIR
from .utils import get_data, save_data


class SpreadsheetsManager:
    '''
    This class deals with reading and processing BLD spreadsheets
    '''

    def __init__(self, filepath):
        self.filepath = filepath

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
        alg = cell_value
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

        for sheet_name, df in sheets.items():
            self.update_algs_helper(sheet_name, df)

            

    def update_algs_helper(self, sheet_name, df):
        print(f"Processing {sheet_name}")
        try:
            piece_type, buffer = sheet_name.split("_")
        except ValueError:
            print("Sheet name must contain both a piece type and a buffer, separated by _ e.g. edges_UF.")
            return

        filepath = JSON_DIR / f"{sheet_name}.json"
        data = get_data(str(filepath))

        for k, v in self.generic_df_to_dict(df, 'algs').items():
            try:
                t1, t2 = k.split(';')
            except ValueError:
                print(f"Invalid key format in sheet {sheet_name}: {k}")
                continue
            
            lp = ""
            
            t1, l1 = self.extract_lps(t1)
            t2, l2 = self.extract_lps(t2)
            
            if l1 and l2:
                lp = f"{l1}{l2}"
           
            
            case_key = f"{self.canonical_representation(buffer)};" \
                    f"{self.canonical_representation(t1)};" \
                    f"{self.canonical_representation(t2)}"

            new_alg = v["alg"]

            if case_key not in data:
                data[case_key] = {
                    'algorithms': [],
                    "difficult": False
                }

            data[case_key]['lp'] = lp
            alg_list = data[case_key]['algorithms']

            # Find existing index
            i = next((x for x, record in enumerate(alg_list) if record['alg'] == new_alg), -1)

            if alg_list:
                alg_list[0]['latest'] = False

            if i == -1:
                new_entry = {
                    "alg": new_alg,
                    "results": [],
                    "latest": True
                }
                alg_list.insert(0, new_entry)
            else:
                alg_list[0], alg_list[i] = alg_list[i], alg_list[0]
                alg_list[0]['latest'] = True

            data[case_key]["algorithms"] = alg_list

        save_data(data, str(filepath))

    @staticmethod
    def extract_lps(text):
        parts = text.split()
        if len(parts) == 2 and parts[1].startswith('(') and parts[1].endswith(')'):
            return parts[0], parts[1][1:-1]
        return text, ""
    
    @staticmethod
    def process_metadata(mapping, process_func):
        for filename in os.listdir(JSON_DIR):
            if not filename.endswith('.json'):
                continue

            file_path = JSON_DIR / filename
            data = get_data(str(file_path))
            
            for key, record in data.items():
                parts = key.split(";")
                if len(parts) < 3:
                    continue
                process_func(record, parts, mapping)
            
            save_data(data, str(file_path))
    
    def get_df_to_dict(self, df, option):
        excel = self.excel_to_dict_of_dfs()
        df = excel[list(excel.keys())[0]]
        return self.generic_df_to_dict(df, option)

    def update_memo(self):
        # Gather words from Excel sheets into a dict:
        # words_dict will be like:
        # { "first_target;second_target": word, ... }
      
        words_dict = self.get_df_to_dict(self, 'words')
        def clear_key(key):
            t1, t2 = key.split(';')
            t1 = t1.split()[0]
            t2 = t2.split()[0]
            return f"{t1};{t2}"
        
        words_dict = {clear_key(k): v for k, v in words_dict.items()} 
        
        def update(record, parts, words_dict): 
            target_key = ";".join(parts[1:])
            if target_key in words_dict:
                memo_word = words_dict[target_key]
                record['memo'] = memo_word

        self.process_metadata(words_dict, update)

    def remove_memo(self):
        def remove(record, parts, words_dict):
            record.pop("memo", None)
        
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