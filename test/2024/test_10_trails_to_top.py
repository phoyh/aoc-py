import functools as ft
from collections import defaultdict
from api import P, PDict, file

def get_grid():
	lines = file.lines('2024/10_ex')
	return PDict.from_lines(lines, int)

def reachable_paths(g, start: P):
	result = []
	todo = [[start]]
	while todo:
		path = todo.pop()
		now = path[-1]
		if g[now] == 9:
			result.append(path)
		else:
			for n in now.neighbors(within=g):
				if g[n] == g[now] + 1:
					todo.append(path + [n])
	return result

def test_first():
	g = get_grid()
	assert 36 == sum(
		len(g.by_value(9) & {
			v for path in reachable_paths(g, p) for v in path
		})
		for p in g.by_value(0)
	)

def test_second():
	g = get_grid()
	assert 81 == sum(
		len(reachable_paths(g, p))
		for p in g.by_value(0)
	)

######### top-down DP #########

def trailheads_to_tops_w_path_count(g):
	@ft.cache
	def tops_by(p: P) -> dict[P, int]:
		if g[p] == 9:
			return {p: 1}
		result = defaultdict(int)
		for nx in p.neighbors(within=g):
			if g[nx] == g[p] + 1:
				for top, path_count in tops_by(nx).items():
					result[top] += path_count
		return result
	return {trailhead: tops_by(trailhead) for trailhead in g.by_value(0)}

def test_first_topdown_dp():
	g = get_grid()
	assert 36 == sum(
		len(tops_by_trailhead)
		for _, tops_by_trailhead in trailheads_to_tops_w_path_count(g).items()
	)

def test_second_topdown_dp():
	g = get_grid()
	assert 81 == sum(
		sum(count for count in tops_by_trailhead.values())
		for _, tops_by_trailhead in trailheads_to_tops_w_path_count(g).items()
	)
