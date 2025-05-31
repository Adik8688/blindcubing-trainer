from random import shuffle
from .project_paths import JSON_DIR
from .utils import get_data, save_data

class GameManager:
    '''
    This class handles game backend
    '''

    def __init__(self, pieceType, buffer, targets):

        self.buffer = buffer
        self.filepath = JSON_DIR / f"{pieceType}_{self.buffer}.json"
        self.data = get_data(self.filepath)
        
        self.keys = [f"{buffer};{';'.join(t.split())}" for t in targets]
        self.keys = [k for k in self.keys if k in self.data]
        self.shuffled_keys = self.keys.copy()


        self._set_game()

    def _set_game(self):
        '''
        Calls all necessary submethods
        '''

        shuffle(self.shuffled_keys)
        self.new_results = dict()

        self.index = 0
        self.size = len(self.keys)

    def remove_pair(self, key):
        '''
        Remove results from game session before saving
        '''
        self.new_results.pop(key)
    
    def increment_index(self):
        '''
        Increments main index
        '''
        self.index += 1
  
    def get_case(self, key):
        memo = self.data[key].get('memo', '')
        if memo:
            return memo
        
        return self.data[key]['lp']

    def get_current_key(self):
        '''
        Returns current key
        '''
        return self.shuffled_keys[self.index]


    def get_current_case(self):
        '''
        Returns current case
        '''
        key = self.get_current_key()
        return self.get_case(key)


    def get_next_case(self):
        '''
        Returns next case (if exists)
        '''
        if self.index == self.size - 1:
            return ''
        
        key = self.shuffled_keys[self.index + 1]
        return self.get_case(key)


    def get_last_result(self):
        '''
        Returns last result (if exists)
        '''
        if self.index == 0:
            return ''
        
        key = self.shuffled_keys[self.index - 1]
        return self.new_results.get(key)
            

    def get_current_alg(self):
        '''
        Returns current algorithm
        '''
        key = self.shuffled_keys[self.index]
        return self.data[key]['algorithms'][0]['alg']
    
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
        key = self.get_current_key()
        self.new_results[key] = result

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
        for k, v in self.new_results.items():
            _, t1, t2 = k.split(";")
            output.append(f'{t1} {t2} {v}')
        
        output = sorted(output, key=lambda x: float(x.split()[-1]), reverse=True)

        return output
    
    def get_difficulty(self):
        '''
        Get difficulty flag of current case alg
        '''
        key = self.get_current_key()
        diff = self.data[key]['difficult']
        print(f"Current difficulty: {diff}")
        return 
    
    def flip_difficulty(self):
        '''
        Set difficulty flag to opposite
        '''

        key = self.get_current_key()
        diff = self.data[key]['difficult']
        self.data[key]['difficult'] = not diff
        print(f"Difficulty after change: {self.data[key]['difficult']}")

    def save_results(self):
        '''
        Saves results from the session to the json file
        '''
        for k in self.shuffled_keys:
            
            if k not in self.new_results:
                continue
            
            new_res = self.new_results[k]

            # ignores results from double click
            if new_res < 0.2:
                continue

            self.data[k]['algorithms'][0]['results'].append(new_res)
        
        save_data(self.data, self.filepath)