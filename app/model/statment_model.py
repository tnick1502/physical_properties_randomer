import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import Font
import xlrd
import xlutils
import xlwt
import os

from model.property_model import PhysicalProperties, RandomType

random_params = {
    "rs": {
        "type": RandomType.PERCENT,
        "value": 20
    },

    "r": {
        "type": RandomType.PERCENT,
        "value": 20
    },

    "W": {
        "type": RandomType.PERCENT,
        "value": 20
    },

    "Wl": {
        "type": RandomType.PERCENT,
        "value": 20
    },

    "Wp": {
        "type": RandomType.PERCENT,
        "value": 20
    },

    "Ir": {
        "type": RandomType.PERCENT,
        "value": 20
    },

    "rd_min": {
        "type": RandomType.PERCENT,
        "value": 20
    },

    "rd_max": {
        "type": RandomType.PERCENT,
        "value": 20
    },

    "Kf_min": {
        "type": RandomType.PERCENT,
        "value": 20
    },

    "Kf_max": {
        "type": RandomType.PERCENT,
        "value": 20
    },

    "slope_angle_dry": {
        "type": RandomType.PERCENT,
        "value": 20
    },

    "slope_angle_wet": {
        "type": RandomType.PERCENT,
        "value": 20
    },

    "granulometric": {
        "value": 3
    },

    "granulometric_areometer": {
        "value": 3
    },
}

class Statment:
    data: dict = {}
    excel_path: str = ''
    dataframe: pd.DataFrame

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Statment, cls).__new__(cls)
        return cls.instance

    def setExcelFile(self, path: str) -> None:
        """Открытие и загрузка файла excel

            :argument path: путь к файлу
            :return None
        """
        if not all([os.path.exists(path), (path.endswith('.xls') or path.endswith('.xlss'))]):
            raise Exception("Wrong file excel")

        self.excel_path = path

        df = pd.read_excel(self.excel_path, usecols="A:IV", skiprows=[0, 1, 3, 4, 5])
        self.dataframe = df[df['Лаб. № пробы'].notna()]

        for i, laboratory_number in enumerate(self.dataframe["Лаб. № пробы"]):
            self.data[laboratory_number] = PhysicalProperties()
            self.data[laboratory_number].defineProperties(data_frame=self.dataframe, number=i)

    def setRandom(self, params: random_params, keys: list) -> list:
        """Открытие файла excel

            :argument params: словарь параметров рандома
            :argument keys: лабномера для ативации на их моделях функции рандома
            :return лабномера, на которых не получилось применить функцию рандома
        """
        problem_keys = []
        for key in keys:
            res = self.data[key].setRandom(params)
            if not res:
                problem_keys.append(key)
        return problem_keys

    def getData(self) -> dict:
        """Получение всех параметров

            :return словарь с ключам лабнмеров, по значением в которых словарь с оригинальными
            зачениями параметров по ключу origin_data и измененными по ключу modified_data
        """
        return {
            key: self.data[key].getData() for key in self.data
        }

    def __iter__(self):
        for key in self.data:
            yield key

    def __len__(self):
        return len(self.data)

    def __getitem__(self, key):
        if not key in list(self.data.keys()):
            return KeyError(f"No test with key {key}")
        return self.data[key]

    def __str__(self):
        data = '\n'.join([''] + [f'{key}: {self.data[key]}' for key in self.data])
        return f'''Путь: {self.excel_path}
        
Данные:
{data}
'''

def set_cell_data(path: str, cell: str, value, sheet: str="Лист1", color=None) -> None:
    """Запись в файл excel

        :argument path: путь к файлу excel
        :argument cell: Ячейка ('A1', (0, 0))
        :argument value: Записываемое значение
        :argument sheet: Лист для записи
        :argument color: цвет шрифта записи

        :return None
    """
    if path.endswith("xlsx"):
        wb = load_workbook(path)
        wb[sheet][cell[0]] = value
        if color:
            cell = wb[sheet][cell[0]]
            cell.font = Font(color=color)
        wb.save(path)

    elif path.endswith("xls"):
        wb = xlrd.open_workbook(path, formatting_info=True)

        out_wb = xlutils.copy.copy(wb)
        sheet = out_wb.get_sheet(0)

        if color:
            xlwt.add_palette_colour("font_colour", 0x21)
            out_wb.set_colour_RGB(0x21, *tuple(int(color[i:i+2], 16) for i in (0, 2, 4)))
            style = xlwt.easyxf('font: colour font_colour')
            sheet.write(cell[1][0] - 1, cell[1][1], value, style)
        else:
            sheet.write(cell[1][0] - 1, cell[1][1], value)

        out_wb.save(path)



if __name__ == "__main__":
    s = Statment()
    #s.setExcelFile('/Users/mac1/Desktop/projects/databases/511-21 ул. Красного Маяка, 26- мех-2.xls')
    s.setExcelFile('C:/Users/Пользователь/Desktop/test/test.xls')
    s.setRandom()
    print(s.getData())