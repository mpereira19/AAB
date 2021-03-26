# -*- coding: utf-8 -*-

class SuffixTree:

    def __init__(self):
        self.nodes = {0: (-1, {})}  # root node
        self.num = 0

    def print_tree(self):
        for k in self.nodes.keys():
            if self.nodes[k][0] < 0:
                print(k, "->", self.nodes[k][1])
            else:
                print(k, ":", self.nodes[k][0])

    def add_node(self, origin, symbol, leafnum=-1):
        self.num += 1
        self.nodes[origin][1][symbol] = self.num
        self.nodes[self.num] = (leafnum, {})

    def add_suffix(self, p, sufnum):
        pos = 0
        node = 0
        while pos < len(p):
            if p[pos] not in self.nodes[node][1].keys():
                if pos == len(p) - 1:
                    self.add_node(node, p[pos], sufnum)
                else:
                    self.add_node(node, p[pos])
            node = self.nodes[node][1][p[pos]]
            pos += 1

    def suffix_tree_from_seq(self, text):
        t = text + "$"
        for i in range(len(t)):
            self.add_suffix(t[i:], i)

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
        if self.nodes[node][0] >= 0:
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
                if self.nodes[node][0] < 0:
                    res.extend(list(self.nodes[m][1].values()))
        res.remove(node)
        lst = []
        for k in self.nodes.keys():
            if self.nodes[k][0] >= 0:
                lst.append(k)
            elif self.nodes[k][0] < 0:
                if '$' in self.nodes[k][1]:
                    lst.append(self.nodes[k][1]['$'])
                if '$' in self.nodes[k][1] and len(self.nodes[k][1]) == 1:
                    lst.append(k)
        for r in lst:
            if r in res:
                res.remove(r)
        return sorted(res)

    def matches_prefix(self, prefix):
        prefix_code = self.find_pattern(prefix)
        res = []
        if not prefix_code:
            return res
        else:
            res.append(prefix)
            for pos in prefix_code:
                first = self.nodes_below(pos + len(prefix) - 1)
                if first == [pos + len(prefix)]:
                    res.append(prefix)
                else:
                    string = prefix
                    for s in first:
                        ss = list(self.nodes[s][1].keys())
                        if '$' in ss and len(ss) > 1:
                            string += ss[0]
                            res.append(string)
                            ss.remove('$')
                        elif '$' not in ss:
                            string += ss[0]
                            res.append(string)
        return sorted(list(set(res)))


def test():
    seq = "GADGGFGGGGGGGGGHLDHOFOIGJKCTA"
    st = SuffixTree()
    st.suffix_tree_from_seq(seq)
    st.print_tree()
    print()
    print(st.find_pattern("TA"))
    # print(st.find_pattern("ACG"))
    print(st.nodes_below(0))
    print(st.matches_prefix('TA'))


def test2():
    seq = "TACTA"
    st = SuffixTree()
    st.suffix_tree_from_seq(seq)
    print(st.find_pattern("TA"))
    # print(st.repeats(2, 2))


test()
print()
test2()
