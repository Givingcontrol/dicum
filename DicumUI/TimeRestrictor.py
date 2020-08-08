import os
from datetime import datetime


class TimeRestrictor():
	def __init__(self):
		self.TIME_FORMAT = "%y/%m/%d %H:%M:%S"

		self.config_filepath = os.getenv("HOME") + "/.config/dicum"
		self.restriction_endtime = datetime.max
		self.session_start = datetime.now()
		if not os.path.isfile(self.config_filepath):
			with open(self.config_filepath, "w") as file:
				file.write(datetime.now().strftime(self.TIME_FORMAT))

		with open(self.config_filepath, "r") as file:
			restriction_time = file.readline().strip()

		try:
			self.restriction_endtime = datetime.strptime(restriction_time, self.TIME_FORMAT)
		except ValueError:
			print("Restriction time could not be retrieved from storage.")
		
	def get_remaining_time(self):
		return self.restriction_endtime - datetime.now()

	def is_restricted(self):
		return (self.restriction_endtime - datetime.now()).total_seconds() > 0

	def store_restriction_time(self, timestamp):
		with open(self.config_filepath, "r+") as file:
			file.seek(0)
			file.write(timestamp.strftime(self.TIME_FORMAT))
