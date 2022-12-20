import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox

from widgets import TablePhysicalProperties

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = "Крутяк"
        self.left = 100
        self.top = 30
        self.width = 1800
        self.height = 1000

        self.table = TablePhysicalProperties()


        self.setCentralWidget(self.table)
        self.table.set_data()

        self.show()

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)


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