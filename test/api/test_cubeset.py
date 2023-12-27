from api import Cube, CubeSet, P

c1 = Cube([(2, 5), (3, 4), (-8, -6)])
c2 = Cube([(4, 6), (1, 3), (-7, -7)])
c3 = Cube([(4, 6), (1, 3), (-3, -2)])
cs12_w_intersection = CubeSet([c1, c2])
cs13_wo_intersection = CubeSet([c1, c3])

### OVERRIDES

def test_str():
	assert str(cs13_wo_intersection) == \
		'[ 2 -> 5 | 3 -> 4 | -8 -> -6 ] , ' + \
		'[ 4 -> 6 | 1 -> 3 | -3 -> -2 ]'

def test_normalize():
	assert str(cs12_w_intersection) == \
		'[ 2 -> 5 | 3 -> 4 | -8 -> -6 ] , ' + \
		'[ 4 -> 5 | 1 -> 2 | -7 ] , ' + \
		'[ 6 | 1 -> 3 | -7 ]'

def test_len():
	assert len(c1) + len(c3) == len(cs13_wo_intersection)
	assert len(c1) + len(c2) - len(c1 & c2) == len(cs12_w_intersection)

def test_intersect():
	assert str(cs12_w_intersection & cs13_wo_intersection) == str(CubeSet([c1]))

def test_intersect_cube():
	assert str(cs12_w_intersection & c2) == str(CubeSet([c2]))

def test_subtract():
	cs = cs13_wo_intersection - cs12_w_intersection
	assert len(cs) == len(c3) - len((c1 | c2) & c3)

def test_subtract_cube():
	cs = cs12_w_intersection - c2
	assert len(cs) == len(c1) - len(c1 & c2)

def test_subtract_from_cube():
	cs = c2 - cs13_wo_intersection
	assert len(cs) == len(c2) - len(cs13_wo_intersection & c2)

def test_union():
	cs1 = CubeSet([Cube([(1, 1), (4, 4)]), Cube([(2, 2), (5, 5)])])
	cs2 = CubeSet([Cube([(1, 1), (5, 5)]), Cube([(2, 2), (4, 4)])])
	cs3 = cs1 | cs2
	assert str(cs3) == '[ 1 -> 2 | 4 -> 5 ]'

def test_union_cube():
	assert str(cs12_w_intersection | c2) == str(cs12_w_intersection)

### OTHER FUNCTIONALITY

def test_contains_point():
	assert (3, 4, -6) in cs12_w_intersection
	assert P((3, 2, -6)) not in cs12_w_intersection

def test_contains_cube():
	assert c1 in cs12_w_intersection
	assert c2 not in cs13_wo_intersection

def test_contains_cubeset():
	assert CubeSet([c1]) in cs12_w_intersection
	assert CubeSet([c2]) not in cs13_wo_intersection

def test_split():
	left, right = cs12_w_intersection.split(1, 3)
	assert ' , '.join([
		'[ 2 -> 5 | 3 | -8 -> -6 ]',
		'[ 4 -> 5 | 1 -> 2 | -7 ]',
		'[ 6 | 1 -> 3 | -7 ]'
	]) == str(left)
	assert '[ 2 -> 5 | 4 | -8 -> -6 ]' == str(right)
	left, right = cs12_w_intersection.split(2, 3)
	assert not right
	assert left == cs12_w_intersection

def test_to_points():
	assert {
		P((4, 1, -7)), P((5, 1, -7)), P((6, 1, -7)),
		P((4, 2, -7)), P((5, 2, -7)), P((6, 2, -7)),
		P((6, 3, -7))
	} == (c2 - c1).to_points()
