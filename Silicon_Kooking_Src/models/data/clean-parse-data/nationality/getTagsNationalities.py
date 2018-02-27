from ftfy import fix_encoding
import re

list = open('all-nationalities-added.txt', 'r', encoding='utf-8').readlines()
tags = open('tags.txt', 'r', encoding='utf-8').readlines()
ingredients = open('ingredients.txt', 'r', encoding='utf-8').readlines()

found = []
newList = [] 
i = 0

list = [item.lower() for item in list]
tags = [item.lower() for item in tags]
remove = []

# find nationalities in tags
for item in tags:
	temp = item
	temp = temp.strip('\n')
	temp = temp.strip()
	for nationality in list:
		nationality = nationality.strip('\n')
		nationality = nationality.strip()
		if re.match(nationality, temp) != None:
			if nationality not in found:
				remove.append(item)
				found.append(nationality)
				i = i + 1
			else:
				remove.append(item)


print('items in tags before removing national dishes ', len(tags))
print('# of unique-nationalities: ', i)

with open('found-nationalities.txt', 'w', encoding='utf-8') as file:
	for nationality in found:
		nationality = fix_encoding(nationality + '\n')
		file.write(nationality)
		
# remove nationalities
for item in remove:
	if item in tags:
		tags.remove(item)

print('items in tags after removing national dishes', len(tags))

# remove ingredients in tags
tags.sort()
ingredients.sort()
for item in tags:
	temp = item
	temp = temp.strip('\n')
	temp = temp.strip()
	for ing in ingredients:
		ing = ing.strip('\n')
		ing = ing.strip()
		if re.match(re.escape(ing), temp) != None:
			if item in tags:
				tags.remove(item)
			break
		
print('items in tags after removing ingredients', len(tags))

with open('left-over.txt', 'w', encoding='utf-8') as file:
	for item in tags:
		item = fix_encoding(item)
		file.write(item)