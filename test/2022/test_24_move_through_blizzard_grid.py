from api import P, PDict, file

def bliz_move(coord, direction, walls):
	result = coord + direction
	while result in walls:
		result += direction
		result = result % walls.size_by_dim()
	return result

def get_missions(walls, move_back_and_forth):
	width, height = walls.size_by_dim()
	start, end = [
		next(P((x, y)) for x in range(width) if (x, y) not in walls)
		for y in (0, height - 1)
	]
	missions = [(start, end)]
	if move_back_and_forth:
		missions += [(end, start)] + missions
	return missions

def solve(move_back_and_forth):
	g = PDict.from_lines(file.lines('2022/24_ex'))
	blizzards = {
		d: g.by_value(d_char)
		for d, d_char in zip(P.NSWE(), '^v<>')
	}
	walls = g.by_value('#')
	movable = g.by_not_value('#')

	step = 0
	for mission_start, mission_end in get_missions(walls, move_back_and_forth):
		candidates = {mission_start}
		while mission_end not in candidates:
			step += 1
			blizzards = {
				d: {
					bliz_move(c, d, walls)
					for c in cs
				}
				for d, cs in blizzards.items()
			}
			candidates = {
				n
				for c in candidates
				for n in c.neighbors(within=movable) | {c}
				if n not in set.union(*blizzards.values())
			}
	return step

def test_first():
	assert 18 == solve(False)

def test_second():
	assert 54 == solve(True)
