from __future__ import annotations
import itertools as it
import functools as ft
import operator as op

class CubeSet:
	def __init__(self, cubes: list[Cube] | None = None):
		self.__cubes = [c.copy() for c in cubes] if cubes else []
		self.__normalize()

	# PRIVATE

	def __remove_intersections_subtract(self, minuend: Cube, subtrahend: Cube) -> list[Cube]:
		if len(minuend & subtrahend) == 0:
			return [minuend]
		subtrahend_iv = subtrahend.get_intervals()
		minuend_iv = minuend.get_intervals()
		dim_num = len(subtrahend_iv)
		result = []
		key_vals_per_dim = [
			(min(ocs, ncs), max(ocs, ncs), min(oce, nce) + 1, max(oce, nce) + 1)
			for (ocs, oce), (ncs, nce) in zip(subtrahend_iv, minuend_iv)
		]
		for area_indexes in it.product(range(3), repeat=dim_num):
			new_iv = [
				(key_vals_per_dim[i][ai], key_vals_per_dim[i][ai+1] - 1)
				for i, ai in enumerate(area_indexes)
			]
			if all(s <= e for s, e in new_iv):
				lowest_point = tuple(s for s, _ in new_iv)
				if lowest_point not in subtrahend and lowest_point in minuend:
					result += [Cube(new_iv)]
		return result

	def __remove_intersections(self):
		todo = self.__cubes
		self.__cubes = []
		while len(todo) > 0:
			subcubes = [todo.pop()]
			for subtrahend in todo:
				last_subcubes = subcubes
				subcubes = []
				for minuend in last_subcubes:
					subcubes += self.__remove_intersections_subtract(minuend, subtrahend)
			self.__cubes += subcubes

	def __merge_adjacent_candidate(self, base_cube: Cube, candidate_cube: Cube) -> Cube | None:
		base_cube_iv = base_cube.get_intervals()
		candidate_cube_iv = candidate_cube.get_intervals()
		for di, ((bcs, bce), (ccs, cce)) in enumerate(zip(base_cube_iv, candidate_cube_iv)):
			if bce + 1 == ccs or cce + 1 == bcs:
				if all(base_cube_iv[odi] == candidate_cube_iv[odi]
						for odi in range(len(base_cube_iv)) if odi != di):
					base_cube_iv[di] = (min(ccs, bcs), max(cce, bce))
					return Cube(base_cube_iv)

	def __merge_adjacent(self):
		has_changed = True
		while has_changed:
			has_changed = False
			todo = self.__cubes
			self.__cubes = []
			while len(todo) > 0:
				c = todo.pop()
				for ci in range(len(todo) - 1, -1, -1):
					changed_c = self.__merge_adjacent_candidate(c, todo[ci])
					if changed_c:
						c = changed_c
						todo = todo[:ci] + todo[ci+1:]
						has_changed = True
				self.__cubes += [c]

	def __normalize(self):
		self.__cubes = [c for c in self.__cubes if len(c) > 0]
		if len(self.__cubes) == 0:
			return
		dim_num = len(self.__cubes[0].get_intervals())
		if any(len(c.get_intervals()) != dim_num for c in self.__cubes):
			return
		self.__remove_intersections()
		self.__merge_adjacent()

	# OVERRIDE

	def __str__(self):
		cube_strs = [str(c) for c in self.__cubes]
		return '[ ' + ' ] , [ '.join(sorted(cube_strs)) + ' ]'
	
	def __len__(self):
		return sum(len(c) for c in self.__cubes)
	
	def __or__(self, param: Cube | CubeSet) -> CubeSet:
		if isinstance(param, Cube):
			param = CubeSet([param])
		return CubeSet(self.__cubes + param.get_cubes())
	
	def __and__(self, param: CubeSet | Cube) -> CubeSet:
		if isinstance(param, Cube):
			param = CubeSet([param])
		return CubeSet([c1 & c2 for c1 in self.__cubes for c2 in param.get_cubes()])

	def __sub__(self, param: CubeSet | Cube) -> CubeSet:
		if len(self.__cubes) == 0:
			return CubeSet([])
		dim_num = len(self.__cubes[0].get_intervals())
		if isinstance(param, Cube):
			param = CubeSet([param])
		param_cubes = param.get_cubes()
		if not isinstance(param, CubeSet) or len(param_cubes) == 0 \
				or dim_num != len(param_cubes[0].get_intervals()):
			return CubeSet(self.__cubes)
		cubes = []
		for c in self.__cubes:
			subcubes = [c]
			for subtrahend in param_cubes:
				last_subcubes = subcubes
				subcubes = []
				for minuend in last_subcubes:
					subcubes += self.__remove_intersections_subtract(minuend, subtrahend)
			cubes += subcubes
		return CubeSet(cubes)
	
	def __contains__(self, param: TP | Cube | CubeSet) -> bool:
		if not isinstance(param, tuple):
			cube_or_cubeset : Cube | CubeSet = param
			return len(self & cube_or_cubeset) == len(cube_or_cubeset)
		point_tuple = param
		return any(point_tuple in c for c in self.__cubes)

	def __eq__(self, other: CubeSet) -> bool:
		return other in self and self in other

	def copy(self) -> CubeSet:
		"""
		You'll never need this as a cube does not offer any method that has side effects
		"""
		return CubeSet(self.get_cubes())

	# OTHER FUNCTIONALITY

	def get_cubes(self) -> list[Cube]:
		return [*self.__cubes]

	def split(self, dim_index: int, lower_equal_value: int) -> tuple[CubeSet, CubeSet]:
		"""
		Split cube set into two parts determined by the cut on the dimension denoted by 'dim_index'.

		All points that conform to the <= 'lower_equal_value' on that dimension are returned
		in the returned tuple's first component, the others in the second.
		"""
		lefts = []
		rights = []
		for c in self.__cubes:
			left, right = c.split(dim_index, lower_equal_value)
			if left:
				lefts.append(left)
			if right:
				rights.append(right)
		return CubeSet(lefts), CubeSet(rights)

	def to_points(self) -> PSet:
		return ft.reduce(op.or_, map(Cube.to_points, self.__cubes))

# late import to allow cyclic references between cube(set) and point(dict/list/set)
# pylint: disable=wrong-import-position
from .cube import Cube
from .point import TP, PSet
