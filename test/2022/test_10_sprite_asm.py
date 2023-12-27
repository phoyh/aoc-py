import api.file

def x_by_cycle():
	x = 1
	res = []
	for l in api.file.lines('2022/10'):
		res += [x]
		if l != 'noop':
			res += [x]
			x += int(l.split()[1])
	return res

def sprite(cycle, x):
	return '#' if abs(x - cycle % 40) <= 1 else '.'

def test_first():
	xc = x_by_cycle()
	assert 13220 == sum(xc[cp1 - 1] * cp1 for cp1 in [20, 60, 100, 140, 180, 220])

def test_second():
	sc = [sprite(c, x) for c, x in enumerate(x_by_cycle())]
	assert ''.join(sc) == \
		'###..#..#..##..#..#.#..#.###..####.#..#.' + \
		'#..#.#..#.#..#.#.#..#..#.#..#.#....#.#..' + \
		'#..#.#..#.#..#.##...####.###..###..##...' + \
		'###..#..#.####.#.#..#..#.#..#.#....#.#..' + \
		'#.#..#..#.#..#.#.#..#..#.#..#.#....#.#..' + \
		'#..#..##..#..#.#..#.#..#.###..####.#..#.'