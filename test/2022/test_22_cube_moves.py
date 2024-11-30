import re
from api import file, P, PDict
N, S, W, E = NSWE = P.NSWE()

def get_input():
	segs = file.segments('2022/22_ex')
	grid = PDict.from_lines(segs[0])
	walkables = grid.by_values('.')
	walls =  grid.by_values('#')
	commands = re.split(r'(L|R)', segs[1][0])
	return walkables, walls, commands

def get_start_pos(walkables):
	return P((min(x for (x, y) in walkables if y == 0), 0))

def move(walkables, walls, pos, face, steps):
	for _ in range(steps):
		if pos + face in walls:
			return pos
		if pos + face in walkables:
			pos += face
		else:
			np = pos
			while np in walkables | walls:
				np -= face
			np += face
			if np in walls:
				return pos
			pos = np
	return pos

def turn(f, is_right):
	nf = [W, E, S, N][NSWE.index(f)]
	if is_right:
		nf = -nf
	return nf

def execute(walkables, walls, commands, pos, face):
	for c in commands:
		match c:
			case 'R':
				face = turn(face, True)
			case 'L':
				face = turn(face, False)
			case _:
				pos = move(walkables, walls, pos, face, int(c))
	return pos, face

def calc_pwd(pos, face):
	pos_x, pos_y = pos
	return 1000 * (pos_y + 1) + 4 * (pos_x + 1) + [E, S, W, N].index(face)

def test_first():
	walkables, walls, commands = get_input()
	pos, face = execute(walkables, walls, commands, get_start_pos(walkables), E)
	assert 6032 == calc_pwd(pos, face)
