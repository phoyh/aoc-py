from api import PDict, file, graph, P
N, S, W, E = NSWE = P.NSWE()

def get_grid():
	return PDict.from_lines(file.lines('2023/17_ex'), int)

def get_neighbors(v: tuple[P, P, int], g, min_streak, max_streak):
	p, dp, streak = v
	np = p + dp
	result = set()
	if np in g:
		if min_streak <= streak:
			for ndp in set(NSWE) - {dp, -dp}:
				result.add((np, ndp, 1))
		if streak < max_streak:
			result.add((np, dp, streak + 1))
	return result

def solve(min_streak, max_streak):
	g = get_grid()
	width, height = g.size_by_dim()
	cost, _ = graph.dijkstra(
		{(P.O(), d, 1) for d in [E, S]},
		lambda v: v[0] == (width - 1, height - 1),
		lambda n: get_neighbors(n, g, min_streak, max_streak),
		lambda _, v2: g[v2[0]]
	)
	return cost

def test_first():
	assert 102 == solve(0, 3)

def test_second():
	assert 94 == solve(4, 10)