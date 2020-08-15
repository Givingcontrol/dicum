import os


class Configuration:
	class __Configuration:
		def __init__(self):
			self.LOCK_LIMIT = 2
			self.UNLOCK_LIMIT = 2
			self.TIME_FORMAT = "%y-%m-%d %H:%M:%S"

			if os.name != "posix":
				print("Currently, only linux systems are supported.")
				exit(1)

			self.TEMP_LOCATION = "/tmp/.dicum"
			self.TEMP_IMAGES = os.path.join(self.TEMP_LOCATION, "images")
			self.TEMP_SCRIPTS = os.path.join(self.TEMP_LOCATION, "js")
			self.LOCK_TIME_LOCATION = "/var/dicum/dicum"
			self.HTML_REL_PATH = "file://" + self.TEMP_LOCATION + "/"
			try:
				os.makedirs(self.TEMP_LOCATION)
				os.makedirs(self.TEMP_IMAGES)
				os.makedirs(self.TEMP_SCRIPTS)
			except FileExistsError:
				pass

			if not os.path.isfile(self.LOCK_TIME_LOCATION):
				print("Dicum time file does not exist.")

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
