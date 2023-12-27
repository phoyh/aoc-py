import math
import ast
import api.file

class Node:
	def __init__(self, parent=None, value=0, left=None, right=None):
		self.parent = parent
		self.value = value
		self.left = left
		self.right = right

	@staticmethod
	def build(t, parent=None):
		if isinstance(t, int):
			return Node(parent, t)
		n = Node(parent)
		n.left = Node.build(t[0], n)
		n.right = Node.build(t[1], n)
		return n
	
	@staticmethod
	def buildFromStr(s):
		return Node.build(ast.literal_eval(s))

	def str(self):
		if not self.left:
			return str(self.value)
		return '[' + self.left.str() + ',' + self.right.str() + ']'

	def clone(self):
		return Node.buildFromStr(self.str())

	def magnitude(self):
		if not self.left:
			return self.value
		return 3 * self.left.magnitude() + 2 * self.right.magnitude()
	
	def depth(self):
		if not self.parent:
			return 0
		return 1 + self.parent.depth()
	
	def valueSubnodes(self):
		if not self.left:
			return [self]
		return self.left.valueSubnodes() + self.right.valueSubnodes()
	
	def add(self, n2):
		res = Node(left = self, right = n2)
		for n in [self, n2]:
			n.parent = res
		return res

	def splitLeftmost(self):
		if self.left:
			return self.left.splitLeftmost() or self.right.splitLeftmost()
		if self.value < 10:
			return False
		self.left = Node(self, self.value // 2)
		self.right = Node(self, math.ceil(self.value / 2))
		self.value = 0
		return True

	def explodeLeftmost(self):
		vn = self.valueSubnodes()
		todos = [(i, l, r, l.parent) for i, (l, r) in enumerate(zip(vn, vn[1:]))
			if l.depth() > 4 and l.parent.right == r]
		if len(todos) == 0:
			return False
		i, l, r, p = todos[0]
		p.left = p.right = None
		if i > 0:
			vn[i-1].value += l.value
		if i + 2 < len(vn):
			vn[i+2].value += r.value
		return True

	def addReduce(self, n2):
		res = self.add(n2)
		hasChanged = True
		while hasChanged:
			hasChanged = res.explodeLeftmost()
			if not hasChanged:
				hasChanged = res.splitLeftmost()
		return res

def buildAllLines():
	lines = api.file.lines('2021/18')
	return [Node.buildFromStr(l) for l in lines]

def addAllLines():
	lineNodes = buildAllLines()
	nodes = lineNodes[0]
	for nextNodes in lineNodes[1:]:
		nodes = nodes.addReduce(nextNodes)
	return nodes

def getAllPairsAddReduce():
	nl = buildAllLines()
	return [x.clone().addReduce(y.clone()) for x in nl for y in nl if x != y]

def test_magnitude():
	n = Node.buildFromStr('[[[[6,6],[7,6]],[[7,7],[7,0]]],[[[7,7],[7,7]],[[7,8],[9,9]]]]')
	assert 4140 == n.magnitude()

def test_magnitude2():
	n = Node.buildFromStr('[[[[7,8],[6,6]],[[6,0],[7,7]]],[[[7,8],[8,8]],[[7,9],[0,6]]]]')
	assert 3993 == n.magnitude()

def test_cloneStr():
	s = '[[[[7,8],[6,6]],[[6,0],[7,7]]],[[[7,8],[8,8]],[[7,9],[0,6]]]]'
	assert s == Node.buildFromStr(s).clone().str()

def test_addition():
	n1 = Node.buildFromStr('[[[[4,3],4],4],[7,[[8,4],9]]]')
	n2 = Node.buildFromStr('[1,1]')
	assert '[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]' == n1.add(n2).str()

def test_split():
	n = Node.buildFromStr('[[[[0,7],4],[15,[0,13]]],[1,1]]')
	n.splitLeftmost()
	assert '[[[[0,7],4],[[7,8],[0,13]]],[1,1]]' == n.str()

def test_explodeLeft():
	n = Node.buildFromStr('[[[[[9,8],1],2],3],4]')
	n.explodeLeftmost()
	assert '[[[[0,9],2],3],4]' == n.str()

def test_explodeMid():
	n = Node.buildFromStr('[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]')
	n.explodeLeftmost()
	assert '[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]' == n.str()

def test_explodeMid2():
	n = Node.buildFromStr('[[[[0,7],4],[7,[[8,4],9]]],[1,1]]')
	n.explodeLeftmost()
	assert '[[[[0,7],4],[15,[0,13]]],[1,1]]' == n.str()

def test_explodeRight():
	n = Node.buildFromStr('[7,[6,[5,[4,[3,2]]]]]')
	n.explodeLeftmost()
	assert '[7,[6,[5,[7,0]]]]' == n.str()

def test_addReduce():
	n1 = Node.buildFromStr('[[[[4,3],4],4],[7,[[8,4],9]]]')
	n2 = Node.buildFromStr('[1,1]')
	assert '[[[[0,7],4],[[7,8],[6,0]]],[8,1]]' == n1.addReduce(n2).str()

def test_addReduce2():
	n1 = Node.buildFromStr('[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]')
	n2 = Node.buildFromStr('[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]')
	assert '[[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]]' == n1.addReduce(n2).str()

def test_addReduce3():
	n1 = Node.buildFromStr('[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]')
	n2 = Node.buildFromStr('[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]')
	assert '[[[[7,8],[6,6]],[[6,0],[7,7]]],[[[7,8],[8,8]],[[7,9],[0,6]]]]' == n1.addReduce(n2).str()

def test_first():
	assert 4469 == addAllLines().magnitude()

def test_second():
	assert 4770 == max(n.magnitude() for n in getAllPairsAddReduce())
