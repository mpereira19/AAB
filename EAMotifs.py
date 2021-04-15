from EvolAlgorithm import EvolAlgorithm
from Popul import PopulInt, PopulReal
from MotifFinding import MotifFinding
from MyMotifs import MyMotifs


def createMatZeros(nl, nc):
    res = []
    for _ in range(0, nl):
        res.append([0]*nc)
    return res


def printMat(mat):
    for i in range(0, len(mat)):
        for j in range(len(mat[i])):
            print(f"{mat[i][j]:.3f}", end=' ')
        print()


class EAMotifsInt (EvolAlgorithm):
    def __init__(self, popsize, numits, noffspring, filename):
        self.motifs = MotifFinding()
        self.motifs.readFile(filename, "dna")
        indsize = len(self.motifs)
        EvolAlgorithm.__init__(self, popsize, numits, noffspring, indsize)

    def initPopul(self, indsize):
        maxvalue = self.motifs.seqSize(0) - self.motifs.motifSize
        self.popul = PopulInt(self.popsize, indsize, maxvalue, [])

    def evaluate(self, indivs):
        for i in range(len(indivs)):
            ind = indivs[i]
            sol = ind.getGenes()
            fit = self.motifs.score(sol)
            ind.setFitness(fit)


class EAMotifsReal (EvolAlgorithm):
    def __init__(self, popsize, numits, noffspring, filename):
        self.motifs = MotifFinding()
        self.motifs.readFile(filename, 'dna')
        indsize = self.motifs.motifSize * len(self.motifs.alphabet)
        EvolAlgorithm.__init__(self, popsize, numits, noffspring, indsize)

    def initPopul(self, indsize):
        maxvalue = self.motifs.seqSize(0) - self.motifs.motifSize
        self.popul = PopulReal(self.popsize, indsize, ub=maxvalue, indivs=[])

    def vec_to_pwm(self, v):
        pwm = createMatZeros(len(self.motifs.alphabet), self.motifs.motifSize)
        for i in range(0, len(v), len(self.motifs.alphabet)):
            col_idx = int(i / len(self.motifs.alphabet))
            col = v[i:i + len(self.motifs.alphabet)]
            soma = sum(col)
            for j in range(len(self.motifs.alphabet)):
                pwm[i][col_idx] = col[j] / soma
            return pwm

    def evaluate(self, indivs):
        for i in range(len(indivs)):
            ind = indivs[i]
            sol = ind.getGenes()
            pwm = self.vec_to_pwm(sol)
            s = []
            my_motif = MyMotifs(pwm, self.motifs.alphabet)
            for seq in self.motifs.seqs:
                p = my_motif.mostProbableSeq(seq)
                s.append(p)
            fit = self.motifs.scoreMult(sol, pwm)
            ind.setFitness(fit)


def test1():
    ea = EAMotifsInt(100, 1000, 50, "exemploMotifs.txt")
    ea.run()
    ea.printBestSolution()


def test2():
    ea = EAMotifsReal(100, 2000, 50, "exemploMotifs.txt")
    ea.run() # O bug que dá deve-se ao facto de ao upper bound (ub) ser atribuído o valor [].
    # Como este valor não é um número inteiro o randint dá erro!
    ea.printBestSolution()


test1()
test2()
