# prerequisite: session id saved in file .sessionid

# usage: [YEAR] [DAY]
# - if no arguments are given YEAR and DAY will be defaulted to today

# example: python get_input.py 2022 18

import urllib.error
import urllib.request
import datetime
import html
import re
import os
import sys
from collections import Counter

with open('.sessionid', 'r') as f:
	sessionid = f.read().strip()
	f.close()

today = datetime.date.today()
year = today.year
day = today.day
if len(sys.argv) == 3:
	year = int(sys.argv[1])
	day = int(sys.argv[2])

print(f'... getting full input {year}/{day}')

req = urllib.request.Request(f'https://adventofcode.com/{year}/day/{day}/input')
req.add_header('Cookie', f'session={sessionid};')
try:
	with urllib.request.urlopen(req) as u:
		content = u.read().decode('utf-8').strip()
except urllib.error.HTTPError:
	print('... not yet available!')
	sys.exit(1)

output_day = f'0{day}'[-2:]
input_folder = f'input/{year}'
if not os.path.exists(input_folder):
    os.makedirs(input_folder)

with open(f'{input_folder}/{output_day}.txt', 'w') as f:
	f.write(content)
	f.close()
with open('full.txt', 'w') as f:
	f.write(content)
	f.close()

lines = content.split('\n')
print(f'... {len(lines)} lines')
char_count_items = Counter(''.join(lines)).items()
top_k = 5
top_charcount = dict(sorted(char_count_items, key=lambda t: (-t[1], t[0]))[:top_k])
top_chars = str(top_charcount)
if len(char_count_items) > top_k:
	top_chars = top_chars.replace('}', ', ...: <=' + str(min(top_charcount.values())) + '}')
print(f'... top of {len(char_count_items)} chars: {top_chars}')
print('#' * 90)
print('\n'.join([
	((l if len(l) < 80 else l[:80] + ' ...') + ' ' * 85)[:85]
		+ f'[{idx}]'
	for idx in sorted(list(set(range(min(5, len(lines)))) | {len(lines) - 1}))
	for l in [lines[idx]]
]))
print('#' * 90)

print('... getting example input')

req = urllib.request.Request(f'https://adventofcode.com/{year}/day/{day}')
req.add_header('Cookie', f'session={sessionid};')
with urllib.request.urlopen(req) as u:
	page = u.read().decode('utf-8')
# adding <pre> to ensure real examples (in own paragraph) - avert single "0" (ex. 2024/18)
ex_sections = re.findall(r'[Ee]xample(.|\n)+?<pre>(.|\n)*?<code>((.|\n)*?)</code>', page)
ex_encoded = ex_sections[0][2].replace('<em>', '').replace('</em>', '').strip()
ex = html.unescape(ex_encoded)

input_ex = f'{input_folder}/{output_day}_ex.txt'
if os.path.isfile(input_ex):
	print('... example already exists in input folder - no overwrite')
else:
	with open(input_ex, 'w') as f:
		f.write(ex)
		f.close()
with open('mini.txt', 'w') as f:
	f.write(ex)
	f.close()

print('Done!')
