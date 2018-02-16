# pip install ftfy
from ftfy import fix_encoding

f = open('cleandata.xml', 'w', encoding='utf-8')

# clean encoding
with open('datadump.xml', 'r', encoding='utf-8') as file:
	for line in file:
		line = fix_encoding(line)
		f.write(line)
f.close()
