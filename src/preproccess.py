import re

def cleanData(data):
	# Remove all pair who has tag equal to '-NONE-' or '-LRB-' or '-RRB-'
	data = [ x for x in data if not re.match('-NONE-|-LRB-|-RRB-', x[0])]

	# JUST FOR TESTS
	# return tags
	return list(dict.fromkeys([ x[0] for x in data ]))