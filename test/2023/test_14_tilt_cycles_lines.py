from api import PDict, file

def get_input(filename):
	return [''.join(nl) for nl in zip(*file.lines(filename))]

def fall(lines):
	return [
		'#'.join(''.join(sorted(p, reverse=True)) for p in l.split('#'))
		for l in lines
	]

def turn_right(lines):
	g = PDict.from_lines(lines)
	width, _ = g.size_by_dim()
	# do as turn left because lines transposed
	tg = PDict({(y, width - 1 - x): v for (x, y), v in g.items()})
	return tg.to_lines_2d()

def get_load(lines):
	return sum(
		len(l) - i
		for l in lines
		for i, c in enumerate(l) if c == 'O'
	)

def test_first():
	assert 108857 == get_load(fall(get_input('2023/14')))

def test_second():
	lines = get_input('2023/14_mini')
	todo = 1_000_000_000
	lookup = {}
	while todo > 0:
		for _ in range(4):
			lines = fall(lines)
			lines = turn_right(lines)
		key = tuple(lines)
		if key in lookup:
			diff = lookup[key] - todo
			todo = todo % diff
		else:
			lookup[key] = todo
		todo -= 1
	assert 64 == get_load(lines)