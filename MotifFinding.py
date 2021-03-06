from MySeq import MySeq
from MyMotifs import MyMotifs

class MotifFinding:

    def __init__(self, size=8, seqs=None):
        self.motifSize = size
        if seqs is not None:
            self.seqs = seqs
            self.alphabet = seqs[0].alfabeto()
        else:
            self.seqs = []

    def __len__(self):
        return len(self.seqs)

    def __getitem__(self, n):
        return self.seqs[n]

    def seqSize(self, i):
        return len(self.seqs[i])

    def readFile(self, fic, t):
        for s in open(fic, "r"):
            self.seqs.append(MySeq(s.strip().upper(), t))
        self.alphabet = self.seqs[0].alfabeto()

    def createMotifFromIndexes(self, indexes):
        pseqs = []
        for i, ind in enumerate(indexes):
            pseqs.append(MySeq(self.seqs[i][ind:(ind + self.motifSize)], self.seqs[i].tipo))
        return MyMotifs(pseqs)

    # SCORES

    def score(self, s):
        score = 0
        motif = self.createMotifFromIndexes(s)
        motif.doCounts()
        mat = motif.counts
        for j in range(len(mat[0])):
            maxcol = mat[0][j]
            for i in range(1, len(mat)):
                if mat[i][j] > maxcol:
                    maxcol = mat[i][j]
            score += maxcol
        return score

    def score_pseudo(self, s):
        score = 0
        motif = self.createMotifFromIndexes(s)
        motif.doCounts()
        mat = motif.counts
        mat = [[mat[lin][col] + 1 for col in range(len(mat[0]))] for lin in range(len(mat))]
        for j in range(len(mat[0])):
            maxcol = mat[0][j]
            for i in range(1, len(mat)):
                if mat[i][j] > maxcol:
                    maxcol = mat[i][j]
            score += maxcol
        return score

    def scoreMult(self, s, no_new_pwm=[]):
        score = 1.0
        motif = self.createMotifFromIndexes(s)
        if no_new_pwm == []:
            motif.createPWM()
            mat = motif.pwm
        else:
            mat = no_new_pwm
        for j in range(len(mat[0])):
            maxcol = mat[0][j]
            for i in range(1, len(mat)):
                if mat[i][j] > maxcol:
                    maxcol = mat[i][j]
            score *= maxcol
        return score

        # EXHAUSTIVE SEARCH

    def nextSol(self, s):
        nextS = [0] * len(s)
        pos = len(s) - 1
        while pos >= 0 and s[pos] == self.seqSize(pos) - self.motifSize:
            pos -= 1
        if pos < 0:
            nextS = None
        else:
            for i in range(pos):
                nextS[i] = s[i]
            nextS[pos] = s[pos] + 1
            for i in range(pos + 1, len(s)):
                nextS[i] = 0
        return nextS

    def exhaustiveSearch(self):
        melhorScore = -1
        res = []
        s = [0] * len(self.seqs)
        while s is not None:
            sc = self.score(s)
            if sc > melhorScore:
                melhorScore = sc
                res = s
            s = self.nextSol(s)
        return res

    # BRANCH AND BOUND     

    def nextVertex(self, s):
        res = []
        if len(s) < len(self.seqs):  # internal node -> down one level
            for i in range(len(s)):
                res.append(s[i])
            res.append(0)
        else:  # bypass
            pos = len(s) - 1
            while pos >= 0 and s[pos] == self.seqSize(pos) - self.motifSize:
                pos -= 1
            if pos < 0:
                res = None  # last solution
            else:
                for i in range(pos): res.append(s[i])
                res.append(s[pos] + 1)
        return res

    def bypass(self, s):
        res = []
        pos = len(s) - 1
        while pos >= 0 and s[pos] == self.seqSize(pos) - self.motifSize:
            pos -= 1
        if pos < 0:
            res = None
        else:
            for i in range(pos): res.append(s[i])
            res.append(s[pos] + 1)
        return res

    def branchAndBound(self):
        melhorScore = -1
        melhorMotif = None
        size = len(self.seqs)
        s = [0] * size
        while s is not None:
            if len(s) < size:
                optimScore = self.score(s) + (size - len(s)) * self.motifSize
                if optimScore < melhorScore:
                    s = self.bypass(s)
                else:
                    s = self.nextVertex(s)
            else:
                sc = self.score(s)
                if sc > melhorScore:
                    melhorScore = sc
                    melhorMotif = s
                s = self.nextVertex(s)
        return melhorMotif

    # Consensus (heuristic)

    def heuristicConsensus(self):
        mf = MotifFinding(self.motifSize, self.seqs[:2])
        s = mf.exhaustiveSearch()
        for i in range(2, len(self.seqs)):
            s.append(0)
            melhorScore = -1
            melhorPosicao = 0
            for j in range(self.seqSize(i) - self.motifSize + 1):
                s[i] = j
                score_atual = self.score(s)
                if score_atual > melhorScore:
                    melhorScore = score_atual
                    melhorPosicao = j
                s[i] = melhorPosicao
        return s

    # Consensus (heuristic)

    def heuristicStochastic(self):
        from random import randint
        s = [0] * len(self.seqs)
        for i in range(len(self.seqs)):
            s[i] = randint(0, self.seqSize(i) - self.motifSize)

        best_score = self.score(s)
        improve = True
        while improve:
            motif = self.createMotifFromIndexes(s)
            motif.createPWM()
            for i in range(len(self.seqs)):
                s[i] = motif.mostProbableSeq(self.seqs[i])
            scr = self.score(s)
            if scr > best_score:
                best_score = scr
            else:
                improve = False
        return s

    def heuristicStochastic_ex(self):
        from random import randint
        s = [0] * len(self.seqs)
        for i in range(len(self.seqs)):
            s[i] = randint(0, self.seqSize(i) - self.motifSize)

        best_score = self.score_pseudo(s)
        improve = True
        while improve:
            motif = self.createMotifFromIndexes(s)
            motif.createPWM()
            motif.pwm = [[motif.pwm[lin][col] + 0.1 for col in range(len(motif.pwm[0]))] for lin in range(len(motif.pwm))]
            for i in range(len(self.seqs)):
                s[i] = motif.mostProbableSeq(self.seqs[i])
            scr = self.score_pseudo(s)
            if scr > best_score:
                best_score = scr
            else:
                improve = False
        return s

    # Gibbs sampling 

    def gibbs(self, iterations=1000):
        from random import randint
        s = [randint(0, len(self.seqs[i]) - self.motifSize - 1) for i in range(len(self.seqs))]
        best_score = self.score(s)
        bests = list(s)
        for it in range(iterations):
            seq_index = randint(0, len(self.seqs) - 1)
            seq = self.seqs[seq_index]
            s.pop(seq_index)
            removed = self.seqs.pop(seq_index)
            motif = self.createMotifFromIndexes(s)
            motif.createPWM()
            self.seqs.insert(seq_index, removed)
            r = motif.probAllPositions(seq)
            pos = self.roulette(r)
            s.insert(seq_index, pos)
            score = self.score(s)
            if score > best_score:
                best_score = score
                bests = list(s)
        return bests

    def gibbs_ex(self, iterations=1000):
        from random import randint
        s = [randint(0, len(self.seqs[i]) - self.motifSize - 1) for i in range(len(self.seqs))]
        best_score = self.score_pseudo(s)
        bests = list(s)
        for it in range(iterations):
            seq_index = randint(0, len(self.seqs) - 1)
            seq = self.seqs[seq_index]
            s.pop(seq_index)
            removed = self.seqs.pop(seq_index)
            motif = self.createMotifFromIndexes(s)
            motif.createPWM()
            motif.pwm = [[motif.pwm[lin][col] + 0.1 for col in range(len(motif.pwm[0]))] for lin in range(len(motif.pwm))]
            self.seqs.insert(seq_index, removed)  # vai voltar a adicionar a seq removida ?? lista de seqs na posi????o seq_index
            r = motif.probAllPositions(seq)
            pos = self.roulette(r)
            s.insert(seq_index, pos)
            score = self.score_pseudo(s)
            if score > best_score:
                best_score = score
                bests = list(s)
        return bests

    def roulette(self, f):
        from random import random
        tot = 0.0
        for x in f: tot += (0.01 + x)
        val = random() * tot
        acum = 0.0
        ind = 0
        while acum < val:
            acum += (f[ind] + 0.01)
            ind += 1
        return ind - 1


# tests
def test1():
    sm = MotifFinding()
    sm.readFile("exemploMotifs.txt", "dna")
    sol = [25, 20, 2, 55, 59]
    sa = sm.score(sol)
    print(sm.score_pseudo(sol))
    print(sa)
    scm = sm.scoreMult(sol)
    print(scm)


def test2():
    print("Test exhaustive:")
    seq1 = MySeq("ATAGAGCTGA", "dna")
    seq2 = MySeq("ACGTAGATGA", "dna")
    seq3 = MySeq("AAGATAGGGG", "dna")
    mf = MotifFinding(3, [seq1, seq2, seq3])
    sol = mf.exhaustiveSearch()
    print("Solution", sol)
    print("Score: ", mf.score(sol))
    print("Consensus:", mf.createMotifFromIndexes(sol).consensus())

    print("Branch and Bound:")
    sol2 = mf.branchAndBound()
    print("Solution: ", sol2)
    print("Score:", mf.score(sol2))
    print("Consensus:", mf.createMotifFromIndexes(sol2).consensus())

    print("Heuristic consensus: ")
    sol1 = mf.heuristicConsensus()
    print("Solution: ", sol1)
    print("Score:", mf.score(sol1))


def test3():
    mf = MotifFinding()
    mf.readFile("exemploMotifs.txt", "dna")
    print("Branch and Bound:")
    sol = mf.branchAndBound()
    print("Solution: ", sol)
    print("Score:", mf.score(sol))
    print("Consensus:", mf.createMotifFromIndexes(sol).consensus())


def test4():
    mf = MotifFinding()
    mf.readFile("exemploMotifs.txt", "dna")
    print("Heuristic stochastic")
    sol = mf.heuristicStochastic()
    print("Solution: ", sol)
    print("Score:", mf.score(sol))
    print(mf.score_pseudo(sol))
    print("Score mult:", mf.scoreMult(sol))
    print("Consensus:", mf.createMotifFromIndexes(sol).consensus())
    sol2 = mf.gibbs(1000)
    print("Score:", mf.score(sol2))
    print("Score mult:", mf.scoreMult(sol2))


test1()
print()
test2()
print()
test3()
print()
test4()
