from Code.SpreadsheetsManager import SpreadsheetsManager
from pathlib import Path
from random import shuffle


class GameManager:
    '''
    This class handles game backend
    '''

    def __init__(self, pieceType, buffer, targets):
        

        project_root = Path(__file__).resolve().parent.parent
        JSON_DIR = project_root / "Json2"
        # path to the json file
        self.filepath = JSON_DIR / f"{pieceType}_{buffer}.json"

        # save .json to dict
        self.data = SpreadsheetsManager.get_data(self.filepath)

        self._get_latest_algs()
        self.buffer = buffer
        # assign list of targets (subset of all algs)
        self.targets = targets

        self._set_game()

    def _get_latest_algs(self):
        self.data = {k: v['algorithms'][0] for k, v in self.data.items()}

    def _set_game(self):
        '''
        Calls all necessary submethods
        '''
        self.get_game_attributes()
        self.get_shuffled_keys()
        self.index = 0
        self.size = len(self.keys)
    
    def remove_from_targets_map(self, key):
        '''
        Removes given key from the map
        '''
        self.targets_keys_map.pop(key)

    def get_game_attributes(self):
        self.data = {k: v for k, v in self.data.items() if k.split in self.targets}
        for k, v in self.targets_keys_map.items():
            key = v['key']
            alg = self.data[key]['alg']

            # word > lp > pair of targets
            if 'word' in self.data[key]:
                memo = self.data[key]['word']

            if 'lp' in self.data[key]:
                memo = self.data[key]['lp']

            else:
                memo = k
            
            self.targets_keys_map[k]['alg'] = alg
            self.targets_keys_map[k]['memo'] = memo

    def get_shuffled_keys(self):
        '''
        Returns list of keys of targets map in random order
        '''
        self.keys = list(self.targets_keys_map.keys())
        shuffle(self.keys)


    def filter_data(self, **attributes):
        '''
        Filters data on given attributes. Attrs values must be put in a list eg latest = [True]
        '''
        result = dict()
        
        for k, v in self.data.items():
            if not any(v[k1] not in v1 for k1, v1 in attributes.items()):
                result[k] = v
        
        self.data = result
    
    
    def increment_index(self):
        '''
        Increments main index
        '''
        self.index += 1
    
    def get_next_case(self):
        '''
        Returns next case (if exists)
        '''
        if self.index == self.size - 1:
            return ''
        return self.targets_keys_map[self.keys[self.index + 1]]['memo'] 

    def get_last_result(self):
        '''
        Returns last result (if exists)
        '''
        if self.index == 0:
            return ''
        return self.targets_keys_map[self.keys[self.index - 1]]['result']
            

    def get_current_alg(self):
        '''
        Returns current algorithm
        '''
        return self.targets_keys_map[self.keys[self.index]]['alg']
    
    def get_current_case(self):
        '''
        Returns current case
        '''
        return self.targets_keys_map[self.keys[self.index]]['memo']

    def get_current_case_no(self):
        '''
        Returns current case number
        '''
        return self.index + 1
    
    def get_cases_count(self):
        '''
        Returns total number of cases
        '''
        return self.size
    
    def save_result(self, result):
        '''
        Save result to the main dictionary
        '''

        # access key from the list with index, then pass the key to the main map and save result to the values
        self.targets_keys_map[self.keys[self.index]]['result'] = result

    def is_game_finished(self):
        '''
        Returns True when the session is done
        '''
        return self.index == self.size
    
    def get_results_list(self):
        '''
        Extracts results from targets map and sorts them by time
        '''
        output = []
        for k, v in self.targets_keys_map.items():
            output.append(f'{k} {v["result"]}')
        
        output = sorted(output, key=lambda x: float(x.split()[2]), reverse=True)

        return output
    
    def save_results(self):
        '''
        Saves results from the session to the json file
        '''
        for v in self.targets_keys_map.values():
            key = v['key']
            result = v['result']

            # ignores results from double click
            if result < 0.1:
                continue
            
            self.data[key]['results'].append(result)
        
        SpreadsheetsManager.save_data(self.data, self.filepath)