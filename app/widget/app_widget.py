from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QHBoxLayout, QPushButton, QMessageBox

from widgets import TablePhysicalProperties, OpenWidget, Params, ChooseWidget

from model import statment

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = "Крутяк"
        self.left = 100
        self.top = 30
        self.width = 1630
        self.height = 1000

        self.createUI()

        self.addHandlers()

        self.show()

    def createUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.widget = QWidget()
        self.layout = QVBoxLayout()
        self.widget.setLayout(self.layout)

        self.layout2 = QHBoxLayout()
        self.layout3 = QVBoxLayout()

        self.table = TablePhysicalProperties()
        self.open_widget = OpenWidget()
        self.choose = ChooseWidget()
        self.params = Params()
        self.save_button = QPushButton("Сохранить результат")
        self.save_button.setFixedHeight(50)

        self.layout3.addWidget(self.choose)
        self.layout3.addWidget(self.params)
        self.layout2.addWidget(self.table)
        self.layout3.addWidget(self.save_button)
        self.layout3.addStretch(-1)
        self.layout2.addLayout(self.layout3)
        self.layout.addWidget(self.open_widget)
        self.layout.addLayout(self.layout2)

        self.setCentralWidget(self.widget)
        self.layout.setContentsMargins(5, 5, 5, 5)

    def addHandlers(self):
        self.open_widget.signal.connect(self.table.set_data)
        self.params.signal[dict].connect(self.set_random)
        self.choose.signal[list].connect(self.table.filter)
        self.save_button.clicked.connect(self.save)

    def set_random(self, params):
        try:
            active = self.table.active_laboratory_numbers
            problem_keys = statment.setRandom(params, active)
            self.table.set_data(active_keys=active, problem_keys=problem_keys)
        except Exception as e:
            print(e)

    def save(self):
        try:
            statment.saveExcel()
            QMessageBox.about(self, "Сообщение", "Успешно сохранено")
        except Exception as err:
            QMessageBox.critical(self, "Ошибка", f"{str(err)}", QMessageBox.Ok)

    def keyPressEvent(self, event):
        if str(event.key()) == "16777216":
            if self.isFullScreen():
                self.showNormal()
            else:
                self.showFullScreen()
