import api.file

def getMasses():
	return [int(l) for l in api.file.lines('2019/01')]

def getFuelReq(v, isRecursive):
	n = v // 3 - 2
	if n <= 0:
		return 0
	return n + (getFuelReq(n, True) if isRecursive else 0)

def test_first():
	assert 3511949 == sum(getFuelReq(m, False) for m in getMasses())

def test_second():
	assert 5265045 == sum(getFuelReq(m, True) for m in getMasses())

