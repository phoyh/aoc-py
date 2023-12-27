import api.file
from collections import Counter

def getStartPairCount(polymer):
	return Counter(map(str.__add__, polymer, polymer[1:]))

def doIteration(pairCount, operations):
	for (l, r), v in pairCount.copy().items():
		pairCount[l + r] -= v
		newe = operations[l + r]
		pairCount[l + newe] += v
		pairCount[newe + r] += v

def getScoreForPairCount(pairCount, lastElement):
	elemCount = Counter({lastElement: 1})
	for (l, _), v in pairCount.items():
		elemCount[l] += v
	vals = elemCount.values()
	return max(vals) - min(vals)

def calcScore(numberOfIterations):
	input = api.file.lines('2021/14')
	pairCount = getStartPairCount(input[0])
	ops = dict(l.split(' -> ') for l in input[2:])
	for _ in range(numberOfIterations):
		doIteration(pairCount, ops)
	return getScoreForPairCount(pairCount, input[0][-1])

def test_first():
	assert 2584 == calcScore(10)

def test_second():
	assert 3816397135460 == calcScore(40)