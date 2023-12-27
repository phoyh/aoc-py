import re
import api.file

def getTarget():
	input = api.file.lines('2021/17')
	return [int(e) for e in re.findall(r'-?\d+', input[0])]

def shotAndGetHighestYIfTarget(target, vx, vy):
	xMin, xMax, yMin, yMax = target
	x, y = (0, 0)
	bestY = 0
	while y >= yMin and x <= xMax:
		bestY = max(bestY, y)
		if y <= yMax and x >= xMin:
			return bestY
		x += vx
		y += vy
		vx = max(0, vx - 1)
		vy -= 1

def getShotsInTargetWithHighestY(target):
	_, xMax, yMin, _ = target
	shotsWithSomeY = {
		(vx, vy): shotAndGetHighestYIfTarget(target, vx, vy)
		for vx in range(xMax + 1) for vy in range(yMin, -yMin + 1)
	}
	return {k: v for k, v in shotsWithSomeY.items() if v != None}

def test_first():
	assert 3916 == max(getShotsInTargetWithHighestY(getTarget()).values())

def test_second():
	assert 2986 == len(getShotsInTargetWithHighestY(getTarget()))