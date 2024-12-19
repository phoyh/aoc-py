import z3
from api import file, parse, z3result

def get_input():
	registers, prg = map(parse.ints, file.segments('2024/17'))
	return registers, prg

def get_output_for_prg(prg, a, b, c):
	pc = 0
	result = []
	while pc < len(prg):
		cmd = prg[pc]
		op_lit = prg[pc+1]
		match op_lit:
			case 4: op_combo = a
			case 5: op_combo = b
			case 6: op_combo = c
			case 7: assert False
			case _: op_combo = op_lit
		match cmd:
			case 0: a = a // (1 << op_combo)
			case 1: b = b ^ op_lit
			case 2: b = op_combo % 8
			case 3:
				if a != 0:
					pc = op_lit - 2
			case 4: b = b ^ c
			case 5: result.append(op_combo % 8)
			case 6: b = a // (1 << op_combo)
			case 7: c = a // (1 << op_combo)
		pc += 2
	return result

def solve_a(prg, target_output_suffix) -> list[int]:
	"""
	assumes 2,4 (a%8) and 0,3 (a//8) and 3,0 (jmp0) in the input
	"""
	if len(target_output_suffix) == 0:
		return [0]
	candidates = solve_a(prg, target_output_suffix[1:])
	return [
		a
		for c in candidates
		for a in range(c * 8, c * 8 + 8)
		if get_output_for_prg(prg, a, 0, 0) == target_output_suffix
	]

def test_first():
	regs, prg = get_input()
	output = get_output_for_prg(prg, *regs)
	assert '6,5,4,7,1,6,0,3,1' == ','.join([str(v) for v in output])

def test_second():
	_, prg = get_input()
	assert 106086382266778 == min(solve_a(prg, prg))

####### z3 SOLVER #######

def find_a_solver(prg):
	lowest = -1
	s = z3.Solver()
	start = z3.BitVec('s', 48)
	a, b, c = start, 0, 0
	for x in prg:
		b = a % 8
		b = b ^ 5
		c = a / (1 << b)
		b = b ^ c
		b = b ^ 6
		a = a / (1 << 3)
		s.add((b % 8) == x)
	s.add(a == 0)
	while True:
		s.push()
		if lowest != -1:
			s.add(start < lowest)
		if s.check() != z3.sat:
			return lowest
		lowest = z3result.get_model_var_value(s.model(), start)
		s.pop()

#def test_second_z3_solver():
def do_not_execute_test_second_z3_solver():
	_, prg = get_input()
	assert 106086382266778 == find_a_solver(prg)

####### z3 OPTIMIZER #######

def find_a_opt(prg):
	opt = z3.Optimize()
	start = z3.BitVec('s', 48)
	a, b, c = start, 0, 0
	for x in prg:
		b = a & 7
		b = b ^ 5
		c = a >> b
		b = b ^ c
		b = b ^ 6
		a = a >> 3
		opt.add((b & 7) == x)
	opt.add(a == 0)
	opt.minimize(start)
	if opt.check() != z3.sat:
		return
	return z3result.get_model_var_value(opt.model(), start)

#def test_second_z3_opt():
def do_not_execute_test_second_z3_opt():
	_, prg = get_input()
	assert 106086382266778 == find_a_opt(prg)
