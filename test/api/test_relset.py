from api import RSet

def test_default():
	rel = RSet()
	rel['A'].add(5)
	assert 5 in rel['A']

def test_topologic_order_succ():
	succ_by = RSet({
		1: {5, 4},
		2: {3, 4},
		3: {4, 5},
		4: set(),
		5: {8},
		6: {7}
	})
	o = succ_by.topologic_order()
	os = ''.join(str(e) for e in o)
	assert '0' not in os
	assert os.index('1') == 0
	assert os.index('3') < os.index('5')
	assert os.index('2') < os.index('4')
	assert os.index('6') < os.index('7')
	assert '4' in os
	assert '8' in os

def test_topologic_order_pred():
	pred_by = RSet({
		1: {5, 4},
		2: {3, 4},
		3: {4, 5},
		4: set(),
		5: {8},
		6: {7}
	})
	o = pred_by.topologic_order(is_predecessors_by=True)
	os = ''.join(str(e) for e in o)
	assert '0' not in os
	assert '1' in os[3:] # behind 4, 5, 8
	assert os.index('3') > os.index('5')
	assert os.index('2') > os.index('4')
	assert os.index('6') > os.index('7')
	assert '4' in os
	assert '8' in os
