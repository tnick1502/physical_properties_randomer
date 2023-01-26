__version__ = '1.0.0'

from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QHBoxLayout, QPushButton, QMessageBox

from widgets import TablePhysicalProperties, OpenWidget, Params, ChooseWidget, Info

from app.model import statment

info = f'''Крутяк {__version__}



Программа для наложения рандома на физические свойства грунтов в ведомости



Инструкция:

1. Выберите файл ведомости в виджете "Параметры директории". Все свойства отобразятся в таблице. Оригинальные свойства отображаются на желтом фоне, измененные - на сером.

2. Выберите трубуемые пробы в таблице. Для этого можно воспользоваться меню выбора через галочки в таблице или применить различные фильтры через виджет "Параметры выбора".

3. Настройте требуемую конфигарацию для определения границ вариаций в виджете "Типы параметров" или загрузите трубуемую конфигурацию в выпадающем меню. Свойства, на которые накладывается рандом отмечаются галочкой в виджете "Типы параметров"
Значения можно задавать через проценты, через абсолютную величину или в диапазоне. 
После настройки всех значений данную конфигурацию можно сохранить, для этого надо ввести имя конфигурации и нажать кнопку сохранить в виджете "Типы параметров".

4. Нажмите кнопку "Крутить" в виджете "Типы параметров". После этого новые значения измененных свойств отобразятся в строке соответствующей побы на сером фоне. 
В СЛУЧАЕ, ЕСЛИ АЛГОРИТМ Е СМОЖЕТ ПОДОБРАТЬ ИЗМЕНЕНИЯ ДЛЯ ЗАДАННОЙ КОНФИГУРАЦИИ, ЗНАЧЕНИЯ ИЗМЕНЕННЫХ ПАРАМЕТРОВ ПРИРАВНИЮТСЯ К ОРИГИНАЛЬНЫМ, А В ТАБИЦЕ ЭТОТ ОБРАЗЕЦ ПОДСВЕТИТСЯ КРАСНЫМ.

5. Нажмите кнопку "Сохранить результаты" для сохранения новой ведомости. Ведомость появится рядом с оригинальной с подписью "ИЗМЕНЕННАЯ".



Работа алгоритма и рекомендации:

Алгоритм накладывает рандомные значения на выбранные параметры в выбранной конфигурации. После наложения свойств алгоритм пересчитывает значения rd, e, n, Ip, Il, Sr и определяет тип грунта. Если тип грунта отличается от исходного, происходит повторное наложение рандома и проверка. Всего алгоритм делает 1000 итераций, на каждой 100 итерации он автоматически снижает диапазон рандома. В случае, если условия не выполняются, алгоритм присвоит измененным параметрам значения оригинальных.

Для повышения точности работы алгоритма рекомендуется выбирать ограниченный круг изменяемых параметров, сохраняя их в меню сохранения конфигураций. Данная практика позволяет расширить диапазон изменений в каждом параметре.
'''

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = f"Крутяк {__version__}"
        self.left = 100
        self.top = 30
        self.width = 1750
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
        self.info_button = QPushButton("Инструкция и описание")
        self.info_button.setFixedHeight(50)
        self.save_button = QPushButton("Сохранить результат")
        self.save_button.setFixedHeight(50)

        self.layout3.addWidget(self.info_button)
        self.layout3.addWidget(self.open_widget)
        self.layout3.addWidget(self.choose)
        self.layout3.addWidget(self.params)
        self.layout2.addWidget(self.table)
        self.layout3.addWidget(self.save_button)
        self.layout3.addStretch(-1)
        self.layout2.addLayout(self.layout3)
        self.layout.addLayout(self.layout2)

        self.setCentralWidget(self.widget)
        self.layout.setContentsMargins(5, 5, 5, 5)

    def addHandlers(self):
        self.open_widget.signal.connect(self.table.set_data)
        self.open_widget.signal.connect(self.choose.update)
        self.params.signal[dict].connect(self.set_random)
        self.choose.signal[list].connect(self.table.filter)
        self.save_button.clicked.connect(self.save)
        self.info_button.clicked.connect(self.info)

    def set_random(self, params):
        try:
            active = self.table.active_laboratory_numbers
            problem_keys = statment.setRandom(params, active)
            self.table.set_data(active_keys=active, problem_keys=problem_keys)
        except Exception as err:
            QMessageBox.critical(self, "Ошибка", f"{str(err)}", QMessageBox.Ok)

    def save(self):
        try:
            statment.saveExcel()
            QMessageBox.about(self, "Сообщение", "Успешно сохранено")
        except Exception as err:
            QMessageBox.critical(self, "Ошибка", f"{str(err)}", QMessageBox.Ok)

    def info(self):
        try:
            dialog = Info(self)
            dialog.setText(info)
            dialog.show()
        except Exception as err:
            print(err)

    def keyPressEvent(self, event):
        if str(event.key()) == "16777216":
            if self.isFullScreen():
                self.showNormal()
            else:
                self.showFullScreen()
