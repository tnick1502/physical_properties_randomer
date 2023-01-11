from PyQt5.QtWidgets import QHeaderView, QTableWidgetItem, QTableWidget, QWidget, QVBoxLayout, QHBoxLayout, QGroupBox,\
    QLineEdit, QPushButton, QLabel, QFileDialog, QMessageBox, QCheckBox, QComboBox, QDialog, QTextEdit
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5 import QtGui
import json
import os

from app.model import statment
from app.model.statment_model import RandomType
from app.model.properties_params import GroundTypes

PARAMS_PATH = "Z:/Digitrock/randomerParams.json"

def open_json() -> dict:
    """Считывание json файла в словарь"""
    with open(PARAMS_PATH, 'r', encoding='utf-8') as file:
        json_data = json.load(file)
    return json_data

def write_json(data: dict) -> None:
    """Запись словаря в json файл. Если файл отсутствует, то создается новый"""
    with open(PARAMS_PATH, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False)


class TablePhysicalProperties(QTableWidget):
    """Класс отрисовывает таблицу физических свойств"""
    keys = [
        "type_ground",
        "rs", "r", "rd", "n", "e", "W", "Sr",
        "Wl", "Wp", "Ip", "Il", "Ir",
        "rd_min", "rd_max", "Kf_min", "Kf_max", "slope_angle_dry", "slope_angle_wet",
        "granulometric_10", "granulometric_5", "granulometric_2",
        "granulometric_1", "granulometric_05", "granulometric_025",
        "granulometric_01", "granulometric_005",
        "granulometric_001", "granulometric_0002", "granulometric_0000"
    ]

    active_laboratory_numbers = []

    def __init__(self):
        super().__init__()
        self.horizontalHeader().setSectionsMovable(True)
        self._clear_table()
        self.itemClicked.connect(self.handleItemClicked)

    def _clear_table(self):
        """Очистка таблицы и придание соответствующего вида"""
        while (self.rowCount() > 0):
            self.removeRow(0)

        self.setRowCount(0)
        self.setColumnCount(len(self.keys) + 3)
        self.setHorizontalHeaderLabels(["Лаб. номер", "Скважина", "Глубина", "Наименование"] + [key.replace("granulometric_", "") for key in self.keys if key != "type_ground"])

        self.verticalHeader().setMinimumSectionSize(30)

        self.horizontalHeader().setMinimumSectionSize(30)

        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

    def set_row_color(self, row, color=(129, 216, 208)):#color=(62, 180, 137)):
        """Раскрашиваем строку"""
        if row is not None:
            for i in range(self.columnCount()):
                self.item(row, i).setBackground(QtGui.QColor(*color))

    def get_row_by_lab_number(self, lab):
        """Поиск номера строки по значению лабномера"""
        for row in range(self.columnCount()):
            try:
                if self.item(row, 0).text() == lab:
                    return row
            except:
                pass
        return None

    def filter(self, lab_numbers):
        for i in range(self.rowCount()):
            try:
                text = self.item(i, 0).text()
                item = self.item(i, 0)
                if text in lab_numbers:
                    item.setCheckState(Qt.Checked)
                else:
                    item.setCheckState(Qt.Unchecked)
            except:
                pass
        self.active_laboratory_numbers = lab_numbers

    def set_data(self, active_keys=None, problem_keys=[]):
        """Функция для получения данных"""
        try:
            replaceNone = lambda x: x if x != "None" else "-"

            data = statment.getData()

            self._clear_table()

            self.active_laboratory_numbers = active_keys if active_keys is not None else list(data.keys())

            self.setRowCount(len(data) * 2)

            for i, lab in enumerate(data):
                item = QTableWidgetItem(lab)
                item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
                if lab in self.active_laboratory_numbers:
                    item.setCheckState(Qt.Checked)
                else:
                    item.setCheckState(Qt.Unchecked)
                item.setTextAlignment(Qt.AlignCenter)
                self.setItem(2 * i, 0, item)

                item_borehole = QTableWidgetItem(replaceNone(data[lab]["origin_data"]["borehole"]))
                item_borehole.setTextAlignment(Qt.AlignCenter)
                self.setItem(2 * i, 1, item_borehole)

                item_depth = QTableWidgetItem(str(replaceNone(data[lab]["origin_data"]["depth"])))
                item_depth.setTextAlignment(Qt.AlignCenter)
                self.setItem(2 * i, 2, item_depth)

                for g, value in enumerate([str(data[lab]["origin_data"][key]) for key in self.keys]):
                    if g == 0:
                        value = GroundTypes[int(value)]
                    item = QTableWidgetItem(replaceNone(value))
                    item.setTextAlignment(Qt.AlignCenter)
                    self.setItem(2 * i, g + 3, item)

                for g, value in enumerate([str(data[lab]["modified_data"][key]) for key in self.keys]):
                    if g == 0:
                        value = GroundTypes[int(value)]
                    item = QTableWidgetItem(replaceNone(value))
                    item.setTextAlignment(Qt.AlignCenter)
                    self.setItem(2 * i + 1, g + 3, item)

            for i, lab in enumerate(data):
                if lab in problem_keys:
                    self.set_row_color(2 * i, (221, 65, 36))
                else:
                    self.set_row_color(2 * i, (231, 210, 186))
                self.setSpan(2 * i, 0, 2, 1)
                self.setSpan(2 * i, 1, 2, 1)
                self.setSpan(2 * i, 2, 2, 1)
        except Exception as err:
            print(err)

    def handleItemClicked(self, item):
       if item.column() == 0:
            if item.checkState() == Qt.Checked:
                self.active_laboratory_numbers.append(item.text())
            elif item.checkState() == Qt.Unchecked:
                self.active_laboratory_numbers.remove(item.text())

    def get_labels(self):
        header = self.table.horizontalHeader()
        labels = [header.model().headerData(header.logicalIndex(i), Qt.Horizontal) for i in range(header.count())]
        print(labels)

    @property
    def active(self):
        return self.active_laboratory_numbers

class OpenWidget(QWidget):
    signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.create_UI()
        self.setFixedHeight(120)
        self.setFixedWidth(450)

    def create_UI(self):

        self.savebox_layout = QVBoxLayout()

        self.path_box = QGroupBox("Параметры директории")
        self.path_box_layout = QVBoxLayout()
        self.path_box.setLayout(self.path_box_layout)
        self.directory_text = QLineEdit()
        self.directory_text.setDisabled(True)
        self.directory_text.setFixedHeight(30)
        self.change_directory_button = QPushButton("Загрузить ведомость")
        self.change_directory_button.setFixedHeight(30)
        self.change_directory_button.clicked.connect(self.change_directory)
        self.path_box_layout.addWidget(self.change_directory_button)
        self.path_box_layout.addWidget(self.directory_text)
        self.savebox_layout.addWidget(self.path_box)

        self.setLayout(self.savebox_layout)
        self.savebox_layout.setContentsMargins(5, 5, 5, 5)

    def change_directory(self):
        """Самостоятельный выбор папки сохранения"""
        s = QFileDialog.getOpenFileName(self, "Select file")
        try:
            statment.setExcelFile(s[0])
            self.directory_text.setText(s[0])
            self.signal.emit()
        except Exception as err:
            QMessageBox.critical(self, "Ошибка", f"{str(err)}", QMessageBox.Ok)

class ChooseWidget(QWidget):
    signal = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self.create_UI()
        self.setFixedHeight(120)

    def create_UI(self):

        self.layout = QVBoxLayout()

        self.box = QGroupBox("Параметры выбора")
        self.box_layout = QVBoxLayout()
        self.box.setLayout(self.box_layout)

        self.h1_layout = QHBoxLayout()
        self.h2_layout = QHBoxLayout()
        self.all_button = QPushButton("Активировать все")
        self.all_button.setFixedHeight(30)
        self.zero_button = QPushButton("Деактивировать все")
        self.zero_button.setFixedHeight(30)

        self.h1_layout.addWidget(self.all_button)
        self.h1_layout.addWidget(self.zero_button)

        self.h2_layout.addWidget(QLabel("Фильтр по типу грунта"))
        self.combobox = QComboBox()
        self.combobox.addItems(["Не выбрано"] + list(GroundTypes.values()))
        self.h2_layout.addWidget(self.combobox)
        self.combobox.setFixedHeight(30)
        self.combobox.setFixedWidth(300)

        self.box_layout.addLayout(self.h1_layout)
        self.box_layout.addLayout(self.h2_layout)

        self.layout.addWidget(self.box)
        self.setLayout(self.layout)
        self.layout.setContentsMargins(5, 5, 5, 5)

        self.zero_button.clicked.connect(lambda: self.signal.emit([]))
        self.all_button.clicked.connect(lambda: self.signal.emit(list(statment.data.keys())))
        self.combobox.activated.connect(self._combo_changed)

    def _combo_changed(self, value):
        if value == 0:
            self.signal.emit(list(statment.data.keys()))
        else:
            self.signal.emit([key for key in statment.data.keys() if statment.data[key].type_ground == value])

class Params(QWidget):
    signal = pyqtSignal(dict)

    keys = [
        "rs", "r", "W", "Wl", "Wp", "Ir", "rd_min", "rd_max", "Kf_min", "Kf_max",
        "slope_angle_dry", "slope_angle_wet", "granulometric", "granulometric_areometer"
    ]

    initial_params = {
        "rs": {
            "type": "Проценты",
            "value": 10,
            "active": True
        },
        "r": {
            "type": "Проценты",
            "value": 10,
            "active": True
        },
        "W": {
            "type": "Проценты",
            "value": 10,
            "active": True
        },
        "Wl": {
            "type": "Проценты",
            "value": 10,
            "active": True
        },
        "Wp": {
            "type": "Проценты",
            "value": 10,
            "active": True
        },
        "Ir": {
            "type": "Проценты",
            "value": 10,
            "active": True
        },
        "rd_min": {
            "type": "Проценты",
            "value": 10,
            "active": True
        },
        "rd_max": {
            "type": "Проценты",
            "value": 10,
            "active": True
        },
        "Kf_min": {
            "type": "Проценты",
            "value": 10,
            "active": True
        },
        "Kf_max": {
            "type": "Проценты",
            "value": 10,
            "active": True
        },
        "slope_angle_dry": {
            "type": "Проценты",
            "value": 10,
            "active": True
        },
        "slope_angle_wet": {
            "type": "Проценты",
            "value": 10,
            "active": True
        },
        "granulometric": {
            "type": "Проценты",
            "value": 5,
            "active": True
        },
        "granulometric_areometer": {
            "type": "Проценты",
            "value": 5,
            "active": True
        }
    }

    params = {}

    def __init__(self):
        super().__init__()
        self.create_UI()

        if os.path.exists(PARAMS_PATH):
            self.params = open_json()
        else:
            write_json({
                "По умолчанию": self.initial_params
            })
            self.params["По умолчанию"] = self.initial_params

        self.combobox.addItems(list(self.params.keys()))

        self.set_params(self.initial_params)
        self.setFixedHeight(550)
        self.setFixedWidth(450)

    def create_UI(self):

        self.savebox_layout = QVBoxLayout()

        self.box = QGroupBox("Типы параметров")
        self.box_layout = QVBoxLayout()
        self.box.setLayout(self.box_layout)
        self.h1_layout = QHBoxLayout()
        self.h2_layout = QHBoxLayout()

        self.combobox = QComboBox()
        self.combobox.setFixedHeight(30)
        self.h1_layout.addWidget(self.combobox)

        self.param_save_line = QLineEdit()
        self.param_save_line.setFixedHeight(30)
        self.param_save_button = QPushButton("Сохранить текущую конфигурацию")
        self.param_save_button.setFixedHeight(30)

        self.h2_layout.addWidget(self.param_save_line)
        self.h2_layout.addWidget(self.param_save_button)

        self.box_layout.addLayout(self.h1_layout)
        self.box_layout.addLayout(self.h2_layout)


        self.path_box = QGroupBox("Параметры")
        self.path_box_layout = QVBoxLayout()
        self.path_box.setLayout(self.path_box_layout)

        for key in self.keys:
            setattr(self, f'layout_{key}', QHBoxLayout())
            layout = getattr(self, f'layout_{key}')

            setattr(self, f'checkbox_active_{key}', QCheckBox())
            checkbox = getattr(self, f'checkbox_active_{key}')
            checkbox.setFixedWidth(20)
            checkbox.setChecked(True)
            layout.addWidget(checkbox)

            setattr(self, f'label_{key}', QLabel(key))
            label = getattr(self, f'label_{key}')
            label.setFixedWidth(120)
            layout.addWidget(label)

            setattr(self, f'text_min_{key}', QLineEdit())
            min_text = getattr(self, f'text_min_{key}')
            min_text.setFixedWidth(50)
            setattr(self, f'text_max_{key}', QLineEdit())
            max_text = getattr(self, f'text_max_{key}')
            max_text.setFixedWidth(50)
            layout.addWidget(min_text)
            layout.addWidget(max_text)

            setattr(self, f'check_type_{key}', QComboBox())
            combobox = getattr(self, f'check_type_{key}')
            if "gran" in key:
                combobox.addItems(["Проценты"])
            else:
                combobox.addItems(["Проценты", "Абсолютное значение", "Диапазон"])
            combobox.setObjectName(f'check_type_{key}')
            combobox.activated.connect(self._combo_changed)
            layout.addWidget(combobox)

            self.path_box_layout.addLayout(layout)

        self.savebox_layout.addWidget(self.box)
        self.savebox_layout.addWidget(self.path_box)
        self.button = QPushButton("Крутить")
        self.button.setFixedHeight(30)
        self.button.clicked.connect(self.get_data)
        self.param_save_button.clicked.connect(self.save_params)
        self.combobox.activated.connect(self._combo_param_changed)
        self.savebox_layout.addWidget(self.button)
        self.setLayout(self.savebox_layout)
        self.savebox_layout.setContentsMargins(5, 5, 5, 5)

    def set_params(self, params):
        combo = {
            "Проценты": 0,
            "Абсолютное значение": 1,
            "Диапазон": 2
        }

        for key in params:
            checkbox = getattr(self, f'checkbox_active_{key}')
            checkbox.setChecked(params[key]["active"])

            combobox = getattr(self, f'check_type_{key}')
            combobox.setCurrentIndex(combo[params[key]["type"]])
            self._set_combo(key, combo[params[key]["type"]])

            if combo[params[key]["type"]] in [0, 1]:
                min_text = getattr(self, f'text_min_{key}')
                if params[key]["value"]:
                    min_text.setText(str(params[key]["value"]))
            else:
                min_text = getattr(self, f'text_min_{key}')
                if params[key]["value"][0]:
                    min_text.setText(str(params[key]["value"][0]))
                max_text = getattr(self, f'text_max_{key}')
                if params[key]["value"][1]:
                    max_text.setText(str(params[key]["value"][1]))

    def _combo_changed(self, value):
        s = self.sender()
        key = s.objectName()[11:]
        self._set_combo(key, value)

    def _combo_param_changed(self):
        try:
            text = self.combobox.currentText()
            self.set_params(self.params[text])
        except Exception as err:
            print(err)

    def _set_combo(self, key, value):
        if value == 2:
            min_text = getattr(self, f'text_min_{key}')
            min_text.setFixedWidth(52)
            max_text = getattr(self, f'text_max_{key}')
            max_text.show()
        else:
            min_text = getattr(self, f'text_min_{key}')
            min_text.setFixedWidth(108)
            max_text = getattr(self, f'text_max_{key}')
            max_text.hide()

    def get_data(self):
        combo = {
            "Проценты": RandomType.PERCENT,
            "Абсолютное значение": RandomType.ABSOLUTE,
            "Диапазон": RandomType.ABSOLUTE_BETWEEN
        }

        params = {}
        try:
            for key in self.keys:
                checkbox = getattr(self, f'checkbox_active_{key}')
                if checkbox.isChecked():
                    combobox = getattr(self, f'check_type_{key}')
                    type = combo[combobox.currentText()]

                    if type == RandomType.ABSOLUTE_BETWEEN:
                        try:
                            min_text = getattr(self, f'text_min_{key}')
                            min_value = float(min_text.text())
                            max_text = getattr(self, f'text_max_{key}')
                            max_value = float(max_text.text())

                            params[key] = {
                                "type": type,
                                "value": [min_value, max_value]
                            }
                        except Exception:
                            raise ValueError(f"Ошибка в значениях для параметра {key}")

                        if max_value <= min_value:
                            raise ValueError(f"Ошибка в значениях для параметра {key}. Максимальное значение должно быть больше минимального")

                    else:
                        try:
                            text = getattr(self, f'text_min_{key}')
                            value = float(text.text())

                            params[key] = {
                                "type": type,
                                "value": value
                            }
                        except Exception:
                            raise ValueError(f"Ошибка в значениях для параметра {key}")

            self.signal.emit(params)
        except Exception as err:
            QMessageBox.critical(self, "Ошибка", f"{str(err)}", QMessageBox.Ok)

    def _get(self):
        params = {}

        for key in self.keys:
            checkbox = getattr(self, f'checkbox_active_{key}')
            active = True if checkbox.isChecked() else False

            combobox = getattr(self, f'check_type_{key}')
            type = combobox.currentText()

            if type == "Диапазон":
                min_text = getattr(self, f'text_min_{key}')
                min_value = float(min_text.text()) if min_text.text() else None
                max_text = getattr(self, f'text_max_{key}')
                max_value = float(max_text.text()) if max_text.text() else None

                params[key] = {
                    "active": active,
                    "type": type,
                    "value": [min_value, max_value]
                }
            else:
                text = getattr(self, f'text_min_{key}')
                value = float(text.text()) if text.text() else None

                params[key] = {
                    "active": active,
                    "type": type,
                    "value": value
                }
        return params

    def save_params(self):
        try:
            text = self.param_save_line.text()
            if not text:
                QMessageBox.critical(self, "Ошибка", f"Заполните поле названия", QMessageBox.Ok)
            else:
                if text in list(self.params.keys()):
                    ret = QMessageBox.question(self, 'Предупреждение',
                                               f"Параметр {text} уже существует. Хотите перезаписать?",
                                               QMessageBox.Yes | QMessageBox.Cancel, QMessageBox.Cancel)
                    if ret == QMessageBox.Yes:
                        self.params[text] = self._get()
                        write_json(self.params)
                        self.combobox.addItems([text])
                        self.combobox.setCurrentText(text)
                        QMessageBox.about(self, "Сообщение", "Успешно сохранено")
                else:
                    self.params[text] = self._get()
                    write_json(self.params)
                    self.combobox.addItems([text])
                    self.combobox.setCurrentText(text)
                    QMessageBox.about(self, "Сообщение", "Успешно сохранено")
        except Exception as err:
            QMessageBox.critical(self, "Ошибка", f"{str(err)}", QMessageBox.Ok)

class Info(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._UI()

    def setText(self, info: str):
        self.textbox.setText(info)

    def _UI(self):
        self.setWindowTitle("Инструкция")
        self.setFixedWidth(500)
        self.setFixedHeight(600)
        self.layout = QVBoxLayout()
        self.layout_buttons = QHBoxLayout()
        self.setLayout(self.layout)
        self.textbox = QTextEdit()
        #self.textbox.setDisabled(True)

        self.ok_button = QPushButton("Ok")
        self.ok_button.clicked.connect(lambda: self.close())

        self.layout_buttons.addStretch(-1)
        self.layout_buttons.addWidget(self.ok_button)

        self.layout.addWidget(self.textbox)
        self.layout.addLayout(self.layout_buttons)



