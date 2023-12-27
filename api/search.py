import typing

def binary(lower_bound: int, upper_bound: int, direction: typing.Callable[[int], int]) \
		-> int | None:
	"""
	direction:
		Returns 0 if spot is found,
		otherwise return any positive (negative) if spot is on the right (left)
	"""
	while lower_bound <= upper_bound:
		mid = (lower_bound + upper_bound) // 2
		d = direction(mid)
		if d == 0:
			return mid
		if d > 0:
			lower_bound = mid + 1
		else:
			upper_bound = mid - 1
	return None

def sign_change(lower_bound: int, upper_bound: int, func: typing.Callable[[int], float]) -> int:
	"""
	When does provided function change its sign?

	Note: 0 is treated as positive

	Precondition: sign(func(lower_bound)) != sign(func(upper_bound))

	Returns number for which sign(func(number)) != sign(func(number - 1))
	"""
	if func(lower_bound) < 0 <= func(upper_bound):
		normalizer = 1
	elif func(lower_bound) >= 0 > func(upper_bound):
		normalizer = -1
	else:
		assert False
	def direction(n):
		return 1 if normalizer * func(n) < 0 else (-1 if normalizer * func(n - 1) >= 0 else 0)
	result = binary(lower_bound, upper_bound, direction)
	assert result is not None
	return result