from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QMainWindow, QVBoxLayout
from PyQt5.QtCore import Qt


class MainWindow(QMainWindow):
	def __init__(self, *args, **kwargs):
		super(MainWindow, self).__init__(*args, **kwargs)

		self.setWindowTitle("Dicum")
		label = QLabel("Hello, World!")
		label.setAlignment(Qt.AlignCenter)
		self.setCentralWidget(label)


if __name__ == '__main__':
	app = QApplication([])

	mainWindow = MainWindow()
	mainWindow.show()

	app.exec()
