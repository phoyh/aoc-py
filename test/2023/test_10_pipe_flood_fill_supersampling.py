from api import PDict, file, P

N, S, W, E = NSWE = P.NSWE()
O = P.O()

pipes = {
	'-': {E, W},
	'|': {N, S},
	'L': {N, E},
	'F': {S, E},
	'7': {S, W},
	'J': {N, W},
}

def get_all():
	g = PDict.from_lines(file.lines('2023/10_mini'))
	g3 = PDict({
		n + c * 3: '#' if (v in pipes and n in pipes[v] | {(0, 0)}) else '.'
		for n in O.neighbors(diag = True) | {O}
		for c, v in g.items()
	})
	g3 = g3.pad('.', diag=True)
	start = next(p for p, v in g.items() if v == 'S')
	start3 = start * 3
	g3[start3] = '#'
	for n in NSWE:
		if g3[start3 + n * 2] == '#':
			g3[start3 + n] = '#'
	path3 = set()
	pos3 = start3
	while pos3:
		path3.add(pos3)
		pos3 = next((n for n in pos3.neighbors() - path3 if g3[n] == '#'), None)
	return g3, path3

def test_first():
	_, path3 = get_all()
	assert 80 == len(path3) // 3 // 2

def test_second():
	g3, path3 = get_all()
	g3 = g3.draw_set(path3, '#').draw_set(g3.keys() - path3, '.')
	g3 = g3.flood('~', (-2, -2))
	g = {(x3 // 3, y3 // 3): v for (x3, y3), v in g3.items() if x3 % 3 == 0 and y3 % 3 == 0}
	assert 10 == sum(v == '.' for v in g.values())
