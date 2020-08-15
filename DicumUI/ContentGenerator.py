import csv
import random
import os
from shutil import copy2

from jinja2 import Environment, FileSystemLoader

from Configuration import Configuration


class ContentGenerator:
	def __init__(self, commands_filename):
		resource_dir = "resources"
		self.env = Environment(loader=FileSystemLoader(resource_dir))
		self.commands = self.__get_commands(os.path.join(commands_filename))

	def get_size(self):
		return len(self.commands)

	def get_next(self):
		try:
			return self.commands.pop()
		except IndexError:
			print("get_next failed, no more elements to pop")
			return None

	def get_restricted(self, timedelta):
		time_string = str(timedelta).split(".")[0]
		template = self.env.get_template("templates/restricted.html")
		return template.render(restricted_time=time_string, background_image="bg03.png")

	def get_unrestricted(self):
		template = self.env.get_template("templates/unrestricted.html")
		return template.render(background_image="bg03.png")

	def get_current_restriction(self, restriction_time):
		time_string = str(restriction_time).split(":")[0] + " hours"
		template = self.env.get_template("templates/restriction_time.html")
		return template.render(current_restriction_time=time_string, background_image="bg03.png")

	@staticmethod
	def __interpret_command(command):
		template_dir = "resources"
		env = Environment(loader=FileSystemLoader(template_dir))
		template = env.get_template("templates/plain_image.html")

		kind, content, time = command
		if kind == "img":
			img_file_name = content.strip()
			if not os.path.isfile(os.path.join(Configuration().TEMP_IMAGES, img_file_name)):
				try:
					copy2("resources/images/" + img_file_name, Configuration().TEMP_IMAGES + "/")
				except FileNotFoundError:
					print("Image file could not be found:", img_file_name)
			img_file_path = os.path.join(Configuration().TEMP_IMAGES, img_file_name)
			html_file_name = img_file_name.split(".")[0]
			html_file_path = os.path.join(Configuration().TEMP_LOCATION, html_file_name + ".html")
			with open(html_file_path, "w") as html_temp_file:
				html_temp_file.write(template.render(image_filename=img_file_path))
			return "url", "file://" + os.path.join(Configuration().TEMP_LOCATION, html_file_name + ".html"), time
		else:
			return command

	@staticmethod
	def __create_temp_html():
		pass

	@staticmethod
	def __get_commands(commands_filename):
		commands = []
		with open(commands_filename) as csv_file:
			reader = csv.reader(csv_file, delimiter=",")
			for row in reader:
				commands.append(ContentGenerator.__interpret_command(row))

		random.shuffle(commands)
		return commands

# TODO 5 min viewing time for web page
# TODO Chose 3 of 5 Cards with Pictures (Cens/NoCens)
