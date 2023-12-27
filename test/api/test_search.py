import api.search

def test_binary():
	assert 7 == api.search.binary(0, 20, lambda n: 7 - n)
	assert 0 == api.search.binary(0, 20, lambda n: 0 - n)
	assert 20 == api.search.binary(0, 20, lambda n: 20 - n)
	assert api.search.binary(0, 20, lambda n: 34 - n) is None
	assert api.search.binary(0, 20, lambda n: -1 - n) is None

def test_sign_change():
	assert 4 == api.search.sign_change(0, 10, lambda n: 2 * n - 8)
	assert -2 == api.search.sign_change(-10, 10, lambda n: -n - 2.5)