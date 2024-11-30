from api import file

def solve(factor, times):
	vals = [int(l) * factor for l in file.lines('2022/20_ex')]
	val_idx_by_pos = list(range(len(vals)))
	for _ in range(times):
		for val_idx, val in enumerate(vals):
			pos = val_idx_by_pos.index(val_idx)
			val_idx_by_pos.pop(pos)
			val_idx_by_pos.insert((pos + val) % (len(vals) - 1), val_idx)
	zero_pos = val_idx_by_pos.index(vals.index(0))
	return sum(
		vals[val_idx_by_pos[(zero_pos + offset) % len(vals)]]
		for offset in range(1000, 4000, 1000)
	)

def test_first():
	assert 3 == solve(1, 1)

def test_second():
	assert 1623178306 == solve(811589153, 10)
