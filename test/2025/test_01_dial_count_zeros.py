from api import file

def get_orders():
	return [
		(1 if l[0] == 'R' else -1, int(l[1:]))
		for l in file.lines('2025/01')
	]

def test_first():
	c = 50
	result = 0
	for d, n in get_orders():
		c = (c + d * n) % 100
		result += c == 0
	assert 1043 == result

def test_second():
	c = 50
	result = 0
	for d, n in get_orders():
		newc_wo_mod = c + d * n
		result += abs(newc_wo_mod) // 100 + (newc_wo_mod <= 0 < c)
		c = newc_wo_mod % 100
	assert 5963 == result
