import api.file

MAGIC_NUMBER = 20201227

def get_loop_size(pk, subject_nmbr):
	i = 0
	val = 1
	while val != pk:
		val = (val * subject_nmbr) % MAGIC_NUMBER
		i += 1
	return i

def test_first():
	card_pk, door_pk = [int(l) for l in api.file.lines('2020/25_ex')]
	card_loop_size = get_loop_size(card_pk, 7)
	assert 14897079 == pow(door_pk, card_loop_size, MAGIC_NUMBER)
