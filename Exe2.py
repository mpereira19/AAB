class SuffixTreeMulti:

    def __init__(self):
        self.nodes = {0: (-1, {})}  # root node
        self.num = 0

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
        prefix_code = self.find_pattern(prefix)
        res = []
        res1 = []
        if not prefix_code:
            return (0, res), (1, res1)
        else:
            for pos in prefix_code:
                if pos[1] == 0:
                    first = self.nodes_below(self.nodes[0][1][prefix[0]])
                    if len(first) == len(prefix):
                        res.append(prefix)
                    else:
                        res.append(prefix)
                        string = prefix
                        lst1 = []
                        for s in first:
                            ss = list(self.nodes[s][1].keys())
                            if '$' in ss:
                                ss.remove('$')
                                if len(ss) == 0:
                                    for i in lst1:
                                        res.append(i)
                                    break
                                else:
                                    string += ss[0]
                                    res.append(string)
                                    for i in lst1:
                                        res.append(i)
                                    lst1 = []
                            elif "$" not in ss:
                                string += ss[0]
                                lst1.append(string)

                elif pos[1] == 1:
                    first = self.nodes_below(self.nodes[0][1][prefix[0]])
                    if len(first) == len(prefix):
                        res1.append(prefix)
                    else:
                        res1.append(prefix)
                        string = prefix
                        lst2 = []
                        for s in first:
                            ss = list(self.nodes[s][1].keys())
                            if '#' in ss:
                                ss.remove('#')
                                if len(ss) == 0:
                                    for i in lst2:
                                        res1.append(i)
                                    break
                                else:
                                    string += ss[0]
                                    res1.append(string)
                                    for i in lst2:
                                        res1.append(i)
                                    lst2 = []
                            elif '#' not in ss:
                                string += ss[0]
                                lst2.append(string)
        return (0, sorted(list(set(res)))), (1, sorted(list(set(res1))))

    def largestCommonSubstring(self):
        pass


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


test()