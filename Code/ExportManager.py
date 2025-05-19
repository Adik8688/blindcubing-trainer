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
        "Latest"

    ]

    def __init__(self):
        self.df_dict = dict()

    def add_to_df(self, record):
        """
        Appends a list of values to the dataframe (stored as a dict of lists) as a new row.
        """
        for column, field in zip(ExportManager.COLUMNS, record):
            self.temp_df[column].append(field)

    def process_file(self, filepath):
        """
        Iterates through every record in the JSON file and extracts statistics.
        """
        data = get_data(filepath)

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
                r.get('latest')
            ]

            # If the algorithm string contains a comma, try analyzing with ComutatorAnalyzer.
            if "," in r.get('alg', ""):
                try:
                    ca = ComutatorAnalyzer(r['alg'])
                    record[4] = ca.get_alg_str()
                    record[7] = ca.get_move_count()
                    record[8] = ca.get_tps(get_stat(np.mean))
                except Exception as e:
                    # Log the error or print more detailed information.
                    print(f"Error processing alg '{r['alg']}': {e}")
            
            else:
                record[4] = r.get('alg')
                record[7] = len(r.get('alg').split())
                record[8] = len(r.get('alg').split()) / get_stat(np.mean) if get_stat(np.mean) != np.nan else np.nan


            self.add_to_df(record)

    def prepare_stats(self):
        """
        Prepares a dataframe with statistics for every JSON file.
        Different piece types (or buffers) are saved as different sheets in the same Excel file.
        """
        for filename in os.listdir(JSON_DIR):
            # temporary skip
            if filename.startswith('wings'):
                continue

            # Initialize a dict-of-lists for the temporary DataFrame.
            self.temp_df = {col: [] for col in ExportManager.COLUMNS}
            self.process_file(JSON_DIR / filename)

            # Only add non-empty dataframes.
            # (Consider checking if at least one column list is non-empty.)
            if any(self.temp_df.values()):
                # Convert filename to a more friendly sheet name.
                sheetname = filename.split('.')[0]
                self.temp_df = pd.DataFrame.from_dict(self.temp_df)
                self.df_dict[sheetname] = self.temp_df

    def save_stats(self):
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
        self.prepare_stats()
        self.save_stats()

        self.save_alg_sets()

    def get_algs_count(self):
        """
        Returns the total count of algorithms (i.e. total number of results across all records).
        """
        result = 0
        for filename in os.listdir(JSON_DIR):
            data = get_data(JSON_DIR / filename)
            for v in data.values():
                for alg in v['algorithms']:
                    result += len(alg.get('results', []))
        return result

    def get_time_spent(self):
        """
        Returns a formatted string (HH:MM:SS) for the total time spent based on the results.
        """
        total = 0
        for filename in os.listdir(JSON_DIR):
            data = get_data(JSON_DIR / filename)
            for v in data.values():
                for alg in v['algorithms']:
                    total += sum(alg.get('results', []))
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
        for filename in os.listdir(JSON_DIR):
            data = get_data(JSON_DIR / filename)
            for v in data.values():
                for alg in v['algorithms']:
                    total += sum(alg.get('results', []))
                    count += len(alg.get('results', []))
        return f"{total / count:.2f}" if count > 0 else "N/A"

    def export_top_n_to_file(self, df, filename, colname, n=40, asc=True):
        """
        Exports top N rows (sorted by a given column) to a text file.
        """
        df_sorted = df.sort_values(colname, ascending=asc)[:n]
        with open(FILES_DIR / filename, 'w') as f:
            for x, y in zip(df_sorted['1st target'], df_sorted['2nd target']):
                f.write(f"{x} {y}\n")

    def save_alg_sets(self):
        """
        Exports various top-N algorithm sets to text files.
        """
        for sheet, df in self.df_dict.items():
            self.export_top_n_to_file(df, f"Training_subsets/{sheet}_unstable_cases.txt", "Skew")
            self.export_top_n_to_file(df, f"Training_subsets/{sheet}_slow_cases.txt", "Mean", asc=False)
            self.export_top_n_to_file(df, f"Training_subsets/{sheet}_fast_cases.txt", "Mean")
            self.export_top_n_to_file(df, f"Training_subsets/{sheet}_low_count.txt", "Count")


    def get_top_n_cases(self, filename, n, func, reverse=False):
        raw_data = get_data(filename)

        aggregated_data = {}
        for full_key, entry in raw_data.items():
            short_key = " ".join(full_key.split(';')[1:])
            value = func(entry['algorithms'][0]['results'])
            aggregated_data[short_key] = value

        sorted_items = sorted(aggregated_data.items(), key=lambda item: item[1], reverse=reverse)

        top_keys = [key for key, _ in sorted_items[:n]]
        print(top_keys)
        return top_keys