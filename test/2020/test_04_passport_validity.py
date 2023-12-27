import re
import api.file

def get_passports():
	return [
		dict(part.split(':') for part in ' '.join(s).split(' '))
		for s in api.file.segments('2020/04')
	]

def is_valid_keys(pp):
	pp['cid'] = ''
	return len(pp.keys()) == 8

def is_year_valid(y, min_y, max_y):
	yi = int(y)
	return min_y <= yi <= max_y

def is_height_valid(hgt):
	hgti = int(hgt[:-2])
	match hgt[-2:]:
		case 'cm':
			return 150 <= hgti <= 193
		case 'in':
			return 59 <= hgti <= 76
		case '_':
			return False

def is_valid_content(pp):
	try:
		return all([
			is_year_valid(pp['byr'], 1920, 2002),
			is_year_valid(pp['iyr'], 2010, 2020),
			is_year_valid(pp['eyr'], 2020, 2030),
			is_height_valid(pp['hgt']),
			pp['ecl'] in 'amb blu brn gry grn hzl oth'.split(),
			re.fullmatch(r'#[0-9a-f]{6}', pp['hcl']),
			re.fullmatch(r'\d{9}', pp['pid'])
		])
	except (KeyError, ValueError):
		return False

def test_first():
	assert 222 == sum(is_valid_keys(pp) for pp in get_passports())

def test_second():
	assert 140 == sum(is_valid_content(pp) for pp in get_passports())