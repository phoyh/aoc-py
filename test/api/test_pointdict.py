from collections import Counter
from api import P, PDict, PSet

grid_input_str = str('''.....
.S-7.
.|.|.
.L-J.
.....
''')
g = PDict.from_lines(grid_input_str.split('\n'))

def test_by_values():
	assert {(2, 1), (3, 2), (2, 3), (1, 2)} == g.by_values('|-')

def test_complex_keys():
	cg = g.to_complex_keys_2d()
	assert len(cg) == len(grid_input_str.replace('\n', ''))
	assert cg[2 + 1j] == '-'
	assert cg[1 + 3j] == 'L'
	assert cg[4 + 4j] == '.'

def test_flood():
	fg = g.flood('o', (4, 2))
	assert fg[P((1, 0))] == 'o'
	assert fg[P((1, 1))] == 'S'
	assert fg[P((2, 2))] == '.'
	g_no_s = g.copy()
	g_no_s[P((1, 1))] = '.'
	fg = g_no_s.flood('o', (4, 2), diag=True)
	assert fg[P((1, 1))] == 'o'
	assert fg[P((2, 2))] == 'o'

def test_fringe():
	assert 5 + 3 + 3 + 5 == len(g.fringe())
	assert ['.'] == list(Counter(g.fringe().values()).keys())
	assert (0, 2) in g.fringe()

def test_move():
	mg = g.move((2, 1))
	assert len(mg) == len(g)
	assert mg[P((3, 2))] == 'S'

def test_pad():
	padded_g = g.pad('o', True, 1)
	assert len(g) + 7 + 5 + 7 + 5 == len(padded_g)
	assert padded_g[P((-1, -1))] == 'o'
	assert padded_g[P((5, 5))] == 'o'
	assert padded_g[P((5, 5))] == 'o'
	assert padded_g[P((3, 3))] == 'J'
	assert padded_g[P((4, 2))] == '.'
	padded_g = g.pad('x', False, 2)
	assert padded_g[P((0, -2))] == 'x'
	assert padded_g[P((-1, -1))] == 'x'
	assert padded_g[P((-2, 0))] == 'x'
	assert (-2, -1) not in padded_g

def test_transpose():
	assert g.transpose()[P((1, 3))] == '7'
	assert g.transpose()[P((3, 1))] == 'L'

#################
# IMPORT / EXPORT
#################

def test_from_minmax():
	assert PDict.from_minmax([(-1, 1), (-2, -2)], 'O').keys() \
		== PSet({P((-1, -2)), P((0, -2)), P((1, -2))})

def test_from_size():
	assert PDict.from_size([2, 3], 'O').to_lines_2d() == ['OO'] * 3 
