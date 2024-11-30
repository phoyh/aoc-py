import itertools as it
from api import file

def get_numbers():
	return file.lines('2020/09', int)

def get_start(numbers):
	return next(
		num
		for idx, num in enumerate(numbers)
		if idx >= 25 and all(
			x + y != num
			for x, y in it.combinations(numbers[idx-25:idx], 2)
		)
	)

def get_contiguous_sequence(numbers):
	start = get_start(numbers)
	cum_numbers = [0] + list(it.accumulate(numbers))
	return next(
		numbers[i:j+1]
		for i, j in it.combinations(range(len(numbers)), 2)
		if cum_numbers[j+1] - cum_numbers[i] == start
	)

def test_first():
	assert 15353384 == get_start(get_numbers())

def test_second():
	seq = get_contiguous_sequence(get_numbers())
	assert 2466556 == min(seq) + max(seq)
