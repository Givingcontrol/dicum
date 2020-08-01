import glob
import os
from functools import partial

from ContentGenerator import ContentGenerator
from PyQt5 import QtCore
from PyQt5 import QtWebEngineWidgets
from PyQt5.QtWidgets import QApplication, QPushButton, QMainWindow, QVBoxLayout, QWidget, QGridLayout


class ButtonWidget(QWidget):
	def __init__(self, *args, **kwargs):
		super(QWidget, self).__init__(*args, **kwargs)

		reset = QPushButton("Restart")

		self.button_cols = 4
		self.button_rows = 3
		self.generator = ContentGenerator(self.button_cols * self.button_rows)
		self.button_array = [QPushButton("x") for i in range(self.button_cols * self.button_rows)]

		self.button_widget = QWidget(self)
		button_layout = QGridLayout()
		for row in range(self.button_rows):
			for col in range(self.button_cols):
				pos = row * self.button_cols + col
				button_layout.addWidget(self.button_array[pos], row, col)
				self.button_array[pos].clicked.connect(partial(self.get_content, pos))

		self.button_widget.setLayout(button_layout)

		layout = QVBoxLayout()

		self.view = QtWebEngineWidgets.QWebEngineView()
		self.view.setHtml("Welcome to Dicum")

		layout.addWidget(self.view)
		layout.addWidget(self.button_widget)
		self.setLayout(layout)

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


@staticmethod
def print_hello():
	print("Hello World")


class MainWindow(QMainWindow):
	def __init__(self, *args, **kwargs):
		super(MainWindow, self).__init__(*args, **kwargs)

		self.setWindowTitle("Dicum")
		main_widget = ButtonWidget(self)
		self.setCentralWidget(main_widget)


if __name__ == '__main__':
	app = QApplication([])
	app.setStyleSheet("QPushButton { background-color: blue }")

	main_window = MainWindow()
	main_window.show()

	app.exec()

	# clear temp folder
	files = glob.glob('temp/*')
	for f in files:
		os.remove(f)
