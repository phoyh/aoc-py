from api import PDict, graph, P

landscape = '''
Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi'''
landscape_lines = [str(l) for l in landscape.splitlines()[1:]]

def get_successors(altitude, p):
	return {s for s in p.neighbors(within=altitude.keys()) if altitude[s] <= altitude[p] + 1}

def get_predecessors(altitude, p):
	return {pr for pr in p.neighbors(within=altitude.keys()) if altitude[p] <= altitude[pr] + 1}

def get_altitude_start_end():
	g = PDict.from_lines(landscape_lines)
	start = [p for p, v in g.items() if v == 'S'][0]
	end = [p for p, v in g.items() if v == 'E'][0]
	g[start] = 'a'
	g[end] = 'z'
	altitude = {p: ord(h) for p, h in g.items()}
	return (altitude, start, end)

def test_dijkstra_all_to_all():
	altitude, start, end = get_altitude_start_end()
	paths = graph.dijkstra_all_to_all(
		list(altitude.keys()),
		lambda p: get_successors(altitude, p),
		lambda *_: 1
	)
	cost, path = paths[(start, end)]
	assert 31 == cost
	assert path is not None
	assert 31 == len(path[1:])
	assert start == path[0]
	assert end == path[-1]

def test_dijkstra_to_all():
	altitude, end, start = get_altitude_start_end()
	paths = graph.dijkstra_to_all(
		start,
		lambda c: get_predecessors(altitude, c),
		lambda *_: 1
	)
	cost, path = paths[end]
	assert 31 == cost
	assert path is not None
	assert 31 == len(path[1:])
	assert end == path[-1]
	assert start == path[0]
	# must pass waypoint (2, 2)
	cost, path = paths[P((2, 2))]
	assert 27 == cost

def test_dijkstra_to_all_w_max_costs():
	altitude, _, start = get_altitude_start_end()
	paths = graph.dijkstra_to_all(
		start,
		lambda c: get_predecessors(altitude, c),
		lambda *_: 1,
		max_costs=5
	)
	assert 6 == len(paths)

def test_dijkstra_to_all_with_path_prefix_filter():
	altitude, end, start = get_altitude_start_end()
	paths = graph.dijkstra_to_all(
		start,
		lambda c: get_predecessors(altitude, c),
		is_path_prefix_legit = lambda p: len({(1, 2), (2, 2)} & set(p)) == 0
	)
	cost, path = paths[end]
	assert 33 == cost
	assert (1, 2) not in path
	assert (2, 2) not in path
