from collections import Counter
import numpy as np

lines = '''
*   *
** **
* * *
*   *'''.splitlines()[1:]

g = np.array([list(l) for l in lines])

def test_typed_construction():
	num_lines = [['5' if e == '*' else '0' for e in l] for l in lines]
	num_g = np.array(num_lines, np.int32)
	num_g *= num_g
	assert (25, 0, 0, 0, 25) == tuple(num_g[0])

def test_flatten():
	flattened = np.concatenate(g)
	c = Counter(flattened)
	assert {'*': 4 + 1 + 1 + 1 + 4, ' ': 0 + 3 + 3 + 3 + 0} == c # counting one column at a time

def test_cycle_rows():
	# 1 = y-axis
	on_self_and_right_neighbor = (g == '*') & (np.roll(g, -1, 1) == '*')
	s = sum(np.concatenate(on_self_and_right_neighbor))
	assert 1 + 1 + 4 == s # (0, 1) and (1, 2) and all right stars have stars on the right

def test_cycle_columns():
	# 0 = y-axis
	on_self_and_upper_neighbor = (g == '*') & (np.roll(g, 1, 0) == '*')
	s = sum(np.concatenate(on_self_and_upper_neighbor))
	assert 4 + 4 == s # only all left and right stars have stars above

def test_sub_rectangle():
	# [ y interval , x interval ]
	assert '** **' == ''.join(g[1,:]) # second row
	assert ' * ' == ''.join(g[:3,1]) # second column, first 3 rows

def test_iterate_coordinates():
	# index over shape!
	# remember dim-ordering y, x
	set_on_third_line_indexes = [x for y, x in np.ndindex(g.shape) if g[y, x] == '*' and y == 2]
	assert [0, 2, 4] == sorted(set_on_third_line_indexes) # stars on left/mid/right

def test_enumerate():
	# remember dim-ordering y, x
	set_on_third_line_indexes = [x for (y, x), e in np.ndenumerate(g) if e == '*' and y == 2]
	assert [0, 2, 4] == sorted(set_on_third_line_indexes) # stars on left/mid/right

def test_predicate_horizontal_or_vertical():
	# remember dim-ordering y, x
	is_marked = g == '*'
	assert (1, 0, 0, 0, 1) == tuple(is_marked.all(0)) # first/last column full
	assert (0, 0, 0, 0) == tuple(is_marked.all(1)) # no row full
	assert (1, 1, 1, 1) == tuple(is_marked.any(1)) # every row has something