import os
from datetime import datetime


class TimeRestrictor():
	def __init__(self):
		self.TIME_FORMAT = "%y/%m/%d %H:%M:%S"

		self.config_filepath = os.getenv("HOME") + "/.config/dicum"
		self.close_time = datetime.max
		self.session_start = datetime.now()
		if not os.path.isfile(self.config_filepath):
			with open(self.config_filepath, "w") as file:
				file.write(datetime.now().strftime(self.TIME_FORMAT))

		with open(self.config_filepath, "r") as file:
			restriction_time = file.readline()[:-1]

		try:
			self.close_time = datetime.strptime(restriction_time, self.TIME_FORMAT)
		except ValueError:
			print("Restriction time could not be retrieved from storage.")
			