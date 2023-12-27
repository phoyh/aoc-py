from collections import defaultdict
from itertools import accumulate
import api.file

def sizeByDir():
	sbd = defaultdict(int)
	currentDir = []
	for l in api.file.lines('2022/07'):
		match l.split():
			case '$', 'cd', '..': currentDir.pop()
			case '$', 'cd', d: currentDir += [d]
			case '$', 'ls': pass
			case 'dir', _: pass
			case sizeStr, _:
				for prefix in accumulate(currentDir):
					sbd[tuple(prefix)] += int(sizeStr)
	return sbd

def test_first():
	assert 1447046 == sum(s for s in sizeByDir().values() if s <= 100_000)

def test_second():
	sbd = sizeByDir()
	needed = sbd[('/',)] - (70_000_000 - 30_000_000)
	assert 578710 == min(s for s in sizeByDir().values() if s >= needed)
