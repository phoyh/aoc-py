import collections

import api.file
import api.graph

def all_paths(start, end, neighbors, is_path_prefix_legit):
	todo = [(start, [])]
	result = []
	while len(todo) > 0:
		node, prefix = todo.pop()
		newPath = prefix + [node]
		if is_path_prefix_legit(newPath):
			if node == end:
				result.append(newPath)
			else:
				for n in neighbors(node):
					todo.append((n, newPath))
	return result

def getEdges():
	e = collections.defaultdict(lambda : [])
	for l in api.file.lines('2021/12_mini'):
		a, b = l.split('-')
		e[a] += [b]
		e[b] += [a]
	return e

def isValid(path: list[str], isOneSmallTwiceOk) -> bool:
	c = collections.Counter(n for n in path if n.islower())
	if c['start'] > 1:
		return False
	if len([v for v in c.values() if v > 2]) > 0:
		return False
	return isOneSmallTwiceOk >= len([v for v in c.values() if v == 2])

def getPathes(isOneSmallTwiceOk):
	e = getEdges()
	return all_paths(str('start'), 'end', lambda n: e[n],
		lambda p: isValid(p, isOneSmallTwiceOk))

def test_first():
	assert 226 == len(getPathes(False))

def test_second():
	assert 3509 == len(getPathes(True))