import itertools as it

from api import PDict, file, P, PList

N, S, W, E = P.NSWE()
pipe_openings: dict[str, tuple[P, P]] = {
	'|': (N, S),
	'-': (W, E),
	'L': (N, E),
	'J': (W, N),
	'7': (W, S),
	'F': (S, E),
}
pipe_enclose_left_in_openings_direction: dict[str, set[P]] = {
	'|': {E},
	'-': {N},
	'L': set(),
	'J': set(),
	'7': {N, E},
	'F': {W, N},
}

def is_qualified(area, path, g):
	width, height = g.size_by_dim()
	for x, y in area:
		if all((xr, y) not in path for xr in range(x)):
			return False
		if all((xr, y) not in path for xr in range(x + 1, width)):
			return False
		if all((x, yr) not in path for yr in range(y)):
			return False
		if all((x, yr) not in path for yr in range(y + 1, height)):
			return False
	return True

def flood_fill_by_x(area, path, g):
	width, _ = g.size_by_dim()
	result = set(area)
	for x in range(width):
		ins_y = [ay for ax, ay in area if ax == x]
		ins_y.sort()
		for yf, yt in it.pairwise(ins_y):
			if all((x, yr) not in path for yr in range(yf + 1, yt)):
				for yr in range(yf + 1, yt):
					result.add((x, yr))
	return result

def get_start_pipe(start, g):
	start_openings = {
		n - start
		for n in start.neighbors(within=g) if g[n] in pipe_openings
		for po in pipe_openings[g[n]] if n + po == start
	}
	return next(pk for pk, pv in pipe_openings.items() if set(pv) == start_openings)

def get_all():
	g = PDict.from_lines(file.lines('2023/10'))
	start = next(k for k, v in g.items() if v == 'S')
	my_dir = pipe_openings[get_start_pipe(start, g)][0]
	pos = start + my_dir
	path = PList([start])
	left_in = set()
	right_in = set()
	while pos != start:
		path.append(pos)
		pipe = g[pos]
		openings = pipe_openings[pipe]
		enclose_left = pipe_enclose_left_in_openings_direction[pipe]
		enclose_right = set(P.NSWE()) - enclose_left - set(openings)
		poi, my_dir = next(
			(poi, po) for poi, po in enumerate(openings)
			if po != -my_dir
		)
		if poi == 1:
			enclose_right, enclose_left = enclose_left, enclose_right
		for el in enclose_left:
			left_in.add(pos + el)
		for er in enclose_right:
			right_in.add(pos + er)
		pos += my_dir
	return g, path, left_in - set(path), right_in - set(path)

def test_first():
	_, path, _, _ = get_all()
	assert 6697 == len(path) // 2

def test_second_clockwise():
	g, path, left_in, right_in = get_all()
	valid_in = set()
	if is_qualified(left_in, path, g):
		valid_in = left_in
	if is_qualified(right_in, path, g):
		valid_in = right_in
	assert len(valid_in) > 0
	assert 423 == len(flood_fill_by_x(valid_in, path, g))

def test_second_surface():
	_, path, _, _ = get_all()
	assert 423 == path.surface_2d() - len(path)
