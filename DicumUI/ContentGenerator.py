import csv
import random


class ContentGenerator:
	def __init__(self, size):
		self.commands = ContentGenerator.__get_commands(size)
		print(len(self.commands))

	def get_next(self):
		try:
			return self.commands.pop()
		except IndexError:
			print("get_next failed, no more elements to pop")
			return None

	@staticmethod
	def __get_html_base_front():
		with open("resources/html_front.html") as html_template:
			html_base = "".join(html_template.readlines())
		return html_base

	@staticmethod
	def __get_html_image(path):
		return path + '<br/><img src="../' + path + '" />'

	@staticmethod
	def __get_html_back():
		with open("resources/html_back.html") as html_template:
			html_back = "".join(html_template.readlines())
		return html_back

	@staticmethod
	def __interpret_command(command):
		text, kind, time = command
		if kind == "img":
			current_file_name = text.replace("/", "")
			with open("temp/" + current_file_name + ".html", "w") as html_temp_file:
				html_temp_file.write(ContentGenerator.__get_html_base_front() + ContentGenerator.__get_html_image(
					text) + ContentGenerator.__get_html_back())
			return "url", "file:///home/jonas/Projects/dicum/temp/" + current_file_name + ".html"
		elif kind == "url":
			return "url", text
		else:
			print("Command kind could not be interpreted:", kind, "Full:", command)

	@staticmethod
	def __get_commands(size):
		commands = [("num", str(i)) for i in range(size)]
		with open("resources/commands.csv") as csv_file:
			reader = csv.reader(csv_file, delimiter=",")
			for i, row in enumerate(reader):
				if i < len(commands):
					commands[i] = ContentGenerator.__interpret_command(row)

		random.shuffle(commands)
		return commands

# TODO 5 min viewing time for web page
# TODO Chose 3 of 5 Cards with Pictures (Cens/NoCens)
