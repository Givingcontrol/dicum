from functools import partial

from ContentGenerator import ContentGenerator
from PyQt5 import QtCore
from PyQt5 import QtWebEngineWidgets
from PyQt5.QtWidgets import QApplication, QPushButton, QMainWindow, QVBoxLayout, QWidget, QGridLayout


class ButtonWidget(QWidget):
	def __init__(self, *args, **kwargs):
		super(QWidget, self).__init__(*args, **kwargs)

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
		# view.load(QtCore.QUrl().fromLocalFile("/home/jonas/Projects/dicum/resources/test.html"))
		# view.load(QtCore.QUrl().fromLocalFile("/home/jonas/Projects/resources/chick.jpeg"))
		self.view.setHtml("Welcome to Dicum")
		# view.load(QtCore.QUrl("https://google.com"))
		layout.addWidget(self.view)
		layout.addWidget(self.button_widget)
		self.setLayout(layout)

	def get_content(self, pos):
		kind = ""
		content = ""
		try:
			self.button_array[pos].setEnabled(False)
			kind, content = self.generator.get_next()
		except IndexError:
			print("Array position", pos, "is out of range")

		print(content)
		if kind == "html" or kind == "num":
			self.view.setHtml(content)
		elif kind == "url":
			self.view.load(QtCore.QUrl(content))
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

	main_window = MainWindow()
	main_window.show()

	app.exec()
