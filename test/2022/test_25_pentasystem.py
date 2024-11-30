from api import file

def snafu_to_num(snafu):
	result = 0
	for s in snafu:
		result *= 5
		result += '=-012'.index(s) - 2
	return result

def num_to_snafu(num):
	result = ''
	while num:
		result = '012=-'[num % 5] + result
		num = (num + 2) // 5
	return result

def test_first():
	snafus = file.lines('2022/25')
	dec_sum = sum(snafu_to_num(s) for s in snafus)
	assert '2-0-0=1-0=2====20=-2' == num_to_snafu(dec_sum)
