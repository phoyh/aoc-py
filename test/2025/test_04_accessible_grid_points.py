from api import file, PDict

def get_rolls():
	return PDict.from_lines(file.lines('2025/04_ex')).by_value('@')

def get_accessible(rolls):
	return {
		p
		for p in rolls
		if sum(n in rolls for n in p.neighbors(diag=True)) < 4
	}

def test_first():
	assert 13 == len(get_accessible(get_rolls()))

def test_second():
	ac = rolls = get_rolls()
	start_count = len(rolls)
	while ac:
		ac = get_accessible(rolls)
		rolls -= ac
	assert 43 == start_count - len(rolls)