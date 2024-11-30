# prerequisite: session id saved in file .sessionid

# usage: [YEAR] [DAY]
# - if no arguments are given YEAR and DAY will be defaulted to today

# example: python get_input.py 2022 18

import urllib.error
import urllib.request
import datetime
import html
import re
import sys

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
with open(f'input/{year}/{output_day}.txt', 'w') as f:
	f.write(content)
	f.close()
with open('full.txt', 'w') as f:
	f.write(content)
	f.close()

print('##########################')
print('\n'.join([l if len(l) < 120 else l[:120] + ' ...' for l in content.split('\n')[:5]]))
print('##########################')

print('... getting example input')

req = urllib.request.Request(f'https://adventofcode.com/{year}/day/{day}')
req.add_header('Cookie', f'session={sessionid};')
with urllib.request.urlopen(req) as u:
	page = u.read().decode('utf-8')
ex_sections = re.findall(r'[Ee]xample(.|\n)+?<code>((.|\n)*?)</code>', page)
ex_encoded = ex_sections[0][1].replace('<em>', '').replace('</em>', '').strip()
ex = html.unescape(ex_encoded)

with open(f'input/{year}/{output_day}_ex.txt', 'w') as f:
	f.write(ex)
	f.close()
with open('mini.txt', 'w') as f:
	f.write(ex)
	f.close()

print("Done!")
