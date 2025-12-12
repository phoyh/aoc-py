import itertools as it
import math

from api import file, P

def get_points_and_sorted_pairs():
	points = file.lines('2025/08_ex', lambda line: P(tuple(map(int, line.split(',')))))
	dists = sorted([
		(a.distance_euclidean(b), a, b)
		for a, b in it.combinations(points, 2)
	])
	pairs = [(a, b) for _, a, b in dists]
	return points, pairs

def connect_points(max_pairs: int | None = None, max_circuits: int | None = None) \
		-> tuple[list[int], tuple[P, P] | None]:
	points, pairs = get_points_and_sorted_pairs()
	circuit_by_p = {p: i for i, p in enumerate(points)}
	circuit_count = len(points)
	if not max_pairs:
		max_pairs = len(pairs)
	for a, b in pairs[:max_pairs]:
		if circuit_by_p[a] != circuit_by_p[b]:
			prior = circuit_by_p[b]
			for p, c in circuit_by_p.items():
				if c == prior:
					circuit_by_p[p] = circuit_by_p[a]
			circuit_count -= 1
			if max_circuits is not None and circuit_count <= max_circuits:
				return [len(points)], (a, b)
	circuit_sizes_desc = sorted([
		sum(ci == i for ci in circuit_by_p.values())
		for i in range(len(points))
	], reverse=True)
	return circuit_sizes_desc, None

def test_first():
	circuit_sizes_desc, _ = connect_points(max_pairs=10)
	assert 40 == math.prod(circuit_sizes_desc[:3])

def test_second():
	_, last_pair = connect_points(max_circuits=1)
	assert last_pair is not None
	a, b = last_pair
	assert 25272 == a[0] * b[0]
