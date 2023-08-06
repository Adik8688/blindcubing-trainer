import json
import os
from pathlib import Path
import pandas as pd
import numpy as np
from datetime import datetime

class ExportManager:
    COLUMNS = [
        "Buffer",
        "1st target",
        "2nd target",
        "Algs",
        "Mean",
        "Median",
        "Count",
        "Std",
    ]

    PIECES_ORDER = [
        'corners',
        'edges',
        'wings',
        'xcenters',
        'midges',
        'tcenters'
    ]

    IN_PATH = Path().absolute().parent / 'json'

    OUT_PATH = Path().absolute().parent / 'exports'

    def __init__(self):
        self.df_dict = dict()

    @staticmethod
    def get_data(filepath):
        if not os.path.exists(filepath):
            return {}

        with open(filepath, "r") as f:
            return json.load(f)

    @staticmethod
    def save_data(data, filepath):
        with open(filepath, "w") as f:
            json.dump(data, f, indent=2)
    
    def prepare_stats(self):
        for piece_name in ExportManager.PIECES_ORDER:
            df = {i: [] for i in ExportManager.COLUMNS}

            for filename in os.listdir(ExportManager.IN_PATH):
                if filename.startswith(piece_name):
                    self.process_file(ExportManager.IN_PATH / filename, df)
        
            if df[ExportManager.COLUMNS[0]]: 
                df = pd.DataFrame.from_dict(df)
                self.df_dict[piece_name] = df

    def save_stats(self):
        dt = datetime.now()
        date = dt.strftime("%Y%m%d%H%M%S")
        filename = f'Export_{date}.xlsx'

        with pd.ExcelWriter(ExportManager.OUT_PATH / filename) as excel_writer:
            for sheet, df in self.df_dict.items():
                df.to_excel(excel_writer, sheet_name=sheet, index=False)
                    
    def process_file(self, filepath, dataframe):
        data = ExportManager.get_data(filepath)
        for r in data.values():
            results = r['results']

            if not results:
                continue

            record = []
            record.append(r['buffer'])
            record.append(r['first_target'])
            record.append(r['second_target'])
            record.append(r['alg'])
            record.append(ExportManager.calculate_stats(np.mean, results))
            record.append(ExportManager.calculate_stats(np.median, results))
            record.append(ExportManager.calculate_stats(np.size, results))
            record.append(ExportManager.calculate_stats(np.std, results))
            
            self.add_to_df(record, dataframe)


    def add_to_df(self, record, dataframe):
        for column, field in zip(ExportManager.COLUMNS, record):
            dataframe[column].append(field)   

    @staticmethod
    def calculate_stats(func, results):
        return round(func(results), 2)
    
    def export_stats(self):
        self.prepare_stats()
        self.save_stats()