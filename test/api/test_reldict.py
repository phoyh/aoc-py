from api import RDict

def test_edge_contraction_undirected_no_reflexive():
	exp = RDict({
		'A': {'B': 3},
		'B': {'A': 2}
	})
	act = exp.contract_forwarders(lambda a, b, _: a + b)
	assert act == exp

def test_edge_contraction_directed():
	succ = RDict({
		'A': {'B': 3, 'C': 4},
		'B': {'Z': 1, 'Y': 2},
		'C': {'D': 5},
		'D': {'E': 1},
		'Y': {'D': 10}
	})
	exp = RDict({
		'A': {'B': 3, 'D': 9},
		'B': {'Z': 1, 'D': 12},
		'D': {'E': 1},
		'E': {},
		'Z': {}
	})
	act = succ.contract_forwarders(lambda a, b, _: a + b)
	assert act == exp

def test_edge_contraction_undirected():
	succ = RDict({
		'A': {'B': 3, 'C': 4, 'O': 0},
		'B': {'Z': 1, 'Y': 2},
		'C': {'D': 5},
		'D': {'E': 1},
		'Y': {'D': 10}
	})
	succ = succ | succ.reverse()
	exp = RDict({
		'A': {'B': 3, 'D': 9, 'O': 0},
		'B': {'A': 3, 'Z': 1, 'D': 12},
		'D': {'A': 9, 'B': 12, 'E': 1},
		'E': {'D': 1},
		'O': {'A': 0},
		'Z': {'B': 1}
	})
	act = succ.contract_forwarders(lambda a, b, _: a + b)
	assert act == exp

def test_edge_contraction_directed_w_merge():
	succ = RDict({
		'A': {'B': 3, 'Z': 2, 'C': 4, 'O': 0},
		'B': {'Z': 1},
		'C': {'D': 5}
	})
	exp = RDict({
		'A': {'D': 9, 'O': 0, 'Z': 2},
		'D': {},
		'O': {},
		'Z': {}
	})
	act = succ.contract_forwarders(lambda a, b, prior: min(prior, a + b) if prior else a + b)
	assert act == exp
	exp['A']['Z'] = 4
	act = succ.contract_forwarders(lambda a, b, prior: max(prior, a + b) if prior else a + b)
	assert act == exp
