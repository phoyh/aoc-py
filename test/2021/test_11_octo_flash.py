import itertools as it
from api import PDict, file

def getMatrix():
	return PDict.from_lines(file.lines('2021/11'), int)

def doIteration(m):
	for c in m.keys():
		m[c] += 1
	p = set(m.keys())
	hasFound = True
	while hasFound:
		hasFound = False
		for c in [c for c in p if m[c] > 9]:
			hasFound = True
			p.remove(c)
			for n in c.neighbors(diag=True, within=m):
				m[n] += 1
	for c, v in m.items():
		m[c] = v if v <= 9 else 0

def getNumberOfRecentFlashes(m):
	return len([e for e in m.values() if e == 0])

def getTotalFlashes():
	m = getMatrix()
	totalFlashes = 0
	for _ in range(100):
		doIteration(m)
		totalFlashes += getNumberOfRecentFlashes(m)
	return totalFlashes

def getAllFlashIteration():
	m = getMatrix()
	for i in it.count(1):
		doIteration(m)
		if getNumberOfRecentFlashes(m) == len(m):
			return i

def test_first():
	assert 1652 == getTotalFlashes()

def test_second():
	assert 220 == getAllFlashIteration()