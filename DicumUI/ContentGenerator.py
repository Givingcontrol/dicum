import csv
import random


class ContentGenerator:
	def __init__(self, size):
		self.commands = ContentGenerator.get_commands(size)

	def get_next(self):
		try:
			return self.commands.pop()
		except IndexError:
			print("get_next failed, no more elements to pop")
			return -1

	@staticmethod
	def get_html_base_front():
		html_template = open("resources/html_front.html")
		html_base = "".join(html_template.readlines())
		html_template.close()
		return html_base

	@staticmethod
	def get_html_image(path):
		return path + '<br/><img src="../' + path + '" />'

	@staticmethod
	def get_html_back():
		html_template = open("resources/html_back.html")
		html_back = "".join(html_template.readlines())
		html_template.close()
		return html_back

	@staticmethod
	def interpret_command(command):
		text, kind, time = command
		if kind == "img":
			current_file_name = text.replace("/", "")
			with open("temp/" + current_file_name + ".html", "w") as html_temp_file:
				html_temp_file.write(ContentGenerator.get_html_base_front() + ContentGenerator.get_html_image(
					text) + ContentGenerator.get_html_back())
			return "url", "file:///home/jonas/Projects/dicum/temp/" + current_file_name + ".html"
			return "html", ContentGenerator.get_html_base_front() + ContentGenerator.get_html_image(
				text) + ContentGenerator.get_html_back()
		elif kind == "url":
			return "url", text
		else:
			print("Command kind could not be interpreted:", kind, "Full:", command)

	@staticmethod
	def get_commands(size):
		commands = [("num", str(i)) for i in range(size)]
		with open("resources/commands.csv") as csvfile:
			reader = csv.reader(csvfile, delimiter=",")
			for i, row in enumerate(reader):
				if i < len(commands):
					commands[i] = ContentGenerator.interpret_command(row)

		# TODO is this shuffled in the same way all the time?
		random.shuffle(commands)
		print(commands)
		return commands

# TODO 5 min viewing time for web page
# TODO Chose 3 of 5 Cards with Pictures (Cens/NoCens)
