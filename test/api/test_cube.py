from api import Cube, P

c1 = Cube([(2, 5), (3, 4), (-8, -6)])
c2 = Cube([(4, 6), (1, 3), (-7, -7)])

def test_str():
	assert '2 -> 5 | 3 -> 4 | -8 -> -6' == str(c1)

def test_len():
	assert 4 * 2 * 3 == len(c1)

def test_intersect():
	c3 = c1 & c2
	assert '4 -> 5 | 3 | -7' == str(c3)

def test_intersect_disjoint():
	c3 = Cube([(4, 6), (1, 3), (-4, -2)])
	c4 = c1 & c3
	assert len(c4) == 0

def test_union():
	c3s = c1 | c2
	assert len(c1) + len(c2) - len(c1 & c2) == len(c3s)

def test_move():
	assert c1.move((4, -1, 3)) == Cube([(6, 9), (2, 3), (-5, -3)])

def test_contains_point():
	assert (3, 5, -7) not in c1
	assert P((5, 3, -7)) in c1

def test_contains_cube():
	assert c2 not in c1
	assert Cube([(4, 5), (3, 3), (-7, -6)]) in c1

def test_min():
	assert [2, 3, -8] == c1.min()

def test_quadrants_full():
	c3 = Cube([(0, 9), (21, 25)])
	c3qs = c3.quadrants()
	assert {str(q) for q in c3qs} == {
		'0 -> 4 | 21 -> 23',
		'0 -> 4 | 24 -> 25',
		'5 -> 9 | 21 -> 23',
		'5 -> 9 | 24 -> 25'
	}

def test_quadrants_sub_dimensional():
	c3 = Cube([(0, 9), (21, 21)])
	c3qs = c3.quadrants()
	assert {str(q) for q in c3qs} == {
		'0 -> 4 | 21',
		'5 -> 9 | 21'
	}

def test_to_points():
	assert {P((4, 3, -7)), P((5, 3, -7))} == (c1 & c2).to_points()
