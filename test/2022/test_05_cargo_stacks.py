import api.file
import api.parse

def getStartStacks(stacksStr):
	stacks = [[] for _ in range(10)]
	for i in range(len(stacksStr) - 2, -1, -1):
		l = stacksStr[i]
		for j, letter in enumerate(l[1::4]):
			if letter != ' ':
				stacks[j+1] += [letter]
	return stacks

def getStacksOrders():
	startStacksStr, ordersStr = api.file.segments('2022/05')
	return (getStartStacks(startStacksStr), [api.parse.ints(os) for os in ordersStr])

def moveCratesOneByOne(stacks, orders):
	for num, fi, ti in orders:
		for _ in range(num):
			stacks[ti] += [stacks[fi].pop()]

def moveCratesAllAtOnce(stacks, orders):
	for num, fi, ti in orders:
		stacks[ti] += stacks[fi][-num:]
		stacks[fi] = stacks[fi][:-num]

def getTop(stacks):
	return ''.join([s[-1] for s in stacks[1:]])

def test_first():
	stacks, orders = getStacksOrders()
	moveCratesOneByOne(stacks, orders)
	assert 'SBPQRSCDF' == getTop(stacks)

def test_second():
	stacks, orders = getStacksOrders()
	moveCratesAllAtOnce(stacks, orders)
	assert 'RGLVRCQSB' == getTop(stacks)