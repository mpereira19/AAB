# -*- coding: utf-8 -*-

class Automata:
    
    def __init__(self, alphabet, pattern):
        self.numstates = len(pattern) + 1
        self.alphabet = alphabet
        self.transitionTable = {}
        self.buildTransitionTable(pattern)        
    
    def buildTransitionTable(self, pattern):
        """
        Construção da tabela de transições
        """
        for q in range(self.numstates):
            for a in self.alphabet:
                self.transitionTable[(q, a)] = overlap(pattern[:q] + a, pattern)
       
    def printAutomata(self):
        print("States: ", self.numstates)
        print("Alphabet: ", self.alphabet)
        print("Transition table:")
        for k in self.transitionTable.keys():
            print(k[0], ",", k[1], " -> ", self.transitionTable[k])
         
    def nextState(self, current, symbol):
        return self.transitionTable[(current, symbol)]

    def applySeq(self, seq):
        q = 0
        res = [q]
        for c in seq:
            q = self.nextState(q, c)
            res.append(q)
        return res
        
    def applySeq1(self, seq):
        q = 0
        return [q]+[self.nextState(q,c) for c in seq]
        
    def occurencesPattern(self, text):
        q = 0 
        res = []
        for c in range(len(text)):
            q = self.nextState(q, text[c])
            if q == self.numstates-1:
                res.append(c - self.numstates + 2)
        return res


def overlap(s1, s2):
    maxov = min(len(s1), len(s2))
    for i in range(maxov, 0, -1):
        if s1[-i:] == s2[:i]:
            return i
    return 0


def test():
    auto = Automata("AC", "ACA")
    auto.printAutomata()
    print(auto.applySeq1("CACAACAA"))
    print(auto.occurencesPattern("CACAACAA"))


test()

# States:  4
# Alphabet:  AC
# Transition table:
# 0 , A  ->  1
# 0 , C  ->  0
# 1 , A  ->  1
# 1 , C  ->  2
# 2 , A  ->  3
# 2 , C  ->  0
# 3 , A  ->  1
# 3 , C  ->  2
# [0, 0, 1, 2, 3, 1, 2, 3, 1]
# [1, 4]
