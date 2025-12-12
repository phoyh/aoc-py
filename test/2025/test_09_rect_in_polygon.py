import itertools as it

from api import file, parse

def points_min_max(points):
	return [(min(d), max(d)) for d in zip(*points)]

def get_max_rect_area(must_be_within_polygon):
	points = [parse.ints(l) for l in file.lines('2025/09_ex')]
	result = 0
	for canidate_pair in it.combinations(points, 2):
		(x_min, x_max), (y_min, y_max) = points_min_max(canidate_pair)
		size = (1 + x_max - x_min) * (1 + y_max - y_min)
		if size > result and (not must_be_within_polygon or all(
			lx_max <= x_min or lx_min >= x_max or ly_max <= y_min or ly_min >= y_max
			for line in it.pairwise(points + [points[0]])
			for (lx_min, lx_max), (ly_min, ly_max) in [points_min_max(line)]
		)):
			result = size
	return result

def test_first():
	assert 50 == get_max_rect_area(False)

def test_second():
	assert 24 == get_max_rect_area(True)
