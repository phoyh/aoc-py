from __future__ import annotations
from typing import TypeVar, Callable
from collections import defaultdict

from .graph import Vertix
from .relset import RSet

TV = TypeVar('TV')

TRDict = dict[Vertix, dict[Vertix, TV]]

class RDict(TRDict):
	"""
	Defines directed, attributed relationship R between vertices.

	R's semantics are left open and only defined as needed by methods.
	For R(x, y), x is 'from' and y is 'to'.

	Acts like a defaultdict:
	Relationships can be directly added with R[x][y] = v, even if x is not yet known.

	Attributes are defaulted to int:
	R[x][y] for unknown y yields zero.
	"""

	# OVERRIDE

	def __getitem__(self, key) -> dict[Vertix, TV]: # type: ignore
		if key not in self:
			self[key] = defaultdict(int)
		return dict.__getitem__(self, key)

	def __or__(self, other: TRDict | set[Vertix]) -> RDict:
		"""
		Also accepts vertix set as operand (those vertices assumed to have no TO).

		If RDict is operand, the FROMs are merged (instead of being overwritten).
		"""
		if isinstance(other, RDict):
			vertices = self.vertices() | other.vertices()
			return RDict({
				v: self[v] | other[v]
				for v in vertices
			})
		if isinstance(other, set):
			other = {k: defaultdict(int) for k in other - set(self.keys())}
		return RDict(dict.__or__(self, other))

	def copy(self) -> RDict:
		"""
		Also clones the respective dictionaries.
		"""
		return RDict({k: v.copy() for k, v in self.items()})

	# RSET

	def to_set(self) -> RSet:
		res = RSet({
			k: set(v.keys())
			for k, v in self.items()
		})
		return res

	def vertices(self) -> set[Vertix]: # type: ignore
		return self.to_set().vertices()
	
	# OTHERS

	def contract_forwarders(self, merge_attribs: Callable[[TV, TV, TV | None], TV]) -> RDict:
		"""
		Removes forwarding vertices (and their edges).
		A forwarding vertix only has two neighbors (either directed or undirected).
		Both neighbors become connected (directed / undirected) by combining the attribute pairs on the
		way through the removed forwarding vertix.

		R is interpreted as edge, the attribute of R(x, y) the edge costs.

		The merge function's gets the attribute of the removed edges as first two parameters.
		If the neighbor were already connected before, the third parameter is its attribute
		(otherwise None).

		Returns all remaining vertices (and adds empty value dict if necessary.)
		"""
		res = self.copy()
		adj_out = self.to_set()
		vertices = adj_out.vertices()
		adj_in = adj_out.reverse()
		def contract(cfro, cp, ct):
			adj_out[cfro].discard(cp)
			adj_in[cp].discard(cfro)
			adj_out[cp].discard(ct)
			adj_in[ct].discard(cp)
			prior = res[cfro][ct] if ct in res[cfro] else None
			res[cfro][ct] = merge_attribs(res[cfro][cp], res[cp][ct], prior)
			adj_out[cfro].add(ct)
			adj_in[ct].add(cfro)
			del res[cfro][cp]
		for p in frozenset(vertices):
			if len(adj_in[p]) == 1 and len(adj_out[p]) == 1 and adj_in[p] != adj_out[p]:
				contract(adj_in[p].pop(), p, adj_out[p].pop())
				del res[p]
				vertices.remove(p)
			else:
				if len(adj_in[p]) == 2 and adj_in[p] == adj_out[p]:
					ns = list(adj_in[p])
					contract(ns[0], p, ns[1])
					contract(ns[1], p, ns[0])
					del res[p]
					vertices.remove(p)
		return res | vertices

	def reverse(self) -> RDict:
		"""
		Swaps FROM and TO: R(x, y) to R(y, x) while maintaining attributation.

		Maintains all known vertices (and adds empty value set if necessary.)

		Useful for switching between 'successors_by' and 'predecessors_by'.
		"""
		return RDict({
			v: {f: td[v] for f, td in self.items() if v in td}
			for v in self.vertices()
		})

	# IMPORT / EXPORT

	@staticmethod
	def from_list(l: list[tuple[Vertix, Vertix, TV]] | list[list[Vertix | TV]]) -> RDict:
		"""
		Converts a list of 3d-tuples or 3e-lists (structure: < FROM , TO , ATTRIB >)
		to a dict (key=from) of dicts (key=to) of value attrib.
		"""
		result = RDict()
		for fro, to, attrib in l:
			result[fro][to] = attrib
		return result
