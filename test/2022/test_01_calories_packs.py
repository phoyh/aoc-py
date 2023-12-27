import api.file

def getSortedElvesCalSum():
	elvesCal = api.file.segments('2022/01', int)
	return sorted([sum(ec) for ec in elvesCal])

def test_first():
	elvesCalSum = getSortedElvesCalSum()
	assert 69693 == elvesCalSum[-1]

def test_second():
	elvesCalSum = getSortedElvesCalSum()
	assert 200945 == sum(elvesCalSum[-3:])