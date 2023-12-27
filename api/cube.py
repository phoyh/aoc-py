from __future__ import annotations
import itertools as it
import math

class Cube:
	def __init__(self, intervals_by_dimension: list[tuple[int, int]]):
		assert isinstance(intervals_by_dimension, list)
		assert all(isinstance(i, tuple) for i in intervals_by_dimension)
		self.__iv = intervals_by_dimension.copy()
	
	# OVERRIDE

	def __str__(self) -> str:
		dim_str = [f'{s} -> {e}' if e != s else str(s) for s, e in self.__iv]
		return ' | '.join(dim_str)
	
	def __len__(self) -> int:
		if len(self.__iv) == 0:
			return 0
		return math.prod(e - s + 1 for s, e in self.__iv)
	
	def __and__(self, param: Cube) -> Cube:
		param_iv = param.get_intervals()
		if len(param_iv) != len(self.__iv):
			return Cube([])
		res_iv = []
		for (sa, ea), (sb, eb) in zip(param_iv, self.__iv):
			s = max(sa, sb)
			e = min(ea, eb)
			if s > e:
				return Cube([])
			res_iv += [(s, e)]
		return Cube(res_iv)
	
	def __or__(self, param: Cube) -> CubeSet:
		return CubeSet([self, param])
	
	def __sub__(self, param: Cube | CubeSet) -> CubeSet:
		return CubeSet([self]) - param
	
	def __contains__(self, param: TP | Cube) -> bool:
		if isinstance(param, Cube):
			cube = param
			return len(self & cube) == len(cube)
		if not isinstance(param, tuple):
			return False
		point_tuple = param
		if len(self.__iv) != len(point_tuple):
			return False
		return all(s <= p <= e for p, (s, e) in zip(point_tuple, self.__iv))

	def __eq__(self, other: Cube):
		return other in self and self in other

	def copy(self) -> Cube:
		"""
		You'll never need this as a cube does not offer any method that has side effects
		"""
		return Cube(self.__iv)

	# CUSTOM METHODS

	def get_intervals(self) -> list[tuple[int, int]]:
		return self.__iv.copy()

	def max(self) -> list[int]:
		return [max(e) for e in self.__iv]

	def min(self) -> list[int]:
		return [min(e) for e in self.__iv]

	def move(self, vector: TP):
		assert len(self.__iv) == len(vector)
		return Cube([(s + v, e + v) for (s, e), v in zip(self.__iv, vector)])
	
	def quadrants(self) -> list[Cube]:
		"""
		returns list and not set
		because cubes might be extremely costly to hash / test for duplicates (as required by set)
		"""
		sub_intervals = [
			[(s, (s + e) // 2), ((s + e) // 2 + 1, e)] if s < e else [(s, e)]
			for s, e in self.__iv
		]
		cubes = []
		for idxs in it.product(range(2), repeat=len(self.__iv)):
			z = list(zip(idxs, sub_intervals))
			if all(idx < len(si) for idx, si in z):
				cubes.append(Cube([si[idx] for idx, si in z]))
		return cubes
	
	def split(self, dim_index: int, lower_equal_value: int) -> tuple[Cube | None, Cube | None]:
		"""
		Splits cube into two parts determined by the cut on the dimension denoted by 'dim_index'.

		All points that conform to the <= 'lower_equal_value' on that dimension are returned
		in the returned tuple's first component, the others in the second.
		If one component does not contain any point, None is provided instead.
		"""
		assert 0 <= dim_index < len(self.__iv)
		mi, ma = self.__iv[dim_index]
		if lower_equal_value < mi:
			return None, self
		if lower_equal_value >= ma:
			return self, None
		left_iv = self.__iv.copy()
		left_iv[dim_index] = (mi, lower_equal_value)
		right_iv = self.__iv.copy()
		right_iv[dim_index] = (lower_equal_value + 1, ma)
		return Cube(left_iv), Cube(right_iv)

	def to_points(self) -> PSet:
		ranges = [range(mi, ma + 1) for mi, ma in self.get_intervals()]
		return PSet({
			P(t)
			for t in it.product(*ranges)
		})

# late import to allow cyclic references between cube(set) and point(dict/list/set)
# pylint: disable=wrong-import-position
from .cubeset import CubeSet
from .point import TP, P, PSet
