import os
import re
from datetime import datetime, timedelta, time


class TimeRestrictor():
	def __init__(self):
		self.TIME_FORMAT = "%y/%m/%d %H:%M:%S"
		self.BASE_FORMAT = "%H:%M:%S"

		self.current_restriction_time = timedelta(hours=1)

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

	def store_restriction_time(self, timestamp=None):
		if not timestamp:
			timestamp = datetime.now() + self.current_restriction_time
		with open(self.config_filepath, "r+") as file:
			file.seek(0)
			file.write(timestamp.strftime(self.TIME_FORMAT))

	def update_restriction_time(self, time_string):
		delta = self.parse_time(time_string)
		self.current_restriction_time += delta
		return self.current_restriction_time

	@staticmethod
	def parse_time(time_string):
		time_delta = timedelta()
		try:
			time_delta = timedelta(hours=int(time_string))
		except ValueError:
			print("Time string could not be parsed to integer (hours):", time_string)
		return time_delta
