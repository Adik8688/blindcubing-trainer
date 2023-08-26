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
        "Alg",
        "Mean",
        "Median",
        "Count",
        "Std",
    ]

    IN_PATH = Path().absolute().parent / "json"

    OUT_PATH = Path().absolute().parent / "exports"

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

    
    def add_to_df(self, record):
        for column, field in zip(ExportManager.COLUMNS, record):
            self.temp_df[column].append(field)
    
    def process_file(self, filepath):
        data = ExportManager.get_data(filepath)
        for r in data.values():
            results = r["results"]

            if not results:
                continue
            
            def get_stat(func):
                return round(func(results), 2)

            record = [
                r["buffer"],
                r["first_target"],
                r["second_target"],
                r["alg"],
                get_stat(np.mean),
                get_stat(np.median),
                get_stat(np.size),
                get_stat(np.std),
            ]

            self.add_to_df(record)


    def prepare_stats(self):
        for filename in os.listdir(ExportManager.IN_PATH):
            self.temp_df = {i: [] for i in ExportManager.COLUMNS}
            self.process_file(ExportManager.IN_PATH / filename)

            if self.temp_df.values():
                sheetname = filename.split('.')[0]
                sheetname = ' '.join(sheetname.split('_'))

                self.temp_df = pd.DataFrame.from_dict(self.temp_df)
                self.df_dict[sheetname] = self.temp_df

    
    def save_stats(self):
        dt = datetime.now()
        date = dt.strftime("%Y%m%d%H%M%S")
        filename = f"Export_{date}.xlsx"

        with pd.ExcelWriter(ExportManager.OUT_PATH / filename) as excel_writer:
            for sheet, df in self.df_dict.items():
                df.to_excel(excel_writer, sheet_name=sheet, index=False)


    def export_stats(self):
        self.prepare_stats()
        self.save_stats()
