import re

class Move:
    def __init__(self, move):
        self.move = move
        self._set_base_move()
        self._set_suffix(''.join([i for i in self.move if not i.isalpha()]))
        self._set_axis()


    def _get_move(self):
        return self.base_move + self.suffix

    def _set_base_move(self):
        self.base_move = ''.join([i for i in self.move if i not in "'2"])

    def _get_base_move(self):
        return self.base_move

    def _set_suffix(self, suff):
        self.suffix = suff 

    def _get_suffix(self):
        return self.suffix
    
    def _get_inv_suffix(self):
        if self.suffix == "'":
            return ''
        if self.suffix == '':
            return "'"
        return self.suffix

    def _set_axis(self):
        
        def axis_check(moves):
            return self.base_move[0] in moves
        
        if axis_check('UED'):
            self.axis = 'y'
        
        elif axis_check('LMR'):
            self.axis = 'x'

        else:
            self.axis = 'z'

    def _get_axis(self):
        return self.axis

    def _inverse_move(self):
        if self.suffix == "'":
            self.suffix = ''

        elif self.suffix == '':
            self.suffix = "'"
        
    def __repr__(self):
        return self.base_move + self.suffix
        

VALID_CHARS = " UDFBRLMESudfbrlw'/:,2xyz"


class ComutatorAnalyzer:
    def __init__(self, comm):
        self.comm = self._clean_entry(comm)
        self.alg = self._expandComm()
    
    @staticmethod
    def _clean_entry(comm):
        return "".join([ch for ch in comm if ch in VALID_CHARS])

    @staticmethod
    def _list_to_alg(alg, inv=False):
        alg = [Move(i) for i in alg]

        if inv:
            alg = alg[::-1]
            for i in alg:
                i._inverse_move()

        return alg

    @staticmethod
    def _splitted_comm_to_alg(a, b, c=''):
        base = ComutatorAnalyzer._list_to_alg(a) + ComutatorAnalyzer._list_to_alg(b) + ComutatorAnalyzer._list_to_alg(a, True) + ComutatorAnalyzer._list_to_alg(b, True)

        if c:
            return ComutatorAnalyzer._list_to_alg(c) + base + ComutatorAnalyzer._list_to_alg(c, True)
        
        return base

    def _split_comm(self):
        split_by_sep = [i.strip() for i in re.split(':|,', self.comm)]
        return [i.split() for i in split_by_sep]

    @staticmethod
    def _reduce_moves(m1, m2):
        if m1._get_axis() != m2._get_axis():
            return [m1, m2]
        
        def suff_to_pos(suffix):
            if suffix == '':
                return 1
            if suffix == '2':
                return 2
            return 3
        
        def suff_sum(s1, s2):
            pos = suff_to_pos(s1) + suff_to_pos(s2)
            return pos % 4

        def pos_to_move(base_move, pos):
            if pos == 0:
                return ''
            if pos == 1: 
                return Move(base_move)
            if pos == 2:
                return Move(base_move + '2')
            return Move(base_move + "'")


        if m1._get_base_move() == m2._get_base_move():

            pos = suff_sum(m1._get_suffix(), m2._get_suffix())
            
            return [pos_to_move(m1._get_base_move(), pos)]
        
        if m1._get_axis() == 'x':
            order = ['R', 'Rw', 'M', 'Lw', 'L']

        elif m1._get_axis() == 'y':
            order = ['U', 'Uw', 'E', 'Dw', 'D']
        
        else:
            order = ['B', 'Bw', 'S', 'Fw', 'F']


        if order.index(m1._get_base_move()) > order.index(m2._get_base_move()):
            m1, m2 = m2, m1
        
        b1, b2 = m1._get_base_move(), m2._get_base_move()
        s1, s2 = m1._get_suffix(), m2._get_suffix()

        if b1 == order[0]:
            if s1 == m2._get_inv_suffix():
                if b2 == order[1]:
                    return [Move(order[2] + m2._get_inv_suffix())]
                if b2 == order[2]:
                    return [Move(order[1] + s1)]
            
            if b2 == order[1]:
                pos = suff_sum(s1, s2)
                return [pos_to_move(b1, pos), Move(order[2] + m2._get_inv_suffix())]

        if b1 == order[1] and b2 == order[2]:
            if s1 == s2:
                return [Move(order[0] + s1)]
            
            else:
                pos = suff_sum(m1._get_inv_suffix(), s2)
                return [Move(order[0] + s1), pos_to_move(b2, pos)]

        
        if b1 == order[2] and b2 == order[3]:
            if s1 == m2._get_inv_suffix():
                return [Move(order[4] + m2._get_inv_suffix())]
            else:
                pos = suff_sum(s1, s2)
                return [Move(order[4] + s2), pos_to_move(b1, pos)]

        
        if b1 == order[2] and b2 == order[4] and s1 == s2:
            return [Move(order[3] + s2)]
        
        if b1 == order[3] and b2 == order[4]:
            if s1 == m2._get_inv_suffix():
                return [Move(order[2] + s1)]
            else:
                pos = suff_sum(s1, s2)
                return [pos_to_move(b2, pos), Move(order[2] + s1)]
        
        return [m1, m2]
 

    def _expandComm(self):
        splitted_comm = self._split_comm()   

        a, b = splitted_comm[-2], splitted_comm[-1]
        c = splitted_comm[0] if splitted_comm[0] != splitted_comm[-2] else ''

        alg = ComutatorAnalyzer._splitted_comm_to_alg(a, b, c)

        i = 0
        while i < len(alg) - 1:
            try:
                reduced_pair = ComutatorAnalyzer._reduce_moves(alg[i], alg[i + 1])
            except:
                i += 1
                continue

            if reduced_pair != alg[i : i + 2] and reduced_pair != alg[i : i + 2][::-1]:
                if not reduced_pair[0]: 
                    reduced_pair = []
                alg = alg[:i] + reduced_pair + alg[i + 2:]
                i = 0

            else:
                i+=1

        return alg

    def get_alg_str(self):
        return ' '.join([i._get_move() for i in self.alg])
    
    def get_move_count(self):
        return sum([1 for _ in self.alg])

    def get_tps(self, time):
        mc = self.get_move_count()
        return round(mc/time, 2)



        