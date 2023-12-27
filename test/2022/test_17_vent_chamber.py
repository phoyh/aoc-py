import api.file

def can_move_on(rc, rock, chamber):
	return all(
		(nrec := rec + rc) not in chamber and 0 <= nrec.real < 7
		for rec in rock
	)

def drop_rock_and_get_rxy_vix(rock, rc, chamber, vents, vix):
	while True:
		vc = vents[vix]
		vix = (vix + 1) % len(vents)
		if can_move_on(vc + rc, rock, chamber):
			rc += vc
		if can_move_on(-1j + rc, rock, chamber):
			rc -= 1j
		else:
			return (rc, vix)

def simulate_by_history_and_get_result_maxy(history_record, step, total_step_num, maxy):
	hstep, hmaxy = history_record
	rest_steps = total_step_num - step
	step_diff_history = step - hstep
	if rest_steps % step_diff_history == 0:
		return maxy + (maxy - hmaxy) * (rest_steps // step_diff_history)

def execute(total_step_num):
	vents = [1 if c == '>' else -1 for c in api.file.readall('2022/17')]
	rock_types = [
		{0, 1, 2, 3},
		{1, 1j, 1+1j, 2+1j, 1+2j},
		{0, 1, 2, 2+1j, 2+2j},
		{0, 1j, 2j, 3j},
		{0, 1j, 1, 1+1j}
	]
	chamber = set(range(7))
	rti = 0
	maxy = 0
	vix = 0
	history: dict[tuple[int, int], tuple[int, int]] = {}
	for step in range(total_step_num):
		if (hkey := (rti, vix)) in history:
			if result:= simulate_by_history_and_get_result_maxy(history[hkey], step, total_step_num, maxy):
				return result
		else:
			history[hkey] = step, maxy
		rock = rock_types[rti]
		rti = (rti + 1) % 5
		rc, vix = drop_rock_and_get_rxy_vix(rock, complex(2, maxy + 4), chamber, vents, vix)
		for rec in rock:
			chamber.add(cc := rc + rec)
			maxy = max(maxy, cc.imag)
	return maxy

def test_first():
	assert execute(2022) == 3048

def test_second():
	assert execute(1000000000000) == 1504093567249