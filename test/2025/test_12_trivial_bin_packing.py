from api import file, parse, PDict

def test_first():
	*lines_by_present, regionlines = file.segments('2025/12')
	presents = [
		PDict.from_lines(lines[1:]).by_value('#')
		for lines in lines_by_present
	]
	present_hashes_width_height = [
		(len(p), width, height)
		for p in presents
		for width, height in [p.size_by_dim()]
	]
	present_max_width = max(w for _, w, _ in present_hashes_width_height)
	present_max_height = max(h for _, _, h in present_hashes_width_height)
	result = 0
	for l in regionlines:
		height, width, *present_counts = parse.ints(l)
		hashes_and_sizes = [
			(c * hc, c * w * h)
			for c, (hc, w, h) in zip(present_counts, present_hashes_width_height)
		]
		hash_count = sum(hc for hc, _ in hashes_and_sizes)
		total_size = sum(s for _, s in hashes_and_sizes)
		if hash_count > height * width:
			# impossible: not enough space for all the hashes to be placed
			...
		else:
			if total_size <= (width - width % present_max_width) \
					* (height - height % present_max_height):
				# trivial packing possible by putting presents as non-overlapping tiles
				result += 1
			else:
				# we'd need a NP solution here - must not enter here,
				# as this would render the solution a mere guess
				assert False
	assert 546 == result
