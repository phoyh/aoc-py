from api import file, PDict, P
N, S, W, E = NSWE = P.NSWE()
SE = S + E
NE = N + E
O = P.O()

def get_grid(suffix = ''):
	return PDict.from_lines(file.lines(f'2024/04{suffix}'))

def get_word(g, p, d, length):
	return ''.join(g[p + d * i] for i in range(length))

def get_xmas_count(g):
	return sum(
		get_word(g, p, d, 4) == 'XMAS'
		for p in g
		for d in O.neighbors(diag=True)
	)

def get_mas_in_cross_count(g):
	return sum(
		{get_word(g, p + S + S, NE, 3), get_word(g, p, SE, 3)} <= {'MAS', 'SAM'}
		for p in g
	)

def test_first():
	assert 18 == get_xmas_count(get_grid('_ex'))

def test_second():
	assert 9 == get_mas_in_cross_count(get_grid('_ex'))