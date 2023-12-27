class Position:
	h = 0
	d = 0
	def result(self):
		return self.h * self.d

class Alg1_Position(Position):
	def forward(self, p):
		self.h += p
	def down(self, p):
		self.d += p
	def up(self, p):
		self.d -= p

class Alg2_Position(Position):
	a = 0
	def forward(self, p):
		self.h += p
		self.d += p * self.a
	def down(self, p):
		self.a += p
	def up(self, p):
		self.a -= p

def get_orders():
	with open('input/2021/02.txt', 'r') as f:
		for l in f.readlines():
			[instr, p] = l.split(' ')
			yield [instr, int(p)]

def execute_orders(pos):
	for o in get_orders():
		match o:
			case ['forward', p]:
				pos.forward(p)
			case ['down', p]:
				pos.down(p)
			case ['up', p]:
				pos.up(p)

def test_first():
	pos = Alg1_Position()
	execute_orders(pos)
	assert 1882980 == pos.result()

def test_second():
	pos = Alg2_Position()
	execute_orders(pos)
	assert 1971232560 == pos.result()
