from collections import defaultdict
from api import file, P

def get_start_tiles():
	is_black = defaultdict(bool)
	for line in file.lines('2020/24_ex'):
		idx = 0
		p = P((0, 0))
		while idx < len(line):
			c = line[idx]
			if c in ['n', 's']:
				c += line[idx+1]
				idx += 1
			idx += 1
			p += {
				'e': (2, 0),
				'w': (-2, 0),
				'ne': (1, -1),
				'nw': (-1, -1),
				'se': (1, 1),
				'sw': (-1, 1),
			}[c]
		is_black[p] = not is_black[p]
	return is_black

def get_black_num(is_black):
	return len([k for k, v in is_black.items() if v])

def get_neighbors(p: P):
	return {p + d for d in [(-2, 0), (2, 0), (1, -1), (-1, -1), (1, 1), (-1, 1)]}

def exec_day(is_black):
	result = defaultdict(int)
	newrelevant = set.union(*[get_neighbors(p) for p in is_black.keys()]) | is_black.keys()
	for p in newrelevant:
		black_neigh_num = len([n for n in get_neighbors(p) if is_black[n]])
		result[p] = black_neigh_num in [1, 2] if is_black[p] else black_neigh_num == 2
	return result

def test_first():
	is_black = get_start_tiles()
	assert 10 == get_black_num(is_black)

def test_second():
	is_black = get_start_tiles()
	for _ in range(10):
		is_black = exec_day(is_black)
	assert 37 == get_black_num(is_black)
