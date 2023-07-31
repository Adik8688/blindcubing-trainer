from Code.SpreadsheetsManager import SpreadsheetsManager
from pathlib import Path

class GameManager:


    def __init__(self, filename, targets):
        self.filepath = Path().absolute().parent / 'json' / filename
        self.data = SpreadsheetsManager.get_data(self.filepath)
        self.filter_data(latest = [True])
        self.targets = targets
        self.map_targets_to_keys()
        self.get_game_attributes()


    def map_targets_to_keys(self):
        self.targets_keys_map = dict()
        while self.targets:
            t, self.targets = self.targets[0], self.targets[1:]

            for k in self.data.keys():
                d_targets = k.split(';')[1:3]
                if t == " ".join(d_targets):
                    self.targets_keys_map[t] = {'key': k}
                    break
    
    def get_game_attributes(self):
        for k, v in self.targets_keys_map.items():
            key = v['key']
            alg = self.data[key]['alg']
            if 'word' in self.data[key]:
                memo = self.data[key]['word']

            if 'lp' in self.data[key]:
                memo = self.data[key]['lp']

            else:
                memo = k
            
            self.targets_keys_map[k]['alg'] = alg
            self.targets_keys_map[k]['memo'] = memo

        for k, v in self.targets_keys_map.items():
            print(k)
            for k1, v1 in v.items():
                print('\t', k1, ':', v1)


    def filter_data(self, **attributes):
        result = dict()
        
        for k, v in self.data.items():
            if not any(v[k1] not in v1 for k1, v1 in attributes.items()):
                result[k] = v
        
        self.data = result

    