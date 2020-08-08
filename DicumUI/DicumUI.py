import glob
import os
import sys
import time
import _thread, threading
from functools import partial

from ContentGenerator import ContentGenerator
from TimeRestrictor import TimeRestrictor
from PyQt5 import QtCore
from PyQt5 import QtWebEngineWidgets
from PyQt5.QtWidgets import QApplication, QPushButton, QMainWindow, QVBoxLayout, QWidget, QGridLayout, QHBoxLayout, \
	QSpacerItem, QSizePolicy
from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimer


class MainGameWidget(QWidget):
	def __init__(self, *args, **kwargs):
		super(QWidget, self).__init__(*args, **kwargs)

		self.button_cols = 4
		self.button_rows = 3
		self.generator = ContentGenerator(self.button_cols * self.button_rows)
		self.button_array = [QPushButton("x") for i in range(self.button_cols * self.button_rows)]

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
		self.time_restrictor = TimeRestrictor()

		self.update_welcome()
		if self.time_restrictor.is_restricted():
			timer = QTimer(self)
			timer.setInterval(1000)
			timer.timeout.connect(self.update_welcome, timer)
			timer.start()

	def get_content(self, pos):
		self.button_array[pos].setEnabled(False)

		content_item = self.generator.get_next()
		if not content_item:
			return
		kind, content = content_item

		if kind == "url":
			self.view.load(QtCore.QUrl(content))
		elif kind == "num":
			self.view.setHtml(content)
		else:
			print("content kind was not recognized:", kind, content)

	def update_welcome(self, timer=None):
		if self.time_restrictor.is_restricted():
			self.view.setHtml(self.generator.get_restricted(self.time_restrictor.get_remaining_time()))
		else:
			self.view.setHtml(self.generator.get_unrestricted())
			if timer:
				timer.stop()


class MainWindow(QMainWindow):
	def __init__(self, *args, **kwargs):
		super(MainWindow, self).__init__(*args, **kwargs)

		self.setWindowTitle("Dicum")
		self.menuBar().addMenu("Dicum")
		main_widget = MainGameWidget(self)
		self.setCentralWidget(main_widget)
		self.setGeometry(0, 0, 1500, 1250)

		self.show()


def run():
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


if __name__ == '__main__':
	run()
