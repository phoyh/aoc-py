import api.parse

def test_negative_ints():
	result = api.parse.ints('bla -3, 4=-2--4')
	assert [-3, 4, -2, -4] == result