import numpy as np
import api.file

def get_matrix():
	return np.array([list(l) for l in api.file.lines('2022/08')], np.int32)

def matrix_range(m):
	return np.ndindex(m.shape)

def sees_border(m, x, y):
	dirs = [m[:y, x], m[y+1:, x], m[y, :x], m[y, x+1:]]
	return any(all(h < m[y, x] for h in d) for d in dirs)

def visible_num(hs, my_h):
	return next((i + 1 for i, h in enumerate(hs) if h >= my_h), len(hs))

def get_vision(m, x, y):
	dirs = [list(reversed(m[:y, x])), m[y+1:, x], list(reversed(m[y, :x])), m[y, x+1:]]
	dir_ranges = [visible_num(d, m[y, x]) for d in dirs]
	return int(np.product(dir_ranges))

def test_first():
	m = get_matrix()
	border_seers = [(x, y) for x, y in matrix_range(m) if sees_border(m, x, y)]
	assert 1713 == len(border_seers)

def test_second():
	m = get_matrix()
	vision = [get_vision(m, x, y) for x, y in matrix_range(m)]
	assert 268464 == max(vision)