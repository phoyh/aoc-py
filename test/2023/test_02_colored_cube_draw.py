import re
import math
from collections import defaultdict

import api.file

def game_parse(l):
	result = defaultdict(int)
	for num, col in re.findall(r'(\d+) (\w)', l):
		result[col] = max(result[col], int(num))
	return result

def test_first():
	games = api.file.lines('2023/02', game_parse)
	assert 2006 == sum(
		i + 1 for i, g in enumerate(games)
		if g['r'] <= 12 and g['g'] <= 13 and g['b'] <= 14
	)

def test_second():
	games = api.file.lines('2023/02', game_parse)
	assert 84911 == sum(math.prod(g.values()) for g in games)
