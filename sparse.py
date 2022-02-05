class SparseVector:
    def __init__(self, length):
        self.length = length
        self.dic = {}

    def __str__(self):
        vector = []
        for i in range(self.length):
            vector.append(self.get_pos(i))
        stringform = str(vector) 
        stringform = stringform.replace(' ', '')           
        return 'SparseVector' + stringform

    def __len__(self):
        return self.length
    
    def set_pos(self, pos, el):
        self.dic[pos] = el

    def get_pos(self, pos):
        if pos in self.dic:
            return self.dic[pos]
        else:
            return 0

    def concatenate(self, v):
        self_cat_v = SparseVector(self.length + v.length)
        for i in self.dic:
            self_cat_v.set_pos(i, self.get_pos(i))
        for i in v.dic:
            self_cat_v.set_pos((i + self.length), v.get_pos(i))
        return self_cat_v
