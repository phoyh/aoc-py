import api.file

def getLines():
	return api.file.lines('2022/03')

def getValue(letter):
	o = ord(letter)
	return o - ord('a') + 1 if letter.islower() else o - ord('A') + 27

def getIntersectionValue(parts):
	return getValue(set.intersection(*map(set, parts)).pop())

def getCompartments(line):
	mi = len(line) // 2
	return [line[:mi], line[mi:]]

def getGroups(lines):
	return [lines[i : i + 3] for i in range(0, len(lines), 3)]

def test_first():
	packVals = [getIntersectionValue(getCompartments(l)) for l in getLines()]
	assert 7795 == sum(packVals)

def test_second():
	groupVals = [getIntersectionValue(g) for g in getGroups(getLines())]
	assert 2703 == sum(groupVals)