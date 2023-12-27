import itertools as it

import api.graph

def getStartStacks(isToBeAdded):
	return ('CDDC', 'DBCB', 'AABA', 'BCAD') if isToBeAdded else ('CC', 'DB', 'AA', 'BD')

costByLetter = dict(zip('ABCD', [1, 10, 100, 1000]))
targetStackIndexByLetter = dict(zip('ABCD', range(4)))
offsetByStack = [2, 4, 6, 8]

def hasOnly(s, c):
	return s == c * len(s)

def moveOutTryOffset(stackIndex, toOffset, status):
	if toOffset in offsetByStack:
		return set()
	maxStackSize, corridor, stacks = status
	stack = stacks[stackIndex]
	letter = stack[-1]
	stacksOnceRemoved = tuple(list(stacks)[:stackIndex] + [stack[:-1]] + list(stacks)[stackIndex+1:])
	newStatus = (maxStackSize, corridor[:toOffset] + letter + corridor[toOffset+1:], stacksOnceRemoved)
	return {(newStatus)}

def moveOut(stackIndex, status):
	_, corridor, _ = status
	stackOffset = offsetByStack[stackIndex]
	candidateOffsets = []
	toOffset = stackOffset - 1
	while toOffset >= 0 and corridor[toOffset] == ' ':
		candidateOffsets += [toOffset]
		toOffset -= 1
	toOffset = stackOffset + 1
	while toOffset < len(corridor) and corridor[toOffset] == ' ':
		candidateOffsets += [toOffset]
		toOffset += 1
	res = set()
	for co in candidateOffsets:
		res |= moveOutTryOffset(stackIndex, co, status)
	return res

def moveIn(offset, status):
	maxStackSize, corridor, stacks = status
	letter = corridor[offset]
	if letter == ' ':
		return set()
	targetStackIndex = targetStackIndexByLetter[letter]
	targetStack = stacks[targetStackIndex]
	targetStackOffset = offsetByStack[targetStackIndex]
	if not hasOnly(targetStack, letter):
		return set()
	if offset < targetStackOffset:
		path = corridor[offset+1:targetStackOffset+1]
	else:
		path = corridor[targetStackOffset:offset]
	if hasOnly(path, ' '):
		stacksOnceAdded = tuple(
			list(stacks)[:targetStackIndex]
			+ [targetStack + letter]
			+ list(stacks)[targetStackIndex+1:]
		)
		newStatus = (maxStackSize, corridor[:offset] + ' ' + corridor[offset+1:], stacksOnceAdded)
		return {newStatus}
	return set()

def getNeighbors(status):
	_, corridor, stacks = status
	res = set()
	for si, s in enumerate(stacks):
		if len(s) > 0 and (not hasOnly(s, s[-1]) or targetStackIndexByLetter[s[-1]] != si):
			res |= moveOut(si, status)
	for ci in range(len(corridor)):
		res |= moveIn(ci, status)
	return res

def getEdgeCost(fromStatus, toStatus):
	maxStackSize, fromCorridor, fromStacks = fromStatus
	_, toCorridor, toStacks = toStatus
	cDiffIdx = 0
	while fromCorridor[cDiffIdx] == toCorridor[cDiffIdx]:
		cDiffIdx += 1
	letter = (fromCorridor[cDiffIdx] + toCorridor[cDiffIdx]).strip()
	sDiffIdx = 0
	while fromStacks[sDiffIdx] == toStacks[sDiffIdx]:
		sDiffIdx += 1
	movesHor = abs(offsetByStack[sDiffIdx] - cDiffIdx)
	movesVer = maxStackSize - min(len(fromStacks[sDiffIdx]), len(toStacks[sDiffIdx]))
	return (movesHor + movesVer) * costByLetter[letter]

def getLeastEffort(stacks):
	stackSize = len(stacks[0])
	startState = (stackSize, ' ' * 11, stacks)
	endState = (stackSize, ' ' * 11, tuple('ABCD'[i] * stackSize for i in range(len(stacks))))
	cost, _ = api.graph.dijkstra(startState, endState, getNeighbors, getEdgeCost)
	return cost

def test_first():
	assert 13558 == getLeastEffort(getStartStacks(False))

def test_second():
	assert 56982 == getLeastEffort(getStartStacks(True))
