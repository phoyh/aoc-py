import itertools as it
from api import PDict, file

def get_landscape():
	g = PDict({})
	for l in file.lines('2022/14'):
		coords = [tuple(int(e) for e in p.split(',')) for p in l.split(' -> ')]
		for s, e in it.pairwise(coords):
			g = g.draw_line(s, e, '#')	
	return g

def drop_sand_is_off(landscape, x, y, stop_drop_at_y):
	g = landscape
	is_falling = True
	x_lookup = [0, -1, 1]
	while is_falling and y < stop_drop_at_y:
		lookup = [(x + dx, y + 1) not in g for dx in x_lookup]
		if is_falling := any(lookup):
			x += x_lookup[lookup.index(True)]
			y += 1
	g[(x, y)] = 'o'
	return is_falling

def drop_sands_get_num(landscape, add_horizontal_line_at_max_y_plus=None):
	g = landscape
	max_y = max(y for _, y in g)
	if add_horizontal_line_at_max_y_plus is not None:
		ly = add_horizontal_line_at_max_y_plus + max_y
		for x in range(500 - ly - 1, 500 + ly + 2):
			g[(x, ly)] = '#'
	c = 0
	is_off = False
	while not is_off and (500, 0) not in g:
		is_off = drop_sand_is_off(g, 500, 0, max_y + 2)
		c += 1
	if is_off:
		c -= 1
	return c

def test_first():
	assert 817 == drop_sands_get_num(get_landscape())

def test_second():
	assert 23416 == drop_sands_get_num(get_landscape(), add_horizontal_line_at_max_y_plus=2)
