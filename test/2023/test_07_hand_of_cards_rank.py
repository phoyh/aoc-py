from collections import Counter

import api.file

def get_desc_counters(hand):
	return sorted(Counter(hand).values(), reverse=True)

def line_to_contestant(l, j_is_joker):
	hand, bid_str = l.split()
	card_order = ''.join(reversed('A, K, Q, J, T, 9, 8, 7, 6, 5, 4, 3, 2'.split(', ')))
	if j_is_joker:
		card_order = 'J' + card_order.replace('J', '')
		h_desc_counter = get_desc_counters(hand.replace('J', '')) + [0]
		h_desc_counter[0] += hand.count('J')
	else:
		h_desc_counter = get_desc_counters(hand)
	value = h_desc_counter, *map(card_order.index, hand)
	return value, int(bid_str)

def get_winnings_sum(j_is_joker = False):
	contestants = api.file.lines('2023/07', lambda l: line_to_contestant(l, j_is_joker))
	return sum(rank * bid for rank, (_, bid) in enumerate(sorted(contestants), 1))

def test_first():
	assert 251121738 == get_winnings_sum()

def test_second():
	assert 251421071 == get_winnings_sum(j_is_joker = True)
