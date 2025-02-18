import json
import os
from pathlib import Path
import pandas as pd
import numpy as np
from datetime import datetime
from scipy import stats

from ComutatorAnalyzer import ComutatorAnalyzer




class ExportManager:
    '''
    This class deals with exporting statistics from the app
    '''

    COLUMNS = [
        "Buffer",
        "1st target",
        "2nd target",
        "Alg",
        "Alg long",
        "Mean",
        "Median",
        "Move count",
        "TPS",
        "Count",
        "Std",
        "Best",
        "Worst",
        "Skew"
    ]

    IN_PATH = Path().absolute().parent / "Json"

    OUT_PATH = Path().absolute().parent / "Exports"

    OUT_FILES_PATH = Path().absolute().parent / "Files"

    def __init__(self):
        self.df_dict = dict()

    @staticmethod
    def get_data(filepath):
        '''
        Returns content of json file under given path
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
        with open(filepath, "w") as f:
            json.dump(data, f, indent=2)

    
    def add_to_df(self, record):
        '''
        Appends list of values to the dataframe as a new row
        '''
        for column, field in zip(ExportManager.COLUMNS, record):
            self.temp_df[column].append(field)
    
    def process_file(self, filepath):
        '''
        Interates thorugh every record in the json file and extract information from them
        '''

        data = ExportManager.get_data(filepath)

        for r in data.values():
            results = r["results"]

            # skip records with empty results list
            if not results:
                continue
            
            # helper function for calculating stats
            def get_stat(func):
                return round(func(results), 2)

            record = [
                r["buffer"],
                r["first_target"],
                r["second_target"],
                r["alg"],
                np.nan,
                get_stat(np.mean),
                get_stat(np.median),
                np.nan,
                np.nan,
                get_stat(np.size),
                get_stat(np.std),
                get_stat(np.min),
                get_stat(np.max),
                get_stat(stats.skew)
            ]

            if "," in r['alg']:
                try:
                    ca = ComutatorAnalyzer(r['alg'])
                    record[4] = ca.get_alg_str()
                    record[7] = ca.get_move_count()
                    record[8] = ca.get_tps(get_stat(np.mean))
                except:
                    print(r['alg'])

            self.add_to_df(record)


    def prepare_stats(self):
        '''
        Prepares dataframe with stats for every json file.
        Different piece types with different buffers are saved as different sheets of the same excel file
        '''
        for filename in os.listdir(ExportManager.IN_PATH):
            self.temp_df = {i: [] for i in ExportManager.COLUMNS}
            self.process_file(ExportManager.IN_PATH / filename)

            if self.temp_df.values():
                # convert file name to the sheet name
                sheetname = filename.split('.')[0]
                sheetname = ' '.join(sheetname.split('_'))

                self.temp_df = pd.DataFrame.from_dict(self.temp_df)
                self.df_dict[sheetname] = self.temp_df

    
    def save_stats(self):
        '''
        Saves calculated statistics to the excel file
        '''
        dt = datetime.now()

        for file in os.listdir(self.OUT_PATH):
            file_path = os.path.join(self.OUT_PATH, file)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)  # Remove the file
            except Exception as e:
                print(f"Error while deleting file {file_path}: {e}")

        # current time string to asure unique file name
        date = dt.strftime("%Y%m%d%H%M%S")
        filename = f"Export_{date}.xlsx"

        with pd.ExcelWriter(ExportManager.OUT_PATH / filename) as excel_writer:
            for sheet, df in self.df_dict.items():
                df.to_excel(excel_writer, sheet_name=sheet, index=False)


    def export_stats(self):
        '''
        Calls submethods to export statistics
        '''
        self.prepare_stats()
        self.save_stats()
        self.save_alg_sets()

    def get_algs_count(self):
        result = 0
        for filename in os.listdir(ExportManager.IN_PATH):
            data = ExportManager.get_data(ExportManager.IN_PATH / filename)
            for v in data.values():
                result += len(v['results'])

        return result
    
    def get_time_spent(self):
        total = 0
        for filename in os.listdir(ExportManager.IN_PATH):
            data = ExportManager.get_data(ExportManager.IN_PATH / filename)
            for v in data.values():
                total += sum(v['results'])

        h = total // 3600
        total = total % 3600
        m, s = total // 60, total % 60

        return f'{int(h):02d}:{int(m):02d}:{int(s):02d}'
    
    def get_global_avg(self):
        total = 0
        comm_num = 0
        for filename in os.listdir(ExportManager.IN_PATH):
            data = ExportManager.get_data(ExportManager.IN_PATH / filename)
            for v in data.values():
                total += sum(v['results'])
                comm_num += len(v['results'])

        return f"{total/comm_num:.2f}"
        
    def export_top_n_to_file(self, df, filename, colname, n=40, asc=True):
        df_sorted = df.sort_values(colname, ascending=asc)[:n]
        with open( self.OUT_FILES_PATH / filename, 'w') as f:
            for x, y in zip(df_sorted['1st target'], df_sorted['2nd target']):
                f.write(f"{x} {y}\n")

    def save_alg_sets(self):
        for sheet, df in self.df_dict.items():
            self.export_top_n_to_file(df, f"{sheet}_unstable_cases.txt", "Skew")
            self.export_top_n_to_file(df, f"{sheet}_slow_cases.txt", "Mean", asc=False)
            self.export_top_n_to_file(df, f"{sheet}_fast_cases.txt", "Mean")
            self.export_top_n_to_file(df, f"{sheet}_low_count.txt", "Count")
