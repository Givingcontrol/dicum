from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QMainWindow, QVBoxLayout, QWidget, QGridLayout
from PyQt5.QtGui import QPixmap
from PyQt5 import QtWebEngineWidgets
from PyQt5 import QtCore
from ContentGenerator import ContentGenerator
from threading import Timer
from functools import partial


class ButtonWidget(QWidget):
	def __init__(self, *args, **kwargs):
		super(QWidget, self).__init__(*args, **kwargs)

		self.generator = ContentGenerator(12)

		button_cols = 4
		button_rows = 3
		self.button_array = [QPushButton("x") for i in range(button_cols * button_rows)]

		self.button_widget = QWidget(self)
		button_layout = QGridLayout()
		for row in range(button_rows):
			for col in range(button_cols):
				pos = row * button_cols + col
				button_layout.addWidget(self.button_array[pos], row, col)
				self.button_array[pos].clicked.connect(partial(self.get_content, pos))
		self.button_widget.setLayout(button_layout)

		self.label = QLabel("-1")

		layout = QVBoxLayout()

		# add image view
		# frame = QPixmap("resources/chick.jpeg")
		# image_label = QLabel(self)
		# image_label.setPixmap(frame)
		# layout.addWidget(image_label)

		view = QtWebEngineWidgets.QWebEngineView()
		#view.load(QtCore.QUrl().fromLocalFile("/home/jonas/Projects/dicum/resources/test.html"))
		view.load(QtCore.QUrl().fromLocalFile("/home/jonas/Projects/dicum/resources/chick.jpeg"))
		#view.load(QtCore.QUrl("https://google.com"))
		layout.addWidget(view)
		layout.addWidget(self.button_widget)
		layout.addWidget(self.label)
		self.setLayout(layout)

	def get_content(self, pos):
		try:
			self.button_array[pos].setEnabled(False)
			self.label.setText(str(self.generator.get_next()))
		except:
			print("Array position", pos, "is out of range")

	def print_hello(self):
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
