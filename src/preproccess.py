import re


'''
Brief:
	Remove invalid pairs (whose have tags equal to '-NONE-', '-LRB-' or '-RRB-') from sentence.
Params:
	data: A list of pairs "(<TAG>, <WORD>)".
Return:
	The data without invalid pairs.
'''
def cleanData(data):
	i = 0

	while i < len(data):
		if re.match('-NONE-|-LRB-|-RRB-', data[i][0]):
			del data[i]
		else:			
			i = i+1


	data = [ x for x in data if not re.match('-NONE-|-LRB-|-RRB-', x[0])]

'''
Brief:
	Convert words to lowercase.
Params:
	data: A list of pairs "(<TAG>, <WORD>)".
Return:
	The data with only lowercase words.
'''
def caseFolding(data):
	for i in range(len(data)):
		data[i] = (data[i][0], data[i][1].lower())

def normalization(data):
	for i in range(len(data)):
		# map ordinal numbers to 1st
		data[i] = (data[i][0], re.sub('[0-9]+(st|nd|th)', '1st', data[i][1]))

		# map numbers to 1
		data[i] = (data[i][0], re.sub('[0-9]+((\.|,)[0-9]+)*', '1', data[i][1]))