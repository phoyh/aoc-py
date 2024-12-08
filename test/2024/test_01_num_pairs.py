from api import file, parse

def get_input():
	tuple_lines = file.lines('2024/01', parse.ints)
	return tuple(zip(*tuple_lines))

def test_first():
	lefts, rights = get_input()
	assert 1388114 == sum(abs(l - r) for l, r in zip(sorted(lefts), sorted(rights)))

def test_second():
	lefts, rights = get_input()
	assert 23529853 == sum(l * rights.count(l) for l in lefts)
