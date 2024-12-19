from api import file

def get_files_and_frees_intervals():
	pos = 0
	ivs = ([], [])
	for i, l in enumerate(file.readall('2024/09_ex')):
		ivs[i % 2].append((pos, int(l)))
		pos += int(l)
	return ivs

def atomize_files(file_iv):
	f_id_by_idx = {}
	atomized_file_iv = []
	for f_id, (f_pos, f_l) in enumerate(file_iv):
		for i in range(f_l):
			f_id_by_idx[len(atomized_file_iv)] = f_id
			atomized_file_iv.append((f_pos + i, 1))
	return atomized_file_iv, lambda idx: f_id_by_idx[idx]

def move_file(file_iv, free_iv, f_idx):
	f_pos, f_l = file_iv[f_idx]
	for fr_idx, (fr_pos, fr_l) in enumerate(free_iv):
		if fr_pos <= f_pos and fr_l >= f_l:
			file_iv[f_idx] = (fr_pos, f_l)
			free_iv[fr_idx] = (fr_pos + f_l, fr_l - f_l)
			return

def move_files(file_iv, free_iv):
	for f_idx in range(len(file_iv) - 1, -1, -1):
		move_file(file_iv, free_iv, f_idx)

def get_checksum(file_iv, f_id_by_idx = lambda idx: idx):
	return sum(
		(f_pos + i) * f_id_by_idx(f_id)
		for f_id, (f_pos, f_l) in enumerate(file_iv)
		for i in range(f_l)
	)

def test_first():
	file_iv, free_iv = get_files_and_frees_intervals()
	atomized_file_iv, f_id_by_idx = atomize_files(file_iv)
	move_files(atomized_file_iv, free_iv)
	assert 1928 == get_checksum(atomized_file_iv, f_id_by_idx)

def test_second():
	file_iv, free_iv = get_files_and_frees_intervals()
	move_files(file_iv, free_iv)
	assert 2858 == get_checksum(file_iv)
