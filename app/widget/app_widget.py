import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QVBoxLayout, QWidget

from widgets import TablePhysicalProperties, OpenWidget

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = "Крутяк"
        self.left = 100
        self.top = 30
        self.width = 1800
        self.height = 1000

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.widget = QWidget()
        self.layout = QVBoxLayout()
        self.widget.setLayout(self.layout)

        self.table = TablePhysicalProperties()
        self.open_widget = OpenWidget()

        self.layout.addWidget(self.open_widget)
        self.layout.addWidget(self.table)

        self.setCentralWidget(self.widget)

        self.layout.setContentsMargins(5, 5, 5, 5)
        self.table.set_data()

        self.show()


    def keyPressEvent(self, event):
        if str(event.key()) == "16777216":
            if self.isFullScreen():
                self.showNormal()
            else:
                self.showFullScreen()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    ex = App()
    sys.exit(app.exec_())