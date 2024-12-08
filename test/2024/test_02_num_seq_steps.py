import itertools as it
from api import file, parse

def get_nums():
	return file.lines('2024/02', parse.ints)

def is_safe(l):
	steps = {a - b for a, b in it.pairwise(l)}
	return steps <= {1, 2, 3} or steps <= {-1, -2, -3}

def test_first():
	assert 246 == sum(1 for l in get_nums() if is_safe(l))

def test_second():
	assert 318 == sum(
		1 for l in get_nums()
		if any(is_safe(p) for p in it.combinations(l, len(l) - 1))
	)
