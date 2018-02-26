from ftfy import fix_encoding
import re

list = open('nationalities-data.txt', 'r', encoding='utf-8').readlines()
newList = []
for string in list:
	string = string.lstrip(' ')
	string = string.rstrip(' ')
	string = string.lstrip('\t')
	string = string.rstrip('\n')
	string = re.sub(r'ers$', '', string)
	string = re.sub(r's$', '', string)
	if string != '':
		newList.append(string)
list = newList

with open('all-nationalities.txt', 'w', encoding='utf-8') as file:
	for nationality in list:
		nationality = fix_encoding(nationality)
		file.write(nationality + '\n')