from __future__ import annotations
import operator as op
import functools as ft

from .graph import Vertix

TRSet = dict[Vertix, set[Vertix]]

class RSet(TRSet):
	"""
	Defines directed, unattributed relationship R between vertices.

	R's semantics are left open and only defined as needed by methods.
	For R(x, y), x is 'from' and y is 'to'.

	Acts like a defaultdict:
	Relationships can be directly added with R[x].add(y), even if x is not yet known.
	"""

	# OVERRIDE

	def __getitem__(self, key) -> set[Vertix]: # type: ignore
		if key not in self:
			self[key] = set()
		return dict.__getitem__(self, key)

	def __or__(self, other: TRSet | set[Vertix]) -> RSet:
		"""
		Also accepts vertix set as operand (those vertices assumed to have no TO)
		"""
		if isinstance(other, set):
			other = {k: set() for k in other - self.keys()}
		return RSet(dict.__or__(self, other))

	def copy(self) -> RSet:
		"""
		Also clones the respective sets.
		"""
		return RSet({k: v.copy() for k, v in self.items()})

	# OTHERS

	def reverse(self) -> RSet:
		"""
		Swaps FROM and TO: R(x, y) to R(y, x).

		Maintains all known vertices (and adds empty value set if necessary.)

		Useful for switching between 'successors_by' and 'predecessors_by'.
		"""
		return RSet({
			v: {f for f, t in self.items() if v in t}
			for v in self.vertices()
		})

	def topologic_order(self, is_predecessors_by: bool = False) \
			-> list[Vertix]: # type: ignore
		"""
		R is interpreted as 'successors_by' if 'is_predecessors_by' is not set.

		All vertices are guaranteed to be returned (both FROM and TO elements).

		Must not be called if R contains cycles.
		"""
		predecessors_by = self.copy() | self.vertices() if is_predecessors_by else self.reverse()
		result = []
		while (v := next((t for t, f in predecessors_by.items() if not f), None)) is not None:
			result.append(v)
			del predecessors_by[v]
			for t in predecessors_by:
				predecessors_by[t].discard(v)
		if any(f for f in predecessors_by.values()):
			# cycle detected - no topologic order can be determined
			assert False, [(t, f) for t, f in predecessors_by.items() if f]
		return result

	def transitive_closure(self) -> RSet:
		result = self.copy()
		for thro in self:
			for fro in self:
				if thro in result[fro]:
					result[fro] |= result[thro]
		return result

	def vertices(self) -> set[Vertix]: # type: ignore
		return ft.reduce(op.or_, self.values(), self.keys())

	# IMPORT / EXPORT

	@staticmethod
	def from_dictlist(dict_with_lists: dict[Vertix, list[Vertix]]) -> RSet:
		"""
		Converts a dict with lists to a dict with sets (=RSet).
		"""
		return RSet({k: set(v) for k, v in dict_with_lists.items()})

	@staticmethod
	def from_list(l: list[tuple[Vertix, Vertix]] | list[list[Vertix]]) -> RSet:
		"""
		Converts a list of 2d-tuples or 2e-lists to a dict with sets (=RSet).
		It combines the right side of all tuples/lists that share the same key (=left).
		"""
		result = RSet()
		for fro, to in l:
			result[fro].add(to)
		return result
	
	def to_dictlist(self) -> dict[Vertix, list[Vertix]]:
		return {k: list(v) for k, v in self.items()}

	def to_tuplelist(self) -> list[tuple[Vertix, Vertix]]:
		return [(k, v) for k, vs in self.items() for v in vs]
