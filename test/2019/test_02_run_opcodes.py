import api.file

def getNums():
	input = api.file.lines('2019/02')
	return [int(e) for e in input[0].split(',')]

def getResult(noun, verb):
	n = getNums()
	n[1] = noun
	n[2] = verb
	i = 0
	while n[i] != 99:
		op = lambda a, b: a + b if n[i] == 1 else a * b
		n[n[i + 3]] = op(n[n[i + 1]], n[n[i + 2]])
		i += 4
	return n[0]

def findNounVerb(result):
	for n in range(100):
		for v in range(100):
			if getResult(n, v) == result:
				return (n, v)

def test_first():
	assert 3895705 == getResult(12, 2)

def test_second():
	n, v = findNounVerb(19690720)
	assert 6417 == 100 * n + v