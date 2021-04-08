class SuffixTreeMulti:

    def __init__(self):
        self.nodes = {0: (-1, {})}  # root node
        self.num = 0
        self.seq1 = ''
        self.seq2 = ''

    def print_tree(self):
        for k in self.nodes.keys():
            if type(self.nodes[k][0]) == int and self.nodes[k][0] < 0 or \
                    type(self.nodes[k][0]) == tuple and self.nodes[k][0][0] < 0:
                print(k, "->", self.nodes[k][1])
            else:
                print(k, ":", self.nodes[k][0])
        print(self.nodes)

    def add_node(self, origin, symbol, leafnum=-1):
        self.num += 1
        self.nodes[origin][1][symbol] = self.num
        self.nodes[self.num] = (leafnum, {})

    def add_suffix(self, p, sufnum, seq):
        pos = 0
        node = 0
        while pos < len(p):
            if p[pos] not in self.nodes[node][1].keys():
                if pos == len(p) - 1:
                    self.add_node(node, p[pos], (sufnum, seq))
                else:
                    self.add_node(node, p[pos])
            node = self.nodes[node][1][p[pos]]
            pos += 1

    def suffix_tree_from_seq(self, text, text1):
        self.seq1 = text
        self.seq2 = text1
        t = text + "$"
        t1 = text1 + '#'
        for seq in [t, t1]:
            for i in range(len(seq)):
                if seq == t:
                    self.add_suffix(seq[i:], i, 0)
                else:
                    self.add_suffix(seq[i:], i, 1)

    def find_pattern(self, pattern):
        node = 0
        for pos in range(len(pattern)):
            if pattern[pos] in self.nodes[node][1].keys():
                node = self.nodes[node][1][pattern[pos]]
            else:
                return None
        return self.get_leafes_below(node)

    def get_leafes_below(self, node):
        res = []
        if type(self.nodes[node][0]) == int and self.nodes[node][0] >= 0 or \
                type(self.nodes[node][0]) == tuple and self.nodes[node][0][0] >= 0:
            res.append(self.nodes[node][0])
        else:
            for k in self.nodes[node][1].keys():
                newnode = self.nodes[node][1][k]
                leafes = self.get_leafes_below(newnode)
                res.extend(leafes)
        return res

    def nodes_below(self, node):
        res = []
        res.append(node)
        if list(self.nodes[node][1].values()):
            for m in res:
                if type(self.nodes[node][0]) == int and self.nodes[node][0] < 0 or \
                        type(self.nodes[node][0]) == tuple and self.nodes[node][0][0] < 0:
                    res.extend(list(self.nodes[m][1].values()))
        res.remove(node)
        lst = []
        for k in self.nodes.keys():
            if type(self.nodes[k][0]) == int and self.nodes[k][0] >= 0 or \
                    type(self.nodes[k][0]) == tuple and self.nodes[k][0][0] >= 0:
                lst.append(k)
            elif type(self.nodes[k][0]) == int and self.nodes[k][0] < 0 or \
                    type(self.nodes[k][0]) == tuple and self.nodes[k][0][0] < 0:
                if '$' in self.nodes[k][1]:
                    lst.append(self.nodes[k][1]['$'])
                if '$' in self.nodes[k][1] and len(self.nodes[k][1]) == 1 or '#' in self.nodes[k][1] and\
                        len(self.nodes[k][1]) == 1:
                    lst.append(k)
                if '#' in self.nodes[k][1]:
                    lst.append(self.nodes[k][1]['#'])
        for r in lst:
            if r in res:
                res.remove(r)
        return sorted(res)

    def matches_prefix(self, prefix):
        res = []
        res1 = []
        a = 0
        b = 0
        if prefix not in self.seq1 and prefix not in self.seq2:
            return (0, res), (1, res1)

        elif prefix in self.seq1 and prefix not in self.seq2:
            for p in range(len(self.seq1)):
                if self.seq1[p] == prefix[0]:
                    a = p
                    for l in range(len(prefix)):
                        if self.seq1[p + l] == prefix[l]:
                            i = True
                            pass
                        else:
                            i = False
                            break
                    if i is True:
                        string = self.seq1[a + len(prefix):]
                        res.append(self.seq1[a:])
                        for f in range(len(string)):
                            res.append(prefix + string[:f])
                        return (0, sorted(list(set(res)), key=len)), (1, res1)

        elif prefix not in self.seq1 and prefix in self.seq2:
            for p in range(len(self.seq2)):
                if self.seq2[p] == prefix[0]:
                    b = p
                    for l in range(len(prefix)):
                        if self.seq2[p + l] == prefix[l]:
                            i = True
                            pass
                        else:
                            i = False
                            break
                    if i is True:
                        string = self.seq2[b + len(prefix):]
                        res1.append(self.seq2[b:])
                        for f in range(len(string)):
                            res1.append(prefix + string[:f])
                        return (0, res), (1, sorted(list(set(res1)), key=len))

        else:
            for p in range(len(self.seq1)):
                if self.seq1[p] == prefix[0]:
                    a = p
                    for l in range(len(prefix)):
                        if self.seq1[p + l] == prefix[l]:
                            i = True
                            pass
                        else:
                            i = False
                            break
                    if i is True:
                        string = self.seq1[a + len(prefix):]
                        res.append(self.seq1[a:])
                        for f in range(len(string)):
                            res.append(prefix + string[:f])
                        break

            for p in range(len(self.seq1)):
                if self.seq2[p] == prefix[0]:
                    b = p
                    for l in range(len(prefix)):
                        if self.seq2[p + l] == prefix[l]:
                            i = True
                            pass
                        else:
                            i = False
                            break
                    if i is True:
                        string1 = self.seq2[b + len(prefix):]
                        res1.append(self.seq2[b:])
                        for f in range(len(string1)):
                            res1.append(prefix + string1[:f])
            return (0, sorted(list(set(res)), key=len)), (1, sorted(list(set(res1)), key=len))

    def largestCommonSubstring(self):
        lst = []
        string1 = self.seq1
        string2 = self.seq2

        for sub in range(len(string1)):
            lst.append(string1[sub:])
        lst = list(set(lst))
        for p in lst:
            if p not in string2:
                lst.remove(p)
        if len(lst) == 0:
            return None
        elif len(lst) == 1:
            return lst
        else:
            sorted(lst, key=len, reverse=True)
            return lst[0]


def test():
    seq1 = 'TACTA'
    seq2 = 'AGTAC'
    stm = SuffixTreeMulti()
    stm.suffix_tree_from_seq(seq1, seq2)
    stm.print_tree()
    print(stm.find_pattern("TA"))
    print(stm.find_pattern("ACG"))
    print(stm.nodes_below(12))
    print(stm.matches_prefix('TA'))
    print(stm.matches_prefix('GT'))
    print(stm.largestCommonSubstring())

test()