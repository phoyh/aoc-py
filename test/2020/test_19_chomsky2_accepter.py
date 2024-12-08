import re
import itertools as it
import lark
from api import file

def get_rules_and_words(suffix = ''):
	rules_raw, words = file.segments(f'2020/19{suffix}')
	rules_w_options = {}
	rules_w_lit = {}
	for rule_raw in rules_raw:
		rule_id, rest = rule_raw.split(': ')
		if '"' in rest:
			rules_w_lit[rule_id] = re.findall(r'"(\w*)"', rest)[0]
		else:
			rules_w_options[rule_id] = [o.split(' ') for o in rest.split(' | ')]
	return (rules_w_options, rules_w_lit), words

def get_lang(rules, rule_id) -> list[str]:
	rules_w_options, rules_w_lit = rules
	if rule_id in rules_w_lit:
		return [rules_w_lit[rule_id]]
	return [
		''.join(sub_word_tuple)
		for o in rules_w_options[rule_id]
		for sub_word_tuple in it.product(*(get_lang(rules, id) for id in o))
	]

def test_first():
	rules, words = get_rules_and_words('_ex')
	lang_0 = get_lang(rules, '0')
	assert 2 == sum(l in lang_0 for l in words)

########### with Lark as C2 parser ##############

def rule_id_to_alpha(rule_id):
	"""
	Lark wants nonterminal names to be lowercase letters.
	"""
	return 'start' if rule_id == '0' else ''.join(chr(int(r) + 97) for r in rule_id)

def get_parser(rules):
	rules_w_options, rules_w_lit = rules
	nonterminal_grammar = '\n'.join(
		f'{rule_id_to_alpha(rule_id)}: {" | ".join(
			" ".join(rule_id_to_alpha(i) for i in o) for o in options
		)}'
		for rule_id, options in rules_w_options.items()
	)
	terminal_grammar = '\n'.join(
		f'{rule_id_to_alpha(rule_id)}: "{lit}"'
		for rule_id, lit in rules_w_lit.items()
	)
	return lark.Lark(nonterminal_grammar + '\n\n' + terminal_grammar)

def is_valid(parser: lark.Lark, word):
	try:
		parser.parse(word)
		return True
	except lark.exceptions.LarkError:
		return False

#def test_first_c2_parser():
def do_not_execute_test_first_c2_parser():
	rules, words = get_rules_and_words()
	parser = get_parser(rules)
	assert 250 == sum(is_valid(parser, l) for l in words)

#def test_second_c2_parser():
def do_not_execute_test_second_c2_parser():
	rules, words = get_rules_and_words()
	rules_w_options, _ = rules
	rules_w_options['8'] = [['42'], ['42', '8']]
	rules_w_options['11'] = [['42', '31'], ['42', '11', '31']]
	parser = get_parser(rules)
	assert 359 == sum(is_valid(parser, l) for l in words)
