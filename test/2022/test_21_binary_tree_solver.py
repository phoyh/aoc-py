import operator as op
import itertools as it
import z3
from api import file, z3result

def get_str_by_ape(is_ex = False):
	return {
		key: val.strip()
		for key, val in [l.split(':') for l in file.lines('2022/21' + ('_ex' if is_ex else ''))]
	}

def get_val_op_operands_by_ape():
	str_by_ape = get_str_by_ape()
	val_by_ape = {
		key: int(val)
		for key, val in str_by_ape.items()
		if val.isnumeric()
	}
	operands_by_ape = {}
	op_by_ape = {}
	def get_val(ape):
		if ape not in val_by_ape:
			left, opstr, right = str_by_ape[ape].split(' ')
			operands_by_ape[ape] = (left, right)
			op_by_ape[ape] = [op.add, op.sub, op.mul, op.floordiv]['+-*/'.index(opstr)]
			val_by_ape[ape] = op_by_ape[ape](get_val(left), get_val(right))
		return val_by_ape[ape]
	get_val('root')
	return val_by_ape, op_by_ape, operands_by_ape

def test_first():
	val_by_ape, _, _ = get_val_op_operands_by_ape()
	assert 331319379445180 == val_by_ape['root']

def test_second():
	val_by_ape, op_by_ape, operands_by_ape = get_val_op_operands_by_ape()
	humn_chain = []
	cur = 'humn'
	while cur != 'root':
		humn_chain.append(cur)
		cur = next(key for key, (left, right) in operands_by_ape.items() if cur in [left, right])
	humn_chain.append('root')
	op_by_ape['root'] = op.eq
	for prev, ape in it.pairwise(reversed(humn_chain)):
		is_left = operands_by_ape[prev][0] == ape
		other = operands_by_ape[prev][1 if is_left else 0]
		match op_by_ape[prev]:
			case op.eq:
				val_by_ape[ape] = val_by_ape[other]
			case op.add:
				val_by_ape[ape] = val_by_ape[prev] - val_by_ape[other]
			case op.sub:
				if is_left:
					val_by_ape[ape] = val_by_ape[prev] + val_by_ape[other]
				else:
					val_by_ape[ape] = val_by_ape[other] - val_by_ape[prev]
			case op.mul:
				val_by_ape[ape] = val_by_ape[prev] // val_by_ape[other]
			case op.floordiv:
				if is_left:
					val_by_ape[ape] = val_by_ape[prev] * val_by_ape[other]
				else:
					val_by_ape[ape] = val_by_ape[other] // val_by_ape[prev]
	assert 3715799488132 == val_by_ape['humn']

def solve_by_z3(target_var):
	str_by_ape = get_str_by_ape(True)
	solver = z3.Solver()
	z3var_by_ape = {}
	for k in str_by_ape:
		z3var_by_ape[k] = z3.Int(k)
	for k, rest in str_by_ape.items():
		if rest.isnumeric():
			solver.add(z3var_by_ape[k] == int(rest))
		else:
			left, opstr, right = rest.split(' ')
			opfn = [op.add, op.sub, op.mul, op.truediv]['+-*/'.index(opstr)]
			solver.add(z3var_by_ape[k] == opfn(z3var_by_ape[left], z3var_by_ape[right]))
	return z3result.next_int(solver, z3var_by_ape[target_var])

def test_first_z3():
	assert 152 == solve_by_z3('root')
