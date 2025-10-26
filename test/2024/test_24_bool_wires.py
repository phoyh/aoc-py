import functools as ft
import operator as op
from api import file

RULE_BY_OUT = dict[str, tuple[str, list[str]]]

def get_start_vals(xy_segment: list[str]) -> dict[str, bool]:
	return {
		l: int(r) == 1 # no need to strip
		for i in xy_segment
		for l, r in [i.split(':')]
	}

def get_rule_by_out(rule_lines: list[str]) -> RULE_BY_OUT:
	result = {}
	for rl in rule_lines:
		op1, op, op2, _, r = rl.split()
		result[r] = (op, [op1, op2])
	return result

def determine_val(wire: str, vals: dict[str, bool], rule_by_out: RULE_BY_OUT):
	if wire not in vals:
		operator, operands = rule_by_out[wire]
		for o in operands:
			determine_val(o, vals, rule_by_out)
		op_fn ={'AND': op.and_, 'OR': op.or_, 'XOR': op.xor}[operator]
		vals[wire] = op_fn(*[vals[o] for o in operands])

def get_z(vals) -> int:
	z_keys = [z for z in vals if z.startswith('z')]
	z_vals = [vals[z] for z in sorted(z_keys, reverse=True)]
	return ft.reduce(lambda x, y: x * 2 + y, z_vals, 0)

def test_first():
	xy_seg, rules_seg = file.segments('2024/24')
	vals = get_start_vals(xy_seg)
	rule_by_out = get_rule_by_out(rules_seg)
	for w in rule_by_out:
		determine_val(w, vals, rule_by_out)
	assert 47666458872582 == get_z(vals)
