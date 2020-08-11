import glob
import os
import sys
from functools import partial
from datetime import datetime

from PyQt5 import QtCore
from PyQt5 import QtWebEngineWidgets
from PyQt5.QtWidgets import QApplication, QPushButton, QMainWindow, QVBoxLayout, QWidget, QGridLayout, QHBoxLayout, \
	QSpacerItem, QSizePolicy
from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimer

from ContentGenerator import ContentGenerator
from TimeRestrictor import TimeRestrictor


class StyledPushButton(QPushButton):
	def __init__(self, *args, **kwargs):
		super(QPushButton, self).__init__(*args, **kwargs)
		self.setStyleSheet(":enabled { color: white; background-color: darkred } :disabled { color: #222222 }")


class Configuration():
	def __init__(self):
		self.lock_limit = 3
		self.unlock_limit = 3


class MainGameWidget(QWidget):
	def __init__(self, commands_file):
		super(QWidget, self).__init__()
		self.commands_file = commands_file  # store filename for reset

		self.__reset()

		self.button_array = [StyledPushButton("x") for i in range(self.generator.get_size())]

		self.__setup_ui()

		self.__run_ui()

	def __run_ui(self):
		self.update_welcome()
		if self.time_restrictor.is_restricted():
			timer = QTimer(self)
			timer.setInterval(1000)
			timer.timeout.connect(lambda: self.update_welcome(timer))
			timer.start()

	def __reset(self):
		self.lock_counter = 0
		self.unlock_counter = 0
		self.config = Configuration()
		self.time_restrictor = TimeRestrictor()
		self.generator = ContentGenerator(self.commands_file)

	def __setup_ui(self):
		# calculate button row and column length based on number of commands
		self.button_rows = self.isqrt(self.generator.get_size())
		self.button_cols = self.button_rows if self.button_rows * (
				self.button_rows + 1) > self.generator.get_size() else self.button_rows + 1

		self.button_widget = QWidget(self)
		self.button_widget.setFixedSize(500, 130)
		self.button_widget.setLayout(QGridLayout())
		for row in range(self.button_rows):
			for col in range(self.button_cols):
				pos = row * self.button_cols + col
				self.button_widget.layout().addWidget(self.button_array[pos], row, col)
				self.button_array[pos].clicked.connect(partial(self.get_content, pos))

		self.button_widget.setSizePolicy(
			QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding))

		# Setting up the view
		self.view = QtWebEngineWidgets.QWebEngineView()

		self.base_widget = QWidget(self)
		self.base_widget.setLayout(QHBoxLayout())
		self.base_widget.setGeometry(0, 0, 0, 130)
		self.base_widget.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Fixed)
		self.base_widget.layout().addItem(QSpacerItem(10, 1, QSizePolicy.Ignored, QSizePolicy.Preferred))
		self.base_widget.layout().addWidget(self.button_widget)
		self.base_widget.layout().addItem(QSpacerItem(10, 1, QSizePolicy.Ignored, QSizePolicy.Preferred))

		self.setLayout(QVBoxLayout())
		self.layout().addWidget(self.view)
		self.layout().addWidget(self.base_widget)

	def get_content(self, pos):
		self.button_array[pos].setEnabled(False)

		content_item = self.generator.get_next()
		if not content_item:
			return
		kind, content, time = content_item

		if kind == "url":
			self.view.load(QtCore.QUrl(content))
		elif kind == "num":
			current_restriction_time = self.time_restrictor.update_restriction_time(content)
			self.view.setHtml(self.generator.get_current_restriction(current_restriction_time))
		elif kind == "lock":
			if content == "lock":
				self.lock_counter += 1
				if self.lock_counter >= self.config.lock_limit:
					self.start_restriction()
			elif content == "unlock":
				self.unlock_counter += 1
				if self.unlock_counter >= self.config.unlock_limit:
					self.stop_restriction()
			else:
				print("lock value invalid, ignoring")
		else:
			print("content kind was not recognized:", kind, content)

	def update_welcome(self, timer=None):
		if self.time_restrictor.is_restricted():
			self.view.setHtml(self.generator.get_restricted(self.time_restrictor.get_remaining_time()))
			self.deactivate_buttons()
		else:
			self.view.setHtml(self.generator.get_unrestricted())
			self.activate_buttons()
			if timer:
				timer.stop()

	def start_restriction(self):
		print("Start Restriction")
		self.time_restrictor.store_restriction_time()
		self.__reset()
		self.__run_ui()

	def stop_restriction(self):
		print("Stop Restriction")
		self.time_restrictor.store_restriction_time(datetime.now())
		self.__reset()
		self.__run_ui()

	def activate_buttons(self):
		for button_number in range(self.button_widget.layout().count()):
			try:
				self.button_widget.layout().itemAt(button_number).widget().setEnabled(True)
			except AttributeError:
				print("Non-button element in button widget, could not be disabled.")

	def deactivate_buttons(self):
		for button_number in range(self.button_widget.layout().count()):
			try:
				self.button_widget.layout().itemAt(button_number).widget().setEnabled(False)
			except AttributeError:
				print("Non-button element in button widget, could not be disabled.")

	@staticmethod
	def isqrt(n):
		x = n
		y = (x + 1) // 2
		while y < x:
			x = y
			y = (x + n // x) // 2
		return x


class MainWindow(QMainWindow):
	def __init__(self, *args, **kwargs):
		super(MainWindow, self).__init__(*args, **kwargs)

		self.setWindowTitle("Dicum")
		self.menuBar().addMenu("Dicum")
		main_widget = MainGameWidget(sys.argv[1])
		self.setCentralWidget(main_widget)
		self.setGeometry(0, 0, 1500, 1250)

		self.show()


if __name__ == '__main__':
	app = QApplication([])
	app.setStyleSheet(
		"QPushButton { background-color: darkred; color: black } QMainWindow { background-color: black }")
	main_window = MainWindow()
	app.exec()

	# clear temp folder
	files = glob.glob('temp/*')
	for f in files:
		os.remove(f)
	sys.exit(0)
