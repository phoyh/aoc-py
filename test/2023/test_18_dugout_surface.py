from api import file, P, PList

def parse_line(instr: str):
	dp_str, nm_str, _ = instr.split()
	return P.by_dir(dp_str), int(nm_str)

def parse_line_by_color(instr: str):
	_, _, cl_str = instr.split()
	return P.by_dir('RDLU'[int(cl_str[-2])]), int(cl_str[2:-2], 16)

def solve(parser):
	instructions = file.lines('2023/18', parser)
	pos = P((0, 0))
	pl = PList([pos])
	for dp, steps in instructions:
		pos += dp * steps
		pl.append(pos)
	return pl.surface_2d()

def test_first():
	assert 95356 == solve(parse_line)

def test_second():
	assert 92291468914147 == solve(parse_line_by_color)
