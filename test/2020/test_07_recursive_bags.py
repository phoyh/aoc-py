import re
from api import file, RDict

def line_parse(line: str):
	holder, holding = line.split(' bags contain ')
	holding_bags = {
		bag: int(num_str)
		for num_str, bag in re.findall(r'(\d+) (\w+ \w+) bag', holding)
	}
	return holder, holding_bags

def get_bag_count_by_holder():
	return RDict(file.lines('2020/07', line_parse))

def held_bags_count(bag_count_by_holder, bag):
	return sum(
		count + count * held_bags_count(bag_count_by_holder, inner)
		for inner, count in bag_count_by_holder[bag].items()
	)

def test_first():
	bag_count_by_holder = get_bag_count_by_holder()
	holders_by_bag = bag_count_by_holder.to_set().reverse()
	todo = ['shiny gold']
	seen = set()
	while todo:
		bag = todo.pop()
		if bag not in seen:
			seen.add(bag)
			for holder in holders_by_bag[bag]:
				todo.append(holder)
	assert 151 == len(seen) - 1

def test_second():
	assert 41559 == held_bags_count(get_bag_count_by_holder(), 'shiny gold')