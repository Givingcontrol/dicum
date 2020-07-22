from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtGui import QPixmap
from PyQt5 import QtWebEngineWidgets
from PyQt5 import QtCore

class ButtonWidget(QWidget):
	def __init__(self, *args, **kwargs):
		super(QWidget, self).__init__(*args, **kwargs)

		self.counter = 0

		self.label = QLabel(str(self.counter))
		button = QPushButton("Click Me!")
		button.clicked.connect(lambda:self.count())

		layout = QVBoxLayout()
		frame = QPixmap("resources/chick.jpeg")

		layout.addWidget(self.label)
		imageLabel = QLabel(self)
		imageLabel.setPixmap(frame)
		layout.addWidget(imageLabel)
		layout.addWidget(button)

		view = QtWebEngineWidgets.QWebEngineView()
		view.load(QtCore.QUrl().fromLocalFile("/home/jonas/Projects/dicum/resources/test.html"))
		layout.addWidget(view)
		self.setLayout(layout)

	def count(self):
		self.counter += 1
		self.label.setText(str(self.counter))

	def PrintHello(self):
		print("Hello")


class MainWindow(QMainWindow):
	def __init__(self, *args, **kwargs):
		super(MainWindow, self).__init__(*args, **kwargs)

		self.setWindowTitle("Dicum")
		mainWidget = ButtonWidget(self)
		self.setCentralWidget(mainWidget)


if __name__ == '__main__':
	app = QApplication([])

	mainWindow = MainWindow()
	mainWindow.show()

	app.exec()
