DAY = '../full'
#DAY = '../mini'

# pylint: disable=unused-import,wrong-import-position,multiple-imports,line-too-long
import functools as ft, itertools as it, operator as op
import heapq, math, re, sys
#import igraph as ig, networkx as nx, numpy as np, z3
from collections import Counter, defaultdict, deque
from api import Cube, CubeSet, file, graph, io, parse, P, PSet, PDict, RDict, RSet, search, xmath, z3result
N, S, W, E = NSWE = P.NSWE()
NW = N + W
NE = N + E
SW = S + W
SE = S + E
O = P.O()

########### HERE ##############

def line_parse(line: str):
	#return [int(e) for e in re.findall(r'\d', line)]
	#return [e for e in re.findall(r'\w+', line)]
	return line

result = 0
#inp = file.readall(DAY)
#segs = file.segments(DAY, line_parse)
lines = file.lines(DAY, line_parse)
#lines = file.lines(DAY, parse.uints)
#lines = file.lines(DAY, parse.ints)
#g = PDict.from_lines(lines)
#numbers = file.lines(DAY, int)
#for lines in segs:
#for n in nums:
#for i, l in enumerate(lines):
	#result += 1

io.print_clip(result)
#sys.exit()

#line = '24-71 J: James\n0-2 B: Brat'
#tuple_matches = re.findall(r'(\d+)-(\d+) (\w): (\w+)', line):
#for match in re.finditer(r'(\d+)-(\d+) (\w): (\w+)', line):
#	lo, hi, ch, word = match.groups()

#g = PDict.from_lines(lines)
#cost, path = graph.dijkstra(
#	start=P.O(),
#	end=P.NSWE()[0],
#	neighbors=lambda p: p.neighbors(diag=False, within=g),
#	edge_cost=lambda a, b: 1
#)
