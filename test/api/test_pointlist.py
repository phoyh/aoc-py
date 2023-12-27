from api import P, PList

def test_surface():
	pl = PList([P((2, 3)), P((12, 3)), P((12, 13)), P((2, 13)), P((2, 3))])
	assert 121 == pl.surface_2d()
	assert 121 == PList(pl[::-1]).surface_2d()
	pl = PList([P((-2, 0)), P((2, 4)), P((2, -4)), P((-2, 0))])
	assert 1 + 2 + 3 + 4 + 5 + 4 + 3 + 2 + 1 == pl.surface_2d()
