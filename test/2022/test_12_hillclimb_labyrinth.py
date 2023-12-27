from api import PDict, file, graph

def get_predecessors(altitude, c):
	return {p for p in c.neighbors(within=altitude.keys()) if altitude[c] <= altitude[p] + 1}

def get_paths_altitudes_start():
	lines = file.lines('2022/12')
	g = PDict.from_lines(lines)
	start = g.by_value('S').pop()
	end = g.by_value('E').pop()
	g[start] = 'a'
	g[end] = 'z'
	altitude_by_point = {p: ord(h) for p, h in g.items()}
	path_from = graph.dijkstra_to_all(
		end,
		lambda c: get_predecessors(altitude_by_point, c),
		lambda *_: 1
	)
	return (path_from, altitude_by_point, start)

def test_first():
	path_from, _, start = get_paths_altitudes_start()
	cost, _ = path_from[start]
	assert 370 == cost

def test_second():
	path_from, altitude_by_point, _ = get_paths_altitudes_start()
	a_paths = [path_from[a] for a, h in altitude_by_point.items() if h == ord('a')]
	assert 363 == min(cost for cost, _ in a_paths)