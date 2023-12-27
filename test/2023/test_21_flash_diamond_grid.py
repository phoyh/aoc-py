from api import file, graph, P, PDict

def simulate_steps(g, steps):
	size_p = P(g.size_by_dim())
	starts = g.by_value('S')
	dots = g.by_value('.') | starts
	paths = graph.dijkstra_to_all(
		starts.pop(),
		lambda p: {n for n in p.neighbors() if n % size_p in dots},
		max_costs=steps
	)
	return sum(c % 2 == steps % 2 for c, _ in paths.values())

def test_first():
	g = PDict.from_lines(file.lines('2023/21'))
	result = simulate_steps(g, 64)
	assert 3578 == result

def test_second2():
	g = PDict.from_lines(file.lines('2023/21_mini'))
	width, height = g.size_by_dim()
	assert width == height
	side_len = width
	a, b, c = [
		simulate_steps(g, steps)
		for steps in [side_len * i // 2 for i in range(1, 7, 2)]
	]
	# side multiple only works in the real input if STEP_NUM % SIDE = SIDE / 2
	# (otherwise S not reached in final grids)
	side_multiple = 26501365 // side_len
	# quadratic polynome based on observations f(0)=a, f(1)=b, f(2)=c
	# extrapolate rest
	result = a + side_multiple * (b - a) + side_multiple * (side_multiple - 1) // 2 * (a - 2 * b + c)
	assert 609453550854168 == result
