import api.file
import api.parse

def hasInclusion(x1, x2, y1, y2):
	return x1 <= y1 and x2 >= y2 or x1 >= y1 and x2 <= y2

def hasOverlap(x1, x2, y1, y2):
	return x2 >= y1 and x1 <= y2

def getNum(fn):
	return sum(fn(*api.parse.uints(l)) for l in api.file.lines('2022/04'))

def test_first():
	assert 453 == getNum(hasInclusion)

def test_second():
	assert 919 == getNum(hasOverlap)
