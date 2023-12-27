import api.file

def getRounds():
	input = api.file.lines('2022/02')
	return [('ABC'.index(l), 'XYZ'.index(r)) for l, _, r in input]

def getScore(rounds):
	sc = 0
	for l, r in rounds:
		if (l + 1) % 3 == r:
			sc += 6
		if l == r:
			sc += 3
		sc += r + 1
	return sc

def test_first():
	rounds = getRounds()
	assert 13682 == getScore(rounds)

def test_second():
	rounds = [(l, (l + r - 1) % 3) for l, r in getRounds()]
	assert 12881 == getScore(rounds)
