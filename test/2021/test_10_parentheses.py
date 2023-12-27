import functools as ft

def getInput():
	with open('../aocPython/input/2021/10.txt', 'r') as f:
		return [l.strip() for l in f.readlines()]

pars = {'(': ')', '[': ']', '{': '}', '<': '>'}
parErrorScores = {')': 3, ']': 57, '}': 1197, '>': 25137}
parCompletionScores = {')': 1, ']': 2, '}': 3, '>': 4}

def getErrorOrCompletion(line):
	stack = []
	for c in list(line):
		if c in pars.keys():
			stack.append(pars[c])
		else:
			if c != stack.pop():
				return (c, [])
	return (None, reversed(stack))

def getErrorScore(line):
	e, _ = getErrorOrCompletion(line)
	return parErrorScores[e] if e else 0

def getCompletionScore(line):
	_, comp = getErrorOrCompletion(line)
	return ft.reduce(lambda sum, c: sum * 5 + parCompletionScores[c], comp, 0)

def test_first():
	assert 288291 == sum(map(getErrorScore, getInput()))

def test_second():
	cs = [getCompletionScore(l) for l in getInput() if getErrorScore(l) == 0]
	assert 820045242 == sorted(cs)[len(cs) // 2]
