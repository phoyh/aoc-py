import re
import itertools as it
import api.file

def getStartPositions():
	return tuple(int(re.findall(r'\d+', l)[1]) for l in api.file.lines('2021/21'))

def getDiracWins(stateResults, state):
	if state in stateResults:
		return stateResults[state]
	p1, s1, p2, s2 = state
	w1, w2 = (0, 0)
	for d1, d2, d3 in it.product(range(1, 4), repeat=3):
		newP1 = (p1 + d1 + d2 + d3 - 1) % 10 + 1
		newS1 = s1 + newP1
		if newS1 >= 21:
			w1 += 1
		else:
			newState = (p2, s2, newP1, newS1)
			newW2, newW1 = getDiracWins(stateResults, newState)
			w1 += newW1
			w2 += newW2
	stateResults[state] = (w1, w2)
	return (w1, w2)

def test_first():
	p1, p2 = getStartPositions()
	dice = 0
	s1, s2 = (0, 0)
	while s2 < 1000:
		for _ in range(3):
			p1 += (dice % 100) + 1
			dice += 1
		p1 = (p1 - 1) % 10 + 1
		s1 += p1
		p1, s1, p2, s2 = (p2, s2, p1, s1)
	assert 711480 == dice * s1

def test_second():
	p1, p2 = getStartPositions()
	w1, w2 = getDiracWins({}, (p1, 0, p2, 0))
	assert 265845890886828 == max(w1, w2)
