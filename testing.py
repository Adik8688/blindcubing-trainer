from Code.SpreadsheetsManager import SpreadsheetsManager



if __name__ == '__main__':
    filepath = "Files/Edges.xlsx"
    sm = SpreadsheetsManager(filepath)

    output = sm.update_algs()
    