from api import PDict, file, P
N, S, W, E = NSWE = P.NSWE()

def get_step_instructions():
	return {
		(t, d): {d}
		for t, ds in [('.', NSWE), ('-', [W, E]), ('|', [S, N])]
		for d in ds
	} | {
		(t, d): set(NSWE) - ds
		for t, ds in [('-', {N, S}), ('|', {W, E})]
		for d in ds
	} | {
		(t, a): {b}
		for t, pair in [('/', {E, N}), ('\\', {E, S})]
		for p in [pair, set(NSWE) - pair]
		for a, b in [p, list(p)[::-1]]
	}

def get_energized(step_instructions, g, start_p, start_direction):
	todo = [(start_p, start_direction)]
	seen = set()
	while todo:
		p, d = td = todo.pop()
		if p in g and td not in seen:
			seen.add(td)
			for newd in step_instructions[(g[p], d)]:
				todo.append((p + newd, newd))
	return len({p for p, _ in seen})

def get_dgrid(filename):
	return PDict.from_lines(file.lines(filename))

def get_starters(g: PDict):
	return {(p, d) for p in g.fringe().keys() for d in NSWE if p - d not in g}

def test_first():
	assert 7728 == get_energized(get_step_instructions(), get_dgrid('2023/16'), P.O(), E)

def test_second():
	g = get_dgrid('2023/16_ex')
	assert 51 == max(get_energized(get_step_instructions(), g, p, d) for p, d in get_starters(g))
