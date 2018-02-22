from bs4 import UnicodeDammit
from ftfy import fix_encoding, fix_text

f = open('cleandata.xml', 'w', encoding='utf-8')

# clean encoding 
with open('datadump.xml', 'r', encoding='utf-8') as file:
	for line in file:
		line = fix_encoding(line)
		line = fix_text(line)
		line = UnicodeDammit(line)
		f.write(line.unicode_markup)
f.close()
