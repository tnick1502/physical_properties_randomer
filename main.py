import sys
from PyQt5.QtWidgets import QApplication
from widget.app_widget import App

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    ex = App()
    sys.exit(app.exec_())
