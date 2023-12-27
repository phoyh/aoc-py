import numpy as np
from api import PDict, file

def steps_dgrid():
	g = PDict.from_lines(file.lines('2021/25_mini'))
	width, height = g.size_by_dim()
	step = 0
	stepg = PDict({})
	while len(g.diff_points(stepg)) > 0:
		step += 1
		stepg = g
		for dx, dy, sc_type in [(1, 0, '>'), (0, 1, 'v')]:
			oldg = g
			g = oldg.copy()
			for (x, y), v in oldg.items():
				n = ((x + dx) % width, (y + dy) % height)
				if v == sc_type and oldg[n] == '.':
					g[n] = v
					g[(x, y)] = '.'
	return step

def steps_numpy():
	g = np.array([list(l) for l in file.lines('2021/25_mini')])
	step = 0
	while True:
		step += 1
		found = False
		for who, dim in [('>', 1), ('v', 0)]:
			allowed_moves = (np.roll(g, -1, dim) == '.') & (g == who)
			g[allowed_moves] = '.'
			g[np.roll(allowed_moves, 1, dim)] = who
			found = found | np.any(allowed_moves) # type: ignore
		if not found:
			return step

def test_first():
	assert 58 == steps_dgrid()
	assert 58 == steps_numpy()