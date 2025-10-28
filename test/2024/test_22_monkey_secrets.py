from collections import defaultdict
from api import file

def get_start_secrets():
	return file.lines('2024/22_ex', int)

def next_secret(s):
	m = 2 ** 24 - 1
	s ^= s << 6 & m
	s ^= s >> 5
	s ^= s << 11 & m
	return s

def test_first():
	secrets = get_start_secrets()
	for _ in range(2000):
		secrets = [next_secret(s) for s in secrets]
	assert 37327623 == sum(secrets)

def test_second():
	secrets = get_start_secrets()
	last_diffs_by_buyer = [() for _ in secrets]
	buy_idx_by_monkey = defaultdict(set)
	bananas_by_monkey = defaultdict(int)
	for _ in range(2000):
		next_secrets = [next_secret(s) for s in secrets]
		last_diffs_by_buyer = [
			(*d[-3:], str(next_secrets[bi] % 10 - secrets[bi] % 10))
			for bi, d in enumerate(last_diffs_by_buyer)
		]
		if len(last_diffs_by_buyer[0]) == 4:
			for bi, d in enumerate(last_diffs_by_buyer):
				if bi not in buy_idx_by_monkey[d]:
					buy_idx_by_monkey[d].add(bi)
					bananas_by_monkey[d] += next_secrets[bi] % 10
		secrets = next_secrets
	assert 24 == max(bananas_by_monkey.values())
