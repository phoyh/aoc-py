import math

from api import PDict, file

def get_tree_num(dx, dy):
	g = PDict.from_lines(file.lines('2020/03'))
	width, height = g.size_by_dim()
	x = dx
	y = dy
	t = 0
	while y < height:
		if g[(x % width, y)] == '#':
			t += 1
		x += dx
		y += dy
	return t

def test_first():
	assert 284 == get_tree_num(3, 1)

def test_second():
	trees_per_direction = [get_tree_num(dx, dy) for dx, dy in [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]]
	assert 3510149120 == math.prod(trees_per_direction)