import numpy as np

def getInput():
	with open('input/2021/09.txt', 'r') as f:
		return [l.strip() for l in f.readlines()]

def getMatrix():
	input = getInput()
	return np.array([list(l) for l in input], int)

def getPadMatrix(matrix):
	return np.pad(matrix, 1, mode='constant', constant_values=9)

def getIsLowest(matrix, padMatrix):
	return (
		(matrix < padMatrix[2:, 1:-1])
		& (matrix < padMatrix[0:-2, 1:-1])
		& (matrix < padMatrix[1:-1, 2:])
		& (matrix < padMatrix[1:-1, 0:-2])
	)

def getLows(matrix, padMatrix):
	return list(zip(*np.where(getIsLowest(matrix, padMatrix) == True)))

def getBasinSize(lowPoint, padMatrix):
	todos = [lowPoint]
	basin = set()
	while len(todos) > 0:
		if (candidate := todos.pop(0)) not in basin:
			basin.add(candidate)
			y, x = candidate
			for dx in range(-1, 2):
				for dy in range(-1, 2):
					if (dx == 0 or dy == 0) and (dx + dy) != 0 and padMatrix[y + dy + 1, x + dx + 1] < 9:
						todos.append((y + dy, x + dx))
	return len(basin)

def test_first():
	matrix = getMatrix()
	isLowest = getIsLowest(matrix, getPadMatrix(matrix))
	assert 489 == sum(matrix[isLowest] + 1)

def test_second():
	matrix = getMatrix()
	padMatrix = getPadMatrix(matrix)
	lows = getLows(matrix, padMatrix)
	basins = [getBasinSize(l, padMatrix) for l in lows]
	assert 1056330 == np.prod(sorted(basins)[-3:])

