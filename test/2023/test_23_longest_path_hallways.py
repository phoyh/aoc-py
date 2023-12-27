from api import file, P, PDict, RDict

def get_grid():
	g = PDict.from_lines(file.lines('2023/23_mini'))
	width, height = g.size_by_dim()
	start = P((1, 0))
	end = P((width - 2, height - 1))
	return g, start, end

def get_adj(g, ignore_slopes):
	walkable = g.by_not_value('#')
	dots = g.by_value('.')
	standable = walkable if ignore_slopes else dots
	adj_out = RDict()
	for p in standable:
		for n in p.neighbors(within=walkable):
			if n in standable:
				adj_out[p][n] = 1
			else:
				dp = n - p
				if dp == P.by_dir(g[n]):
					adj_out[p][n + dp] = 2
	return adj_out

def find_max_len(start, end, adj_out):
	todo = [(start, set(), 0)]
	res = 0
	while todo:
		p, seen, c = todo.pop()
		if p == end:
			res = max(res, c)
		else:
			for n, nc in adj_out[p].items():
				if n not in seen:
					todo.append((n, seen | {p}, c + nc))
	return res

def solve(ignore_slopes):
	g, start, end = get_grid()
	adj_out = get_adj(g, ignore_slopes=ignore_slopes)
	contracted_adj_out = adj_out.contract_forwarders(
		lambda a, b, prior: max(prior, a + b) if prior else a + b
	)
	return find_max_len(start, end, contracted_adj_out)

def test_first():
	assert 94 == solve(ignore_slopes=False)

def test_second():
	assert 154 == solve(ignore_slopes=True)
