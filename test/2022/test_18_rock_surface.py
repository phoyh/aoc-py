from api import file, parse

def get_cubes():
	return {tuple(e) for e in file.lines('2022/18', parse.ints)}

def get_dirs(x, y, z):
	return [
		(x + dx, y + dy, z + dz)
		for dx, dy, dz in [(-1, 0, 0), (1, 0, 0), (0, -1, 0), (0, 1, 0), (0, 0, -1), (0, 0, 1)]
	]

def test_first():
	cubes = get_cubes()
	assert 4302 == sum(
		dc not in cubes
		for c in cubes
		for dc in get_dirs(*c)
	)

def test_second():
	cubes = get_cubes()
	xs, ys, zs = zip(*cubes)
	candidates = {
		(x, y, z)
		for x in range(min(xs) - 1, max(xs) + 2)
		for y in range(min(ys) - 1, max(ys) + 2)
		for z in range(min(zs) - 1, max(zs) + 2)
	}
	todo = {(min(xs) - 1, min(ys) - 1, min(zs) - 1)}
	surface = 0
	while todo:
		c = todo.pop()
		if c in candidates:
			candidates.remove(c)
			for dc in get_dirs(*c):
				if dc in cubes:
					surface += 1
				elif dc in candidates:
					todo.add(dc)
	assert 2492 == surface
