import glob
import os, sys
from functools import partial

from ContentGenerator import ContentGenerator
from TimeRestrictor import TimeRestrictor
from PyQt5 import QtCore
from PyQt5 import QtWebEngineWidgets
from PyQt5.QtWidgets import QApplication, QPushButton, QMainWindow, QVBoxLayout, QWidget, QGridLayout, QSizePolicy
from PyQt5 import QtWidgets


class MainGameWidget(QWidget):
	def __init__(self, *args, **kwargs):
		super(QWidget, self).__init__(*args, **kwargs)

		self.button_cols = 4
		self.button_rows = 3
		self.generator = ContentGenerator(self.button_cols * self.button_rows)
		self.button_array = [QPushButton("x") for i in range(self.button_cols * self.button_rows)]

		self.button_widget = QWidget(self)
		self.button_widget.setFixedSize(500, 150)
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
		self.view.setHtml('<center style="margin-top:7em">Welcome to Dicum</center>')

		self.setLayout(QVBoxLayout())
		self.layout().addWidget(self.view)
		self.layout().addWidget(self.button_widget)
		self.time_restrictor = TimeRestrictor()

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


class MainWindow(QMainWindow):
	def __init__(self, *args, **kwargs):
		super(MainWindow, self).__init__(*args, **kwargs)

		self.setWindowTitle("Dicum")
		self.menuBar().addMenu("Dicum")
		main_widget = MainGameWidget(self)
		self.setCentralWidget(main_widget)
		self.setGeometry(0, 0, 1500, 1250)

		self.show()


if __name__ == '__main__':
	app = QApplication([])
	app.setStyleSheet(
		"QPushButton { background-color: darkred; color: white } QMainWindow { background-color: black }")

	main_window = MainWindow()
	app.exec()

	# clear temp folder
	files = glob.glob('temp/*')
	for f in files:
		os.remove(f)

	sys.exit()
