import re

import api.file

def get_seat(descr: str):
	#descr = descr.translate(str.maketrans('FLBR', '0011'))
	#descr = ''.join(['0' if e in 'FL' else '1' for e in descr])
	descr = re.sub(r'F|L', '0', descr)
	descr = re.sub(r'\D', '1', descr)
	return int(descr, 2)

def get_seat_ids():
	return [get_seat(d) for d in api.file.lines('2020/05')]

def test_first():
	assert 892 == max(get_seat_ids())

def test_second():
	ids = set(get_seat_ids())
	assert 625 == (set(range(min(ids), max(ids))) - ids).pop()
