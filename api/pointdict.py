from __future__ import annotations
import itertools as it
from typing import TypeVar, Any, Callable
import os
from PIL import Image
import numpy as np

from .point import P, TP

TV = TypeVar('TV')

# Yes, there are many methods - but this is a very versatile class
# pylint: disable-next=too-many-public-methods
class PDict(dict[P, TV]):
	"""
	Grid utilities for a dictionary which maps points to values (not necessarily ints).

	All operations are FUNCTIONAL (without side-effects) and
	always return a new instance for the result.

	The dictionary is a lazy default dictionary - requesting the value of unknown keys
	yields the default value of the value type.
	(Such defaulting only works if dictionary is not empty, of course.)

	Drawing operations on the dictionary return same dictionary type (dict vs. defaultdict),
	complete transformations do not.
	"""

	# OVERRIDE

	def __or__(self, other: dict[P, TV]) -> PDict:
		return PDict(dict.__or__(self, other))
	
	def __sub__(self, other: dict[P, TV] | TPSet | list[P]) -> PDict:
		if isinstance(other, list):
			other = set(other)
		return PDict({
			k: v
			for k, v in self.items()
			if (isinstance(other, set) and k not in other)
				or (isinstance(other, dict) and (k not in other or other[k] != v)) # type: ignore pylance
		})

	def __getitem__(self, key) -> TV:
		if key in self:
			return dict.__getitem__(self, key)
		for e in self.values():
			return type(e)()
		assert False, f'tried to get value for key {key} in empty dictionary'

	def copy(self) -> PDict:
		return PDict(dict.copy(self))

	def keys(self) -> PSet:
		return PSet(dict.keys(self))
	
	# DIMENSIONS (FACADE FOR KEY SETS)

	def max_by_dim(self) -> list[int]:
		return self.keys().max_by_dim()

	def minmax_by_dim(self) -> list[tuple[int, int]]:
		return self.keys().minmax_by_dim()

	def range_by_dim(self) -> list[range]:
		return self.keys().range_by_dim()

	def size_by_dim(self) -> list[int]:
		return self.keys().size_by_dim()

	# EXTENSIONS

	def by_value(self, value_for_which_points_are_found: TV) \
			-> PSet:
		return PSet({p for p, v in self.items() if v == value_for_which_points_are_found})

	def by_not_value(self, value_for_which_points_are_excluded: TV) \
			-> PSet:
		return PSet({p for p, v in self.items() if v != value_for_which_points_are_excluded})

	def by_values(self, values_for_which_points_are_found: set[TV] | list[TV] | str) \
			-> PSet:
		"""
		String can be provided as parameter if TV is char.
		"""
		if isinstance(values_for_which_points_are_found, str):
			vals = set(values_for_which_points_are_found)
		elif isinstance(values_for_which_points_are_found, list):
			vals = set(values_for_which_points_are_found)
		else:
			vals = values_for_which_points_are_found
		return PSet({p for p, v in self.items() if v in vals})

	def diff_points(self, other: dict[P, TV]) -> PSet:
		one_sided = lambda d1, d2: PSet(
			{d1k for d1k, d1v in d1.items() if d1k not in d2 or d2[d1k] != d1v}
		)
		return one_sided(self, other) | one_sided(other, self)

	def draw_line(self, start_point: TP, end_point: TP,
			value_to_be_drawn: TV) -> PDict:
		""" assert that line is horizontal, vertical or diagonal """
		result = self.copy()
		p = np.array(start_point)
		e = np.array(end_point)
		assert len(p) == len(e)
		bearing = np.sign(e - p)
		if (bearing == 0).all():
			result[P(p)] = value_to_be_drawn
			return result
		steps_per_dim = bearing * (e - p)
		steps = max(steps_per_dim)
		assert ((steps_per_dim == 0) | (steps_per_dim == steps)).all()
		while (p != e + bearing).any():
			result[P(p)] = value_to_be_drawn
			p += bearing
		return result

	def draw_set(self, points_where_to_draw: TPSet,
			value_to_be_drawn: TV) -> PDict:
		result = self.copy()
		for p in points_where_to_draw:
			result[p] = value_to_be_drawn
		return result

	def filter(self, predicate: Callable[[TP, TV], bool]) -> PDict:
		return PDict({
			p: v
			for p, v in self.items()
			if predicate(p, v)
		})

	def flood(self, flood_value: TV, start_point: TP, diag: bool = False,
			matches: Callable[[tuple[TP, TV], tuple[TP, TV]], bool] = lambda a, b: a[1] == b[1]) -> PDict:
		"""
		Obtains the regions based on start_point and paints them with flood_value
		"""
		return self.draw_set(self.region(start_point, diag, matches), flood_value)

	def fringe(self, diag: bool = False) -> PDict:
		return PDict({p: self[p] for p in self.keys().fringe(diag = diag)})

	def move(self, vector: TP) -> PDict:
		return PDict({p + vector: value for p, value in self.items()})

	def pad(self, value: TV, diag: bool = False, distance: int = 1) \
			-> PDict:
		return PDict({
			n: value
			for p in self.fringe()
			for n in p.neighbors(diag=diag, dist=distance)
		} | self)

	def region(self, start_point: TP, diag: bool = False,
			matches: Callable[[tuple[TP, TV], tuple[TP, TV]], bool] = lambda a, b: a[1] == b[1]) -> PSet:
		"""
		Expands the start point based on the matcher
		(defaulted to identical values, meaning tolerance = 0).
		
		All (transitively) adjacent points will be considered
		as long there is a path allowed by the matcher.
		"""
		start_point = P.box(start_point)
		result = PSet()
		todo = [start_point]
		while todo:
			p = todo.pop()
			if p not in result:
				result.add(p)
				for n in p.neighbors(diag, self):
					if matches((p, self[p]), (n, self[n])):
						todo.append(n)
		return result
	
	def transpose(self) -> PDict:
		return PDict({p.transpose(): v for p, v in self.items()})

	# IMPORT / EXPORT

	@staticmethod
	def from_points(points: PSet, point_value: TV, no_point_value: TV):
		return PDict.from_minmax(points.minmax_by_dim(), no_point_value).draw_set(points, point_value)

	@staticmethod
	def from_lines(lines_with_char1_values: list[str],
			value_mapper: Callable[[str], Any] = lambda c: c) -> PDict:
		return PDict({
			P((x, y)): value_mapper(v)
			for y, l in enumerate(lines_with_char1_values)
			for x, v in enumerate(l)
		})

	@staticmethod
	def from_minmax(minmax_by_dim: list[tuple[int, int]], value: TV) -> PDict:
		result = PDict()
		for p in it.product(*[range(mi, ma + 1) for mi, ma in minmax_by_dim]):
			result[P(p)] = value
		return result

	@staticmethod
	def from_size(length_by_dim: list[int], value: TV) -> PDict:
		result = PDict()
		for p in it.product(*[range(lbd) for lbd in length_by_dim]):
			result[P(p)] = value
		return result

	def to_complex_keys_2d(self) -> dict[complex, TV]:
		return {complex(x, y): v for (x, y), v in self.items()}

	def to_lines_2d(self) -> list[str]:
		(minx, maxx), (miny, maxy), *_ = self.keys().minmax_by_dim()
		matrix = np.full((maxy - miny + 1, maxx - minx + 1), ' ')
		for x, y in self:
			matrix[y - miny, x - minx] = self[P((x, y))]
		return [''.join(l) for l in matrix]

	def to_png(self, file_name: str, file_dir: str = ''):
		"""
		Exports the dictionary as a PNG file.
		Assumes that the values are RGB int-tuples.
		The [file_path/file_name] is relative to ./exports and should not contain the extension.
		"""
		(min_x, max_x), (min_y, max_y) = self.keys().minmax_by_dim()
		im = Image.new('RGB', (max_x - min_x + 1, max_y - min_y + 1))
		for p in self:
			x, y = p
			im.putpixel((x - min_x, y - min_y), self[p])  # type: ignore
		file_dir = f'exports/{file_dir}'
		if not os.path.exists(file_dir):
			os.makedirs(file_dir)
		im.save(f'{file_dir}/{file_name}.png')

	def to_str_2d(self) -> str:
		return '\n'.join(self.to_lines_2d())

# late import to allow cyclic references between cube(set) and point(dict/list/set)
# pylint: disable=wrong-import-position
from .pointset import PSet, TPSet
