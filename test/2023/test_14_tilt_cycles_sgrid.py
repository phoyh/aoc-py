from api import file, P, PDict, PSet

def get_input(filename):
	g = PDict.from_lines(file.lines(filename))
	hashes = g.by_value('#')
	rocks = g.by_value('O')
	g = g.draw_set(rocks, '.')
	return g, hashes, rocks

def turn_right(ps: PSet, height) -> PSet:
	return PSet({P((height - 1 - y, x)) for x, y in ps})

def fall_north(hashes: PSet, rocks: PSet):
	for x in rocks.range_by_dim()[0]:
		fall_dest = 0
		for y in range(0, rocks.max_by_dim()[1] + 1):
			p = P((x, y))
			if p in hashes:
				fall_dest = y + 1
			elif p in rocks:
				rocks.remove(p)
				rocks.add(P((x, fall_dest)))
				fall_dest += 1
	return rocks

def get_load(height, rocks):
	return sum(height - y for _, y in rocks)

def test_first():
	g, hashes, rocks = get_input('2023/14')
	rocks = fall_north(hashes, rocks)
	_, height = g.size_by_dim()
	assert 108857 == get_load(height, rocks)

def test_second():
	g, hashes, rocks = get_input('2023/14_mini')
	todo = 1_000_000_000
	width, height = g.size_by_dim()
	lookup = {}
	while todo > 0:
		for _ in range(4):
			rocks = fall_north(hashes, rocks)
			hashes = turn_right(hashes, height)
			rocks = turn_right(rocks, height)
			width, height = height, width
		status = frozenset(rocks)
		if status in lookup:
			prior = lookup[status]
			diff = prior - todo
			todo = todo % diff
		else:
			lookup[status] = todo
		todo -= 1
	assert 64 == get_load(height, rocks)
