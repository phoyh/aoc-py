from api import P

def test_dist():
	assert 5 == P((3,)).distance((8,))
	assert 5 == P((3, 2)).distance((2, 6))
	assert 4 == P((3, 2)).distance((2, 6), diag=True)

def test_trivial_ops():
	assert (6, 3, 1) == P((2, 6, 2)) + (4, -3, -1)
	assert (-2, 9, 3) == P((2, 6, 2)) - (4, -3, -1)
	assert (3, 6, 9) == P((1, 2, 3)) * 3
	assert (1, 2, 3) == P((2, 4, 6)) // 2
	assert (-2, -6, -2) == -P((2, 6, 2))
	assert (-1, -3, 4) == P((4, -3, -1)).transpose()

def test_to_cube():
	c3 = P((4, 2, 8)).to_cube()
	assert '4 | 2 | 8' == str(c3)

def test_mod():
	assert (1, 1, 0) == P((-2, 9, 3)) % P((3, 4, 1))
