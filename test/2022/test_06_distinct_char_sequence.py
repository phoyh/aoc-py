import api.file

def getFirstDistinctSequence(targetSize):
	signal = api.file.lines('2022/06')[0]
	for i in range(targetSize, len(signal)):
		subseq = signal[i-targetSize:i]
		if len(set(subseq)) == targetSize:
			return i

def test_first():
	assert 1987 == getFirstDistinctSequence(4)

def test_second():
	assert 3059 == getFirstDistinctSequence(14)
