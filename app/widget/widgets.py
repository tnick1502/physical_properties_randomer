from PyQt5.QtWidgets import QHeaderView, QTableWidgetItem, QTableWidget, QWidget, QVBoxLayout, QHBoxLayout, QGroupBox,\
    QLineEdit, QPushButton, QLabel, QFileDialog
from PyQt5.QtCore import Qt
from PyQt5 import QtGui

test_data = {'89-4': {
    'origin_data': {'rs': 2.71, 'r': 2.18, 'rd': 1.91, 'n': 29.7, 'e': 0.42, 'W': 14.4, 'Sr': 0.93, 'Wl': 22.9, 'Wp': 13.4, 'Ip': 9.5, 'Il': 0.11, 'Ir': None, 'rd_min': None, 'rd_max': None, 'Kf_min': None,
                    'Kf_max': None, 'slope_angle_dry': None, 'slope_angle_wet': None, 'granulometric_10': None, 'granulometric_5': None, 'granulometric_2': None, 'granulometric_1': None,
                    'granulometric_05': None, 'granulometric_025': None, 'granulometric_01': None, 'granulometric_005': None, 'granulometric_001': None, 'granulometric_0002': None,
                    'granulometric_0000': None, 'sample_number': 0, 'type_ground': 7},
    'modified_data': {'rs': 2.77, 'r': 2.17, 'rd': 1.93, 'n': 30.6, 'e': 0.44, 'W': 12.5, 'Sr': 0.07, 'Wl': 24.9, 'Wp': 15.3, 'Ip': 9.6, 'Il': -0.29, 'Ir': None, 'rd_min': None, 'rd_max': None,
                      'Kf_min': None, 'Kf_max': None, 'slope_angle_dry': None, 'slope_angle_wet': None, 'granulometric_10': None, 'granulometric_5': None, 'granulometric_2': None,
                      'granulometric_1': None, 'granulometric_05': None, 'granulometric_025': None, 'granulometric_01': None, 'granulometric_005': None, 'granulometric_001': None,
                      'granulometric_0002': None, 'granulometric_0000': None}},
    '89-7': {
        'origin_data': {'rs': 2.66, 'r': None, 'rd': None, 'n': None, 'e': None, 'W': 10.0, 'Sr': None, 'Wl': None, 'Wp': None, 'Ip': None, 'Il': None, 'Ir': None, 'rd_min': 1.44,
                        'rd_max': 1.63, 'Kf_min': 7.31, 'Kf_max': 3.64, 'slope_angle_dry': None, 'slope_angle_wet': None, 'granulometric_10': None, 'granulometric_5': None,
                        'granulometric_2': None, 'granulometric_1': None, 'granulometric_05': None, 'granulometric_025': 2.2, 'granulometric_01': 90.5, 'granulometric_005': 7.3,
                        'granulometric_001': None, 'granulometric_0002': None, 'granulometric_0000': None, 'sample_number': 1, 'type_ground': 4},
        'modified_data': {'rs': 2.61, 'r': None, 'rd': None, 'n': None, 'e': None, 'W': 11.8, 'Sr': None, 'Wl': None, 'Wp': None, 'Ip': None, 'Il': None, 'Ir': None, 'rd_min': 1.34,
                          'rd_max': 1.46, 'Kf_min': 8.57, 'Kf_max': 3.04, 'slope_angle_dry': None, 'slope_angle_wet': None, 'granulometric_10': None, 'granulometric_5': None,
                          'granulometric_2': None, 'granulometric_1': None, 'granulometric_05': 0.1, 'granulometric_025': 1.0, 'granulometric_01': 93.3, 'granulometric_005': 5.6,
                          'granulometric_001': None, 'granulometric_0002': None, 'granulometric_0000': 0.0}},
    '91-3': {'origin_data': {'rs': 2.7, 'r': 2.12, 'rd': 1.87, 'n': 30.9, 'e': 0.45, 'W': 13.6,
                             'Sr': 0.82, 'Wl': 21.6, 'Wp': 12.8, 'Ip': 8.8, 'Il': 0.1, 'Ir': None, 'rd_min': None, 'rd_max': None, 'Kf_min': None, 'Kf_max': None,
                             'slope_angle_dry': None, 'slope_angle_wet': None, 'granulometric_10': None, 'granulometric_5': None, 'granulometric_2': None, 'granulometric_1': None,
                             'granulometric_05': None, 'granulometric_025': None, 'granulometric_01': None, 'granulometric_005': None, 'granulometric_001': None, 'granulometric_0002': None,
                             'granulometric_0000': None, 'sample_number': 2, 'type_ground': 7},
             'modified_data': {'rs': 2.7, 'r': 2.11, 'rd': 1.84, 'n': 32.0, 'e': 0.47,
                               'W': 14.6, 'Sr': 0.06, 'Wl': 24.8, 'Wp': 14.7, 'Ip': 10.1, 'Il': -0.01, 'Ir': None, 'rd_min': None, 'rd_max': None, 'Kf_min': None, 'Kf_max': None,
                               'slope_angle_dry': None, 'slope_angle_wet': None, 'granulometric_10': None, 'granulometric_5': None, 'granulometric_2': None, 'granulometric_1': None,
                               'granulometric_05': None, 'granulometric_025': None, 'granulometric_01': None, 'granulometric_005': None, 'granulometric_001': None, 'granulometric_0002': None,
                               'granulometric_0000': None}}, '91-5': {'origin_data': {'rs': 2.71, 'r': 2.18, 'rd': 1.92, 'n': 29.3, 'e': 0.41, 'W': 13.7, 'Sr': 0.9, 'Wl': 21.0, 'Wp': 11.7, 'Ip': 9.3, 'Il': 0.22, 'Ir': None, 'rd_min': None, 'rd_max': None, 'Kf_min': None, 'Kf_max': None, 'slope_angle_dry': None, 'slope_angle_wet': None, 'granulometric_10': None, 'granulometric_5': None, 'granulometric_2': None, 'granulometric_1': None, 'granulometric_05': None, 'granulometric_025': None, 'granulometric_01': None, 'granulometric_005': None, 'granulometric_001': None, 'granulometric_0002': None, 'granulometric_0000': None, 'sample_number': 3, 'type_ground': 7}, 'modified_data': {'rs': 2.79, 'r': 2.32, 'rd': 1.99, 'n': 28.6, 'e': 0.4, 'W': 16.3, 'Sr': 0.08, 'Wl': 19.5, 'Wp': 9.9, 'Ip': 9.6, 'Il': 0.67, 'Ir': None, 'rd_min': None, 'rd_max': None, 'Kf_min': None, 'Kf_max': None, 'slope_angle_dry': None, 'slope_angle_wet': None, 'granulometric_10': None, 'granulometric_5': None, 'granulometric_2': None, 'granulometric_1': None, 'granulometric_05': None, 'granulometric_025': None, 'granulometric_01': None, 'granulometric_005': None, 'granulometric_001': None, 'granulometric_0002': None, 'granulometric_0000': None}}, '91-6': {'origin_data': {'rs': 2.71, 'r': 2.19, 'rd': 1.92, 'n': 29.2, 'e': 0.41, 'W': 14.1, 'Sr': 0.93, 'Wl': 21.9, 'Wp': 12.9, 'Ip': 9.0, 'Il': 0.13, 'Ir': None, 'rd_min': None, 'rd_max': None, 'Kf_min': None, 'Kf_max': None, 'slope_angle_dry': None, 'slope_angle_wet': None, 'granulometric_10': None, 'granulometric_5': None, 'granulometric_2': None, 'granulometric_1': None, 'granulometric_05': None, 'granulometric_025': None, 'granulometric_01': None, 'granulometric_005': None, 'granulometric_001': None, 'granulometric_0002': None, 'granulometric_0000': None, 'sample_number': 4, 'type_ground': 7}, 'modified_data': {'rs': 2.72, 'r': 2.14, 'rd': 1.88, 'n': 31.0, 'e': 0.45, 'W': 14.1, 'Sr': 0.06, 'Wl': 22.8, 'Wp': 10.9, 'Ip': 11.9, 'Il': 0.27, 'Ir': None, 'rd_min': None, 'rd_max': None, 'Kf_min': None, 'Kf_max': None, 'slope_angle_dry': None, 'slope_angle_wet': None, 'granulometric_10': None, 'granulometric_5': None, 'granulometric_2': None, 'granulometric_1': None, 'granulometric_05': None, 'granulometric_025': None, 'granulometric_01': None, 'granulometric_005': None, 'granulometric_001': None, 'granulometric_0002': None, 'granulometric_0000': None}}, '91-9': {'origin_data': {'rs': 2.74, 'r': 1.97, 'rd': 1.53, 'n': 44.1, 'e': 0.79, 'W': 28.7, 'Sr': 1.0, 'Wl': 56.0, 'Wp': 31.8, 'Ip': 24.2, 'Il': -0.13, 'Ir': None, 'rd_min': None, 'rd_max': None, 'Kf_min': None, 'Kf_max': None, 'slope_angle_dry': None, 'slope_angle_wet': None, 'granulometric_10': None, 'granulometric_5': None, 'granulometric_2': None, 'granulometric_1': None, 'granulometric_05': None, 'granulometric_025': None, 'granulometric_01': None, 'granulometric_005': None, 'granulometric_001': None, 'granulometric_0002': None, 'granulometric_0000': None, 'sample_number': 5, 'type_ground': 8}, 'modified_data': {'rs': 2.82, 'r': 2.05, 'rd': 1.53, 'n': 45.7, 'e': 0.84, 'W': 33.7, 'Sr': 0.04, 'Wl': 49.0, 'Wp': 27.1, 'Ip': 21.9, 'Il': 0.3, 'Ir': None, 'rd_min': None, 'rd_max': None, 'Kf_min': None, 'Kf_max': None, 'slope_angle_dry': None, 'slope_angle_wet': None, 'granulometric_10': None, 'granulometric_5': None, 'granulometric_2': None, 'granulometric_1': None, 'granulometric_05': None, 'granulometric_025': None, 'granulometric_01': None, 'granulometric_005': None, 'granulometric_001': None, 'granulometric_0002': None, 'granulometric_0000': None}}, '94-3': {'origin_data': {'rs': 2.71, 'r': 2.15, 'rd': 1.85, 'n': 31.9, 'e': 0.47, 'W': 16.4, 'Sr': 0.95, 'Wl': 24.7, 'Wp': 15.2, 'Ip': 9.5, 'Il': 0.13, 'Ir': None, 'rd_min': None, 'rd_max': None, 'Kf_min': None, 'Kf_max': None, 'slope_angle_dry': None, 'slope_angle_wet': None, 'granulometric_10': None, 'granulometric_5': None, 'granulometric_2': None, 'granulometric_1': None, 'granulometric_05': None, 'granulometric_025': None, 'granulometric_01': None, 'granulometric_005': None, 'granulometric_001': None, 'granulometric_0002': None, 'granulometric_0000': None, 'sample_number': 6, 'type_ground': 7}, 'modified_data': {'rs': 2.71, 'r': 2.14, 'rd': 1.86, 'n': 31.5, 'e': 0.46, 'W': 14.8, 'Sr': 0.06, 'Wl': 24.8, 'Wp': 14.3, 'Ip': 10.5, 'Il': 0.05, 'Ir': None, 'rd_min': None, 'rd_max': None, 'Kf_min': None, 'Kf_max': None, 'slope_angle_dry': None, 'slope_angle_wet': None, 'granulometric_10': None, 'granulometric_5': None, 'granulometric_2': None, 'granulometric_1': None, 'granulometric_05': None, 'granulometric_025': None, 'granulometric_01': None, 'granulometric_005': None, 'granulometric_001': None, 'granulometric_0002': None, 'granulometric_0000': None}}, '94-4': {'origin_data': {'rs': 2.66, 'r': None, 'rd': None, 'n': None, 'e': None, 'W': 5.6, 'Sr': None, 'Wl': None, 'Wp': None, 'Ip': None, 'Il': None, 'Ir': None, 'rd_min': None, 'rd_max': None, 'Kf_min': None, 'Kf_max': None, 'slope_angle_dry': None, 'slope_angle_wet': None, 'granulometric_10': None, 'granulometric_5': None, 'granulometric_2': 0.3, 'granulometric_1': 0.9, 'granulometric_05': 10.5, 'granulometric_025': 52.8, 'granulometric_01': 21.1, 'granulometric_005': 14.4, 'granulometric_001': None, 'granulometric_0002': None, 'granulometric_0000': None, 'sample_number': 7, 'type_ground': 3}, 'modified_data': {'rs': 2.42, 'r': None, 'rd': None, 'n': None, 'e': None, 'W': 5.5, 'Sr': None, 'Wl': None, 'Wp': None, 'Ip': None, 'Il': None, 'Ir': None, 'rd_min': None, 'rd_max': None, 'Kf_min': None, 'Kf_max': None, 'slope_angle_dry': None, 'slope_angle_wet': None, 'granulometric_10': None, 'granulometric_5': 1.1, 'granulometric_2': 3.4, 'granulometric_1': 3.0, 'granulometric_05': 4.5, 'granulometric_025': 49.3, 'granulometric_01': 22.1, 'granulometric_005': 16.6, 'granulometric_001': None, 'granulometric_0002': None, 'granulometric_0000': None}}, '94-5': {'origin_data': {'rs': 2.66, 'r': None, 'rd': None, 'n': None, 'e': None, 'W': 4.9, 'Sr': None, 'Wl': None, 'Wp': None, 'Ip': None, 'Il': None, 'Ir': None, 'rd_min': None, 'rd_max': None, 'Kf_min': None, 'Kf_max': None, 'slope_angle_dry': None, 'slope_angle_wet': None, 'granulometric_10': None, 'granulometric_5': None, 'granulometric_2': 0.1, 'granulometric_1': 0.4, 'granulometric_05': 0.7, 'granulometric_025': 9.5, 'granulometric_01': 77.8, 'granulometric_005': 11.5, 'granulometric_001': None, 'granulometric_0002': None, 'granulometric_0000': None, 'sample_number': 8, 'type_ground': 4}, 'modified_data': {'rs': 2.77, 'r': None, 'rd': None, 'n': None, 'e': None, 'W': 5.0, 'Sr': None, 'Wl': None, 'Wp': None, 'Ip': None, 'Il': None, 'Ir': None, 'rd_min': None, 'rd_max': None, 'Kf_min': None, 'Kf_max': None, 'slope_angle_dry': None, 'slope_angle_wet': None, 'granulometric_10': None, 'granulometric_5': None, 'granulometric_2': None, 'granulometric_1': 17.5, 'granulometric_05': 3.61, 'granulometric_025': 27.3, 'granulometric_01': 28.6, 'granulometric_005': 23.0, 'granulometric_001': None, 'granulometric_0002': None, 'granulometric_0000': None}}}


class TablePhysicalProperties(QTableWidget):
    """Класс отрисовывает таблицу физических свойств"""
    keys = [
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

        self.setRowCount(31)
        self.setColumnCount(len(self.keys) + 1)
        self.setHorizontalHeaderLabels(["Лаб. номер"] + [key.replace("granulometric_", "") for key in self.keys])

        self.verticalHeader().setMinimumSectionSize(30)

        self.horizontalHeader().setMinimumSectionSize(30)
        self.horizontalHeader().setSectionResizeMode(1, QHeaderView.Fixed)

        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)


    def set_row_color(self, row, color=(129, 216, 208)):#color=(62, 180, 137)):
        """Раскрашиваем строку"""
        if row is not None:
            for i in range(self.columnCount()):
                self.item(row, i).setBackground(QtGui.QColor(*color))

    def get_row_by_lab_naumber(self, lab):
        """Поиск номера строки по значению лабномера"""
        for row in range(self.columnCount()):
            if self.item(row, 0).text() == lab:
                return row
        return None

    def set_data(self, data=test_data):
        """Функция для получения данных"""
        replaceNone = lambda x: x if x != "None" else "-"

        self._clear_table()

        self.active_laboratory_numbers = list(data.keys())

        self.setRowCount(len(data) * 2)

        for i, lab in enumerate(data):
            item = QTableWidgetItem(lab)
            item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            item.setCheckState(Qt.Checked)
            item.setTextAlignment(Qt.AlignCenter)
            self.setItem(2 * i, 0, item)

            item = QTableWidgetItem(replaceNone(lab))
            item.setTextAlignment(Qt.AlignCenter)
            self.setItem(2 * i, 1, item)

            for g, value in enumerate([str(data[lab]["origin_data"][key]) for key in self.keys]):
                item = QTableWidgetItem(replaceNone(value))
                item.setTextAlignment(Qt.AlignCenter)
                self.setItem(2 * i, g + 1, item)
            for g, value in enumerate([str(data[lab]["modified_data"][key]) for key in self.keys]):
                item = QTableWidgetItem(replaceNone(value))
                item.setTextAlignment(Qt.AlignCenter)
                self.setItem(2 * i + 1, g + 1, item)

        for i, lab in enumerate(data):
            self.set_row_color(2 * i, (192, 192, 192))
            self.setSpan(2 * i, 0, 2, 1)
            #self.setSpan(2 * i, 1, 2, 1)

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
    def __init__(self):
        super().__init__()
        self.create_UI()
        self.setFixedHeight(80)

    def create_UI(self):

        self.savebox_layout = QVBoxLayout()

        self.path_box = QGroupBox("Параметры директории")
        self.path_box_layout = QHBoxLayout()
        self.path_box.setLayout(self.path_box_layout)
        self.directory_text = QLineEdit()
        self.directory_text.setDisabled(True)
        self.directory_text.setFixedHeight(30)
        self.change_directory_button = QPushButton("Загрузить ведомость")
        self.change_directory_button.setFixedHeight(30)
        self.change_directory_button.clicked.connect(self.change_directory)
        self.path_box_layout.addWidget(self.change_directory_button)
        self.path_box_layout.addWidget(self.directory_text)
        self.save_button = QPushButton("Сохранить")
        self.save_button.setFixedHeight(30)
        self.path_box_layout.addWidget(self.save_button)
        self.savebox_layout.addWidget(self.path_box)



        self.setLayout(self.savebox_layout)
        self.savebox_layout.setContentsMargins(5, 5, 5, 5)


    def change_directory(self):
        """Самостоятельный выбор папки сохранения"""
        s = QFileDialog.getExistingDirectory(self, "Select Directory")


