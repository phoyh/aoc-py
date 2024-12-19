from api import file, PDict, PSet

def get_regions():
	g = PDict.from_lines(file.lines('2024/12_ex'))
	result = []
	seen = PSet()
	for p in g:
		if p not in seen:
			region = g.region(p)
			seen |= region
			result.append(region)
	return result

def get_price(region):
	return len(region) * len(region.edges())

def get_price_long_fence(region: PSet):
	long_edge_count = 0
	edges = region.edges()
	for inner, outer in edges:
		orth_dir = (inner - outer).rotate_right()
		# only consider left-most edge as representative of the long edge
		if (inner + orth_dir, outer + orth_dir) not in edges:
			long_edge_count += 1
	return long_edge_count * len(region)

def test_first():
	assert 1930 == sum(get_price(r) for r in get_regions())

def test_second():
	assert 1206 == sum(get_price_long_fence(r) for r in get_regions())
