from api import file

def get_path_count_on_last_line_and_active_carrot_count():
	lines = file.lines('2025/07')
	cur_path_counts = [c == 'S' for c in lines[0]]
	active_carrot_count = 0
	for line in lines[1:]:
		next_path_counts = [0] * len(line)
		for i, c in enumerate(line):
			pc = cur_path_counts[i]
			if pc > 0:
				if c == '^':
					next_path_counts[i - 1] += pc
					next_path_counts[i + 1] += pc
					active_carrot_count += 1
				else:
					next_path_counts[i] += pc
		cur_path_counts = next_path_counts
	return cur_path_counts, active_carrot_count

def test_first():
	_, active_carrot_count = get_path_count_on_last_line_and_active_carrot_count()
	assert 1594 == active_carrot_count

def test_second():
	cur_path_counts, _ = get_path_count_on_last_line_and_active_carrot_count()
	assert 15650261281478 == sum(cur_path_counts)
