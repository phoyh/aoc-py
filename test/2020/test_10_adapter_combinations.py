import functools as ft
import itertools as it
from collections import Counter
from api import file

def get_adapters():
	result = sorted(file.lines('2020/10', int) + [0])
	result.append(result[-1] + 3)
	return result

@ft.cache
def count_ways(adapters: tuple[int]):
	if len(adapters) == 1:
		return 1
	ways = 0
	idx = 1
	while idx < len(adapters):
		if adapters[idx] - adapters[0] <= 3:
			ways += count_ways(adapters[idx:])
		idx += 1
	return ways

def test_first():
	c = Counter(b - a for a, b in it.pairwise(get_adapters()))
	assert 2112 == c[1] * c[3]

def test_second():
	assert 3022415986688 == count_ways(tuple(get_adapters()))
