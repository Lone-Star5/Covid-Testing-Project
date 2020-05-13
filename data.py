from operator import itemgetter

data = [
			{'com' : 10},
			{'com' : 7},
			{'com' : 12},
			{'com' : 15},
			{'com' : 6} 

		]
temp  = sorted(data, key=itemgetter('com'))
temp.reverse()
print(temp)