import os
import tempfile
import logging


class Configuration:
	class __Configuration:
		def __init__(self, commands_file=None):
			self.LOCK_LIMIT = 2
			self.UNLOCK_LIMIT = 2

			self.HOME = os.getenv('HOME')
			self.CONFIG = os.path.join(self.HOME, ".config", "dicum");
			if not os.path.isdir(self.CONFIG):
				os.makedirs(self.CONFIG)

			if not commands_file:
				commands_file = "game.csv"
			self.COMMANDS = os.path.join(self.CONFIG, commands_file)
			if not os.path.isfile(self.COMMANDS):
				logging.critical("Commands not found.")
				exit(404)

			self.LOCK_TIME_LOCATION = os.path.join(self.CONFIG, "time")
			if not os.path.isfile(self.LOCK_TIME_LOCATION):
				with open(self.LOCK_TIME_LOCATION, "w+"):
					pass

			self.GAME_CONFIG = os.path.join(self.CONFIG, "game.csv")
			if not os.path.isfile(self.GAME_CONFIG):
				with open(self.GAME_CONFIG, "w+"):
					pass

			self.RESOURCES = os.path.join(self.CONFIG, "resources")
			if not os.path.isdir(self.RESOURCES):
				os.makedirs(self.RESOURCES)

			with tempfile.TemporaryDirectory() as temp_dir:
				self.TEMP_LOCATION = temp_dir
				logging.info('created temporary directory', temp_dir)

			self.TEMP_IMAGES = os.path.join(self.TEMP_LOCATION, "images")
			self.TEMP_SCRIPTS = os.path.join(self.TEMP_LOCATION, "js")
			self.HTML_REL_PATH = "file://" + self.TEMP_LOCATION + "/"
			self.BG_IMAGE = "images/bg03.png"
			try:
				os.makedirs(self.TEMP_LOCATION)
				os.makedirs(self.TEMP_IMAGES)
				os.makedirs(self.TEMP_SCRIPTS)
			except FileExistsError:
				pass

			if not os.path.isfile(self.LOCK_TIME_LOCATION):
				logging.critical("Dicum time file does not exist.")

		def __str__(self):
			return repr(self) + self.val

	instance = None

	def __init__(self):
		if not Configuration.instance:
			Configuration.instance = Configuration.__Configuration()
		else:
			Configuration.instance

	def __getattr__(self, name):
		return getattr(self.instance, name)
