import itertools as it
import api.file

def getAlgoWithStartDots(suffix):
	input = api.file.lines('2021/20' + suffix)
	return (input[0], {
		(x, y): v == '#'
		for y, l in enumerate(input[2:])
		for x, v in enumerate(list(l))
	})

def getRange(dots):
	xs, ys = zip(*dots.keys())
	return it.product(range(min(xs) - 1, max(xs) + 2), range(min(ys) - 1, max(ys) + 2))

def getDot(dots, default, x, y):
	return default if (x, y) not in dots else dots[(x, y)]
	
def getAlgoOutput(algo, dots, default, x, y):
	algoIn = [
		'1' if getDot(dots, default, x + dx, y + dy) else '0'
		for dy in range(-1, 2) for dx in range(-1, 2)
	]
	offset = int(''.join(algoIn), 2)
	return algo[offset] == '#'

def dotsAfterEnhanceTimes(algoWithDots, times):
	algo, dots = algoWithDots
	for i in range(times):
		default = i % 2 == 1 and algo[0] == '#'
		dots = {
			(x, y): getAlgoOutput(algo, dots, default, x, y)
			for x, y in getRange(dots)
		}
	return len([k for k, v in dots.items() if v])

def test_first():
	assert 5400 == dotsAfterEnhanceTimes(getAlgoWithStartDots(''), 2)

def test_second_mini():
	assert 3351 == dotsAfterEnhanceTimes(getAlgoWithStartDots('_mini'), 50)