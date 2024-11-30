from api import PDict

def getInput():
	with open('input/2021/13.txt', 'r') as f:
		return [l.strip() for l in f.readlines()]

def getFoldOp(line):
	FOLD_ALONG = "fold along "
	if line[0:len(FOLD_ALONG)] == FOLD_ALONG:
		dim, offsetStr = line[len(FOLD_ALONG):].split('=')
		return (0 if dim == 'x' else 1, int(offsetStr))

def getStartingPoints(inp):
	return {
		tuple([int(c) for c in line.split(',')])
		for line in inp
		if not getFoldOp(line) and len(line) > 0
	}

def getFoldOps(inp):
	return [fo for fo in map(getFoldOp, inp) if fo]

def foldPoint(p, foldOp):
	pl = list(p)
	compIndex, foldOffset = foldOp
	pl[compIndex] = min(pl[compIndex], foldOffset - (pl[compIndex] - foldOffset))
	return tuple(pl)

def getPointsAfterFoldOpsEx(points, foldOps):
	for fo in foldOps:
		points = {foldPoint(p, fo) for p in points}
	return points

def test_first():
	inp = getInput()
	startingPoints = getStartingPoints(inp)
	foldOps = getFoldOps(inp)
	points = getPointsAfterFoldOpsEx(startingPoints, [foldOps[0]])
	assert 621 == len(points)

def test_second():
	inp = getInput()
	startingPoints = getStartingPoints(inp)
	foldOps = getFoldOps(inp)
	points = getPointsAfterFoldOpsEx(startingPoints, foldOps)
	assert PDict({p: '*' for p in points}).to_str_2d() == (
		'*  * *  * *  *   **  **   **    ** ****\n'
		'*  * * *  *  *    * *  * *  *    *    *\n'
		'**** **   *  *    * *    *  *    *   * \n'
		'*  * * *  *  *    * * ** ****    *  *  \n'
		'*  * * *  *  * *  * *  * *  * *  * *   \n'
		'*  * *  *  **   **   *** *  *  **  ****'
	)
