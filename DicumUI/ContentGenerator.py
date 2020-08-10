import csv
import random

from jinja2 import Environment, FileSystemLoader


class ContentGenerator:
	def __init__(self, size):
		self.commands = ContentGenerator.__get_commands(size)
		template_dir = "resources"
		self.env = Environment(loader=FileSystemLoader(template_dir))

	def get_next(self):
		try:
			return self.commands.pop()
		except IndexError:
			print("get_next failed, no more elements to pop")
			return None

	def get_restricted(self, timedelta):
		time_string = str(timedelta).split(".")[0]
		template = self.env.get_template("restricted.html")
		return template.render(restricted_time=time_string)

	def get_unrestricted(self):
		template = self.env.get_template("unrestricted.html")
		return template.render()

	def get_current_restriction(self, restriction_time):
		time_string = str(restriction_time).split(".")[0]
		template = self.env.get_template("restriction_time.html")
		return template.render(current_restriction_time=time_string)

	@staticmethod
	def __interpret_command(command):
		template_dir = "resources"
		env = Environment(loader=FileSystemLoader(template_dir))
		template = env.get_template("plain_image.html")

		kind, content, time = command
		if kind == "img":
			image_file_name = content.replace("/", "")
			html_file_name = image_file_name.split(".")[0]
			with open("temp/" + html_file_name + ".html", "w") as html_temp_file:
				html_temp_file.write(template.render(image_filename=content))
			return "url", "file:///home/jonas/Projects/dicum/temp/" + html_file_name + ".html", time
		else:
			return command

	@staticmethod
	def __get_commands(size):
		commands = [("num", str(i)) for i in range(size)]
		with open("resources/commands2.csv") as csv_file:
			reader = csv.reader(csv_file, delimiter=",")
			for i, row in enumerate(reader):
				if i < len(commands):
					commands[i] = ContentGenerator.__interpret_command(row)

		random.shuffle(commands)
		return commands

# TODO 5 min viewing time for web page
# TODO Chose 3 of 5 Cards with Pictures (Cens/NoCens)
