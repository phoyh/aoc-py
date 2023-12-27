import numpy as np

from collections import defaultdict

def get_lines():
	with open('input/2021/05.txt', 'r') as f:
		return [[[int(c) for c in p.split(',')] for p in l.strip().split(' -> ')] for l in f.readlines()]

def is_diag(l):
	(x1, y1), (x2, y2) = l
	return x1 != x2 and y1 != y2

def prune_diags(lines):
	return [l for l in lines if not is_diag(l)]

def get_point_dict(lines):
	result = defaultdict(int)
	for (x1, y1), (x2, y2) in lines:
		dx, dy = np.sign((x2 - x1, y2 - y1))
		p = (x1, y1)
		while p != (x2 + dx, y2 + dy):
			result[p] += 1
			p = (p[0] + dx, p[1] + dy)
	return result

def count_overlaps(lines):
	return len([v for v in get_point_dict(lines).values() if v > 1])

def test_first():
	assert 8622 == count_overlaps(prune_diags(get_lines()))

def test_second():
	assert 22037 == count_overlaps(get_lines())
