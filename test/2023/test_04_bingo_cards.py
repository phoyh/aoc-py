import api.file
import api.parse

def get_card(line):
	return [side.split() for side in line.split(':')[1].split('|')]

def get_hits():
	return [
		len(set(l) & set(r))
		for l, r in api.file.lines('2023/04', get_card)
	]

def test_first():
	assert 21105 == sum(2 ** (h - 1) for h in get_hits() if h > 0)

def test_second():
	hits = get_hits()
	copy_num = [1] * len(hits)
	for idx, h in enumerate(hits):
		for copy_idx in range(idx + 1, min(idx + 1 + h, len(hits))):
			copy_num[copy_idx] += copy_num[idx]
	assert 5329815 == sum(copy_num)
