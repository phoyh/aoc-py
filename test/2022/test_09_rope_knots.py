import numpy as np
import api.file

def tail_positions_numpy(knot_num):
	tails = [np.array([0, 0]) for _ in range(knot_num)]
	ts = set()
	for l in api.file.lines('2022/09'):
		op, val = l.split()
		delta = [[1, 0], [-1, 0], [0, -1], [0, 1]]['RLUD'.index(op)]
		for _ in range(int(val)):
			tails[0] += delta
			for front, rear in zip(tails, tails[1:]):
				if max(np.abs(front - rear)) >= 2:
					rear += np.sign(front - rear)
			ts.add(tuple(tails[-1]))
	return ts

def tail_positions_complex(knot_num):
	tails = [0] * knot_num
	ts = set()
	for l in api.file.lines('2022/09'):
		op, val = l.split()
		bearing = [1, -1, -1j, 1j]['RLUD'.index(op)]
		for _ in range(int(val)):
			tails[0] += bearing
			for i in range(1, len(tails)):
				diff = tails[i-1] - tails[i]
				ds = np.sign(diff.real) + 1j * np.sign(diff.imag)
				tails[i] += ds if abs(diff) >= 2 else 0
			ts.add(tails[-1])
	return ts

def test_first():
	assert 6011 == len(tail_positions_numpy(2))
	assert 6011 == len(tail_positions_complex(2))

def test_second():
	assert 2419 == len(tail_positions_numpy(10))
	assert 2419 == len(tail_positions_complex(10))
	