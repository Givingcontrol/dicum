import random


class ContentGenerator:
	def __init__(self, size):
		self.content = [i for i in range(size)]
		file = open("resources/commands.txt", "r")
		lines = file.readlines()
		file.close()
		for i, x in enumerate(lines):
			if i < len(self.content):
				self.content[i] = x
		random.shuffle(self.content)

	def get_next(self):
		try:
			return self.content.pop()
		except:
			return -1



# TODO 5 min viewing time for web page
# TODO Chose 3 of 5 Cards with Pictures (Cens/NoCens)