import itertools as it
from api import file, PDict

def get_antinodes_double_dist(g, a1, a2):
	return {a1 * 2 - a2} & g.keys()

def get_antinodes_all(g, a1, a2):
	result = set()
	diff = a1 - a2
	p = a2
	while (p := p + diff) in g:
		result.add(p)
	return result

def solve(fn_antinodes):
	g = PDict.from_lines(file.lines('2024/08'))
	freqs = set(g.values()) - {'.'}
	locs = {
		n
		for f in freqs
		for a, b in it.permutations(g.by_value(f), 2)
		for n in fn_antinodes(g, a, b)
	}
	return len(locs)

def test_first():
	assert 256 == solve(get_antinodes_double_dist)

def test_second():
	assert 1005 == solve(get_antinodes_all)
