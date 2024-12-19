from api import file

def get_player_hands_start():
	segs = file.segments('2020/22_ex')
	return [tuple(int(l) for l in s[1:]) for s in segs]

def play(player_hand_a: tuple[int, ...], player_hand_b: tuple[int, ...], with_recursive):
	hands = [[*player_hand_a], [*player_hand_b]]
	seen = set()
	while all(hands[i] for i in range(2)):
		hands_tuple = tuple(tuple(h) for h in hands)
		if hands_tuple in seen and with_recursive:
			return 0, hands
		seen.add(hands_tuple)
		cards = [hands[i].pop(0) for i in range(2)]
		winner_idx = cards[1] > cards[0]
		if with_recursive and all(len(h) >= c for h, c in zip(hands, cards)):
			winner_idx, _ = play(
				*[tuple(h[:c]) for h, c in zip(hands, cards)],
				with_recursive=with_recursive
			)
		hands[winner_idx].extend([cards[winner_idx], cards[1-winner_idx]])
	winner_idx = 0 if hands[0] else 1
	return winner_idx, hands

def get_score(winner_hand):
	return sum((i + 1) * c for i, c in enumerate(reversed(winner_hand)))

def test_first():
	player_hands = get_player_hands_start()
	winner_idx, post_player_hands = play(*player_hands, with_recursive=False)
	assert 306 == get_score(post_player_hands[winner_idx])

def test_second():
	player_hands = get_player_hands_start()
	winner_idx, post_player_hands = play(*player_hands, with_recursive=True)
	assert 291 == get_score(post_player_hands[winner_idx])
