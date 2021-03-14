# -*- coding: utf-8 -*-

class BWT:
    
	def __init__(self, seq = "", buildsufarray = False):
		self.bwt = self.build_bwt1(seq, buildsufarray) 

	def set_bwt(self, bw):
		self.bwt = bw

	def build_bwt(self, text, buildsufarray = False):
		ls = []
		for l in range(len(text)):
			ls.append(text[l:]+text[:l])
		srtd = sorted(ls)
		res = []
		for i in range(len(srtd)):
			res.append(srtd[i][-1])
		if buildsufarray:
			self.sa = []
			for i in range(len(ls)):
				stpos = ls[i].index("$")
				self.sa.append(len(text)-stpos-1)
		return res

	def build_bwt1(self, text, buildsufarray = False):
		ls = sorted([text[l:] + text[:l] for l in range(len(text))])
		res = [ls[i][-1] for i in range(len(ls))]
		if buildsufarray: self.sa = [len(text)-ls[i].index("$")-1 for i in range(len(ls))]
		return res
    
	def inverse_bwt(self):
		firstcol = self.get_first_col()
		res = ""
		c = "$" 
		occ = 1
		for i in range(len(self.bwt)):
			pos = find_ith_occ(self.bwt, c, occ)
			c = firstcol[pos]
			occ = firstcol[:pos].count(c) + 1
			res += c
		return res
 
	def get_first_col (self):
		return sorted(self.bwt)
        
	def last_to_first(self):
		res = []
		firstcol = self.get_first_col()
		for i in range(len(firstcol)):
			c = self.bwt[i]
			occ = self.bwt[:i].count(c) + 1
			pos = find_ith_occ(firstcol, c, occ)
			res.append(pos)
		return res

	def bw_matching(self, patt):
		lf = self.last_to_first()
		res = []
		top = 0
		bottom = len(self.bwt)-1
		flag = True
		while flag and top <= bottom:
			if patt != "":
				symbol = patt[-1]
				patt = patt[:-1]
				lmat = self.bwt[top:(bottom+1)]
				if symbol in lmat:
					topIndex = lmat.index(symbol) + top
					bottomIndex = bottom - lmat[::-1].index(symbol)
					top = lf[topIndex]
					bottom = lf[bottomIndex]
				else: flag = False
			else: 
				for i in range(top, bottom+1): res.append(i)
				flag = False            
		return res        
 
	def bw_matching_pos(self, patt):
		res = []
		matches = self.bw_matching(patt)
		for match in matches:
			res.append(self.sa[match])
		res.sort()
		return res
	
	def bw_matching_pos1(self, patt):
		return sorted([self.sa[match] for match in self.bw_matching(patt)])
 
# auxiliary
 
def find_ith_occ(l, elem, index):
	count = 0
	for i in range(len(l)):
		if l[i] == elem:
			count += 1
		if count == index:
			return i
			break
	return -1 

      
def test():
	seq = "TAGACAGAGA$"
	bw = BWT(seq)
	print (bw.bwt)
	print (bw.last_to_first())
	print (bw.bw_matching("AGA"))


def test2():
    bw = BWT("")
    bw.set_bwt("ACG$GTAAAAC")
    print (bw.inverse_bwt())

def test3():
    seq = "TAGACAGAGA$"
    bw = BWT(seq, True)
    print("Suffix array:", bw.sa)
    print(bw.bw_matching_pos("AGA"))
#    print(bw.bw_matching_pos1("AGA"))

test()
test2()
test3()

