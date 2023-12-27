import math
import operator as op
import functools as ft
import api.file

def getBits():
	bits = ''
	for h in api.file.lines('2021/16')[0]:
		hx = int('0x' + h, 16)
		bits += ('000' + format(hx, 'b'))[-4:]
	return bits

class Node:
	def __init__(self, version, nodeType):
		self.version = version
		self.type = nodeType
		self.subs = []
		self.value = 0

def nextInt(binStr, startPos, length):
	return (int(binStr[startPos:startPos+length], 2), startPos + length)

def build(bits, demandedNumberOfPackages=math.inf):
	i = 0
	res = []
	while i + 6 < len(bits) and len(res) < demandedNumberOfPackages:
		v, i = nextInt(bits, i, 3)
		t, i = nextInt(bits, i, 3)
		n = Node(v, t)
		if n.type == 4:
			isDone = 1
			while isDone == 1:
				isDone, i = nextInt(bits, i, 1)
				vp, i = nextInt(bits, i, 4)
				n.value = 16 * n.value + vp
		else:
			mode, i = nextInt(bits, i, 1)
			if mode == 0:
				totalLen, i = nextInt(bits, i, 15)
				n.subs, _ = build(bits[i:i+totalLen])
				i += totalLen
			else:
				subNum, i = nextInt(bits, i, 11)
				n.subs, offset = build(bits[i:], subNum)
				i += offset
		res += [n]
	return (res, i)

def getAst():
	asts, _ = build(getBits())
	return asts[0]

def getVersions(ast):
	return [ast.version] + [v for n in ast.subs for v in getVersions(n)]

funs = [op.add, op.mul, min, max, lambda v: v, op.gt, op.lt, op.eq]

def evalAst(ast):
	return ft.reduce(funs[ast.type], map(evalAst, ast.subs) if len(ast.subs) > 0 else [ast.value])

def test_first():
	assert 967 == sum(getVersions(getAst()))

def test_second():
	assert 12883091136209 == evalAst(getAst())