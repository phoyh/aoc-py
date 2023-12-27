from collections import defaultdict
from api import Cube, CubeSet, file, RSet, parse, P

def parse_input():
	wfs_raw, ps_raw = file.segments('2023/19_ex')
	wfs = {}
	for wf_raw in wfs_raw:
		base_label, rest_raw = wf_raw.split('{')
		conds_raw = rest_raw[:-1].split(',')
		for wfkidx, cond_raw in enumerate(conds_raw[:-1]):
			label = base_label + str(wfkidx) if wfkidx else base_label
			other_dest = base_label + str(wfkidx + 1) if wfkidx < len(conds_raw) - 2 else conds_raw[-1]
			op_raw, dest = cond_raw.split(':')
			wfs[label] = (dest, other_dest, 'xmas'.index(op_raw[0]), op_raw[1], int(op_raw[2:]))
	cs = CubeSet([
		P(tuple(parse.ints(p_raw))).to_cube()
		for p_raw in ps_raw
	])
	return wfs, cs

def do_step(wfs, cs_by_label, pos):
	if pos not in wfs:
		return
	cs = cs_by_label[pos]
	dest, other_dest, varidx, op, num = wfs[pos]
	left, right = cs.split(varidx, num - (op == '<'))
	if op == '>':
		left, right = right, left
	cs_by_label[dest] |= cs & left
	cs_by_label[other_dest] |= cs & right

def solve(wfs, start_cs) -> CubeSet:
	topo = RSet({
		k: {d, od}
		for k, (d, od, *_) in wfs.items()
	}).topologic_order()
	assert topo[0] == 'in'
	cs_by_label = defaultdict(CubeSet)
	cs_by_label[topo[0]] = start_cs
	for pos in topo:
		do_step(wfs, cs_by_label, pos)
	return cs_by_label['A']
		
def test_first():
	wfs, start_cs = parse_input()
	cs = solve(wfs, start_cs)
	assert 19114 == sum(c for p in cs.to_points() for c in p)

def test_second():
	wfs, _ = parse_input()
	cs = solve(wfs, CubeSet([Cube([(1, 4000)] * 4)]))
	assert 167409079868000 == len(cs)
