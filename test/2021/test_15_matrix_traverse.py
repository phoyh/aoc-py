from api import file, graph, P

def getBottomRight(m):
	return (max(x for x, _ in m.keys()), max(y for _, y in m.keys()))

def getMinCost(m):
	cost, _ = graph.dijkstra(
		P.O(),
		getBottomRight(m),
		lambda p: p.neighbors(within=m),
		lambda _, p: m[p]
	)
	return cost

def normalizeValue(v):
	while v > 9:
		v -= 9
	return v

def test_first():
	assert 583 == getMinCost({
		(x, y): int(c)
		for y, l in enumerate(file.lines('2021/15'))
		for x, c in enumerate(list(l))
	})

def test_second():
	inp = file.lines('2021/15_mini')
	assert 315 == getMinCost({
		(rx * len(inp[0]) + x, ry * len(inp) + y): normalizeValue(int(c) + rx + ry)
		for y, l in enumerate(inp)
		for x, c in enumerate(list(l))
		for rx in range(5)
		for ry in range(5)
	})
