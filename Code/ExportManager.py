import os
import pandas as pd
import numpy as np
from scipy import stats

from .ComutatorAnalyzer import ComutatorAnalyzer
from .project_paths import JSON_DIR, EXPORTS_DIR, FILES_DIR
from .utils import get_data

class ExportManager:
    """
    This class deals with exporting statistics from the app.
    """

    # Columns for the export table.
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
        "Skew",
    ]

    def __init__(self):
        self.df_dict = dict()

    def add_to_df(self, record, temp_df):
        """
        Appends a list of values to the dataframe (stored as a dict of lists) as a new row.
        """
        for column, field in zip(ExportManager.COLUMNS, record):
            temp_df[column].append(field)

    def _process_file(self, data, temp_df):
        """
        Iterates through every record in the JSON file and extracts statistics.
        """

        for case, record in data.items():
            r = record['algorithms'][0]

            results = r.get("results", [])
            buffer, first_target, second_target = tuple(case.split(";"))

            # Helper function for calculating stats.
            def get_stat(func):
                if not results:
                    return np.nan
                return round(func(results), 2)

            record = [
                buffer,
                first_target,
                second_target,
                r.get("alg"),
                np.nan,               # Placeholder for "Alg long"
                get_stat(np.mean),
                get_stat(np.median),
                np.nan,               # Placeholder for "Move count"
                np.nan,               # Placeholder for "TPS"
                get_stat(np.size),
                get_stat(np.std),
                get_stat(np.min),
                get_stat(np.max),
                get_stat(stats.skew),
            ]
            alg = r.get('alg', '')

            if self._is_commutator(alg):
                ca = ComutatorAnalyzer(r['alg'])
                record[4] = ca.get_alg_str()
                record[7] = ca.get_move_count()
                record[8] = ca.get_tps(get_stat(np.mean))

            elif self._is_alg(alg):
                record[4] = alg
                record[7] = len(alg.split())
                if get_stat(np.mean) != np.nan:
                    record[8] = record[7] / get_stat(np.mean)

            self.add_to_df(record, temp_df)

    def _is_alg(self, alg):
        separators = ",:[]()"
        valid_moves = "UDFBRLMESudfbrlxyz"

        for sep in separators:
            alg = alg.replace(sep, " ")
    
        alg = alg.split()

        for move in alg:
            if move[0] not in valid_moves or len(move) > 3:
                return False

        return True
        
    def _is_commutator(self, alg):
        if not self._is_alg(alg):
            return False
        if alg.count(',') != 1:
            return False
        if alg.count(':') > 1:
            return False
        return True

    def write_stats_to_excel(self):
        """
        Saves calculated statistics to an Excel file.
        """

        filename = f"export_stats.xlsx"

        with pd.ExcelWriter(EXPORTS_DIR / filename) as excel_writer:
            for sheet, df in self.df_dict.items():
                df.to_excel(excel_writer, sheet_name=sheet, index=False)

    def export_stats(self):
        """
        Calls submethods to export statistics.
        """
        self.generate_stats()
        self.write_stats_to_excel()

    def generate_stats(self):
        """
        Prepares a dataframe with statistics for every JSON file.
        Different piece types (or buffers) are saved as different sheets in the same Excel file.
        """
        def process_stats(data, filename):
            temp_df = {col: [] for col in ExportManager.COLUMNS}
            self._process_file(data, temp_df)

            if any(temp_df.values()):
                sheetname = filename.split('.')[0]
                self.df_dict[sheetname] = pd.DataFrame.from_dict(temp_df)

        self.process_jsons(process_stats)

    def process_jsons(self, process_func):
        '''
        Iterates over JSON files in JSON DIR and applies process_func to each file
        '''

        for filename in os.listdir(JSON_DIR):
            if not filename.endswith('.json'):
                continue
            data = get_data(JSON_DIR / filename)
            process_func(data, filename)

    def get_algs_count(self):
        """
        Returns the total count of algorithms (i.e. total number of results across all records).
        """
        result = 0

        def count_func(data, filename):
            nonlocal result
            for v in data.values():
                for alg in v['algorithms']:
                    result += len(alg.get('results', []))

        self.process_jsons(count_func)
        return result

    def get_time_spent(self):
        """
        Returns a formatted string (HH:MM:SS) for the total time spent based on the results.
        """
        total = 0

        def time_func(data, filename):
            nonlocal total
            for v in data.values():
                for alg in v['algorithms']:
                    total += sum(alg.get('results', []))

        self.process_jsons(time_func)

        h = total // 3600
        total %= 3600
        m, s = total // 60, total % 60
        return f'{int(h):02d}:{int(m):02d}:{int(s):02d}'

    def get_global_avg(self):
        """
        Returns the global average (mean) of all results.
        """
        total = 0
        count = 0
        def avg_func(data, filename):
            nonlocal total, count
            for v in data.values():
                for alg in v['algorithms']:
                    results = alg.get('results', [])
                    total += sum(results)
                    count += len(results)

        self.process_jsons(avg_func)
        return f"{total / count:.2f}" if count > 0 else "N/A"

    def export_top_n_to_file(self, df, filename, colname, n=40, asc=True):
        """
        Exports top N rows (sorted by a given column) to a text file.
        """
        df_sorted = df.sort_values(colname, ascending=asc)[:n]
        with open(FILES_DIR / filename, 'w') as f:
            for x, y in zip(df_sorted['1st target'], df_sorted['2nd target']):
                f.write(f"{x} {y}\n")

    def get_top_n_cases(self, filename, n, func, reverse=False):
        raw_data = get_data(filename)

        aggregated_data = {}
        for full_key, entry in raw_data.items():
            short_key = " ".join(full_key.split(';')[1:])
            value = func(entry['algorithms'][0]['results'])
            aggregated_data[short_key] = value

        sorted_items = sorted(aggregated_data.items(), key=lambda item: item[1], reverse=reverse)

        top_keys = [key for key, _ in sorted_items[:n]]
        return top_keys
    
    def get_difficult_cases(self, filename):
        raw_data = get_data(filename)
        
        difficult_cases = []
        for full_key, entry in raw_data.items():
            if entry['difficult']:
                short_key = " ".join(full_key.split(';')[1:])
                difficult_cases.append(short_key)
        
        return difficult_cases