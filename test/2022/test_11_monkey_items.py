import math
from collections import deque
import api.file
import api.parse

class Monkey:
	def __init__(self, items, op, operand, mod, follow_up_indexes):
		self.items = deque(items)
		self.op = op
		self.operand = operand
		self.mod = mod
		self.follow_up_indexes = follow_up_indexes
		self.follow_up_monkeys = []
		self.inspections = 0
		self.multiple = 0

	def finalize(self, monkeys):
		self.follow_up_monkeys = [monkeys[i] for i in self.follow_up_indexes]
		self.multiple = math.lcm(*[m.mod for m in monkeys])

	def exec_round(self, with_worry_decrease):
		while len(self.items) > 0:
			it = self.items.pop()
			match self.op:
				case '+': it += self.operand
				case '*': it *= self.operand
				case '^': it **= self.operand
			if with_worry_decrease:
				it //= 3
			it %= self.multiple
			self.follow_up_monkeys[it % self.mod == 0].items.append(it)
			self.inspections += 1

def monkeys_at_start():
	res = []
	for mi, s in enumerate(api.file.segments('2022/11')):
		assert mi == api.parse.ints(s[0])[0]
		items = api.parse.ints(s[1])
		*_, op, val_str = s[2].split()
		if op == '*' and val_str == 'old':
			op, val_str = '^', '2'
		mod = api.parse.ints(s[3])[0]
		fu_true = api.parse.ints(s[4])[0]
		fu_false = api.parse.ints(s[5])[0]
		res += [Monkey(items, op, int(val_str), mod, (fu_false, fu_true))]
	for m in res:
		m.finalize(res)
	return res

def exec_rounds(monkeys, round_num, with_worry_decrease):
	for _ in range(round_num):
		for m in monkeys:
			m.exec_round(with_worry_decrease)

def monkey_business(monkeys):
	return math.prod(sorted([m.inspections for m in monkeys])[-2:])

def test_first():
	monkeys = monkeys_at_start()
	exec_rounds(monkeys, 20, True)
	assert 99840 == monkey_business(monkeys)

def test_second():
	monkeys = monkeys_at_start()
	exec_rounds(monkeys, 10000, False)
	assert 20683044837 == monkey_business(monkeys)