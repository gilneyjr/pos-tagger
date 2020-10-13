class Bigram:

	def train(self, setences):
		for setence in setences:
			last_tag = 'BEGIN'
			for tag, word in setence:
				pass
				# contar quantas vezes word foi antecedida da tag anterior
