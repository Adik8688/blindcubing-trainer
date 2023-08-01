from Code.SpreadsheetsManager import SpreadsheetsManager
from pathlib import Path
from random import shuffle


class GameManager:


    def __init__(self, filename, targets):
        self.filepath = Path().absolute().parent / 'json' / filename
        self.data = SpreadsheetsManager.get_data(self.filepath)
        self.filter_data(latest = [True])
        self.targets = targets
        self.map_targets_to_keys()
        self.get_game_attributes()
        self.get_shuffled_keys()
        self.index = 0
        self.size = len(self.keys)


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

    def get_shuffled_keys(self):
        self.keys = list(self.targets_keys_map.keys())
        shuffle(self.keys)


    def filter_data(self, **attributes):
        result = dict()
        
        for k, v in self.data.items():
            if not any(v[k1] not in v1 for k1, v1 in attributes.items()):
                result[k] = v
        
        self.data = result
    
    
    def increment_index(self):
        self.index += 1
    
    def get_next_alg(self):
        if self.index == self.size - 1:
            return ''
        return self.targets_keys_map[self.keys[self.index + 1]]['memo'] 

    def get_last_result(self):
        if self.index == 0:
            return ''
        return self.targets_keys_map[self.keys[self.index - 1]]['result']
            

    def get_current_alg(self):
        return self.targets_keys_map[self.keys[self.index]]['alg']
    
    def get_current_memo(self):
        return self.targets_keys_map[self.keys[self.index]]['memo']

    def get_current_alg_no(self):
        return self.index + 1
    
    def get_algs_count(self):
        return self.size
    
    def save_result(self, result):
        self.targets_keys_map[self.keys[self.index]]['result'] = result

    def is_game_finished(self):
        return self.index == self.size
    
    def get_results_list(self):
        output = []
        for k, v in self.targets_keys_map.items():
            output.append(f'{k} {v["result"]}')
        return output