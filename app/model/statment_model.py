import pandas as pd
import xlrd
from xlutils.copy import copy
import os

from app.model.property_model import PhysicalProperties, RandomType
from app.model.properties_params import PhysicalPropertyParams

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

        self.data = {}

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

    def saveExcel(self) -> None:
        """Сохранение измененных параметров в эксель

        Копирует исхожный excel файл и записывает в него измененные значения

            :return None
        """
        postfix = "ИЗМЕНЕННЫЙ"

        dir, file_name = os.path.split(self.excel_path)
        _, file_extension = os.path.splitext(self.excel_path)
        path = os.path.normpath(os.path.join(dir, f'{file_name.replace(file_extension, "")} {postfix}{file_extension}'))

        data = self.getData()

        '''if file_extension == ".xlsx":
            shutil.copy(self.excel_path, path)
            sheet: str = "Лист1"
            wb = load_workbook(path)
            for labolatory_number in data.keys():
                for key in data[labolatory_number]["modified_data"]:
                    if data[labolatory_number]["origin_data"][key] and (
                            data[labolatory_number]["origin_data"][key] != data[labolatory_number]["modified_data"][
                            key]):
                        cell = PhysicalPropertyParams[key][1] + str(
                            data[labolatory_number]["origin_data"][key]["sample_number"] + 6)
                        wb[sheet][cell] = data[labolatory_number]["modified_data"][key]
            wb.save(path)'''

        wb = xlrd.open_workbook(self.excel_path, formatting_info=True)
        out_wb = copy(wb)
        sheet = out_wb.get_sheet(0)

        for labolatory_number in data.keys():
            string = self[labolatory_number].sample_number + 6
            for key in data[labolatory_number]["modified_data"]:
                modified_value = data[labolatory_number]["modified_data"][key]
                original_value = data[labolatory_number]["origin_data"][key]
                if modified_value and (original_value != modified_value):
                    column = PhysicalPropertyParams[key][1]
                    sheet.write(string, column, modified_value)

        out_wb.save(path)

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



if __name__ == "__main__":
    s = Statment()
    #s.setExcelFile('/Users/mac1/Desktop/projects/databases/511-21 ул. Красного Маяка, 26- мех-2.xls')
    s.setExcelFile('C:/Users/Пользователь/Desktop/test/ПРОВЕРКА скальники.xls')
    s.setRandom(random_params, ["Р45-12"])
    print(s.getData())
    excel_path = '/Users/mac1/Desktop/projects/databases/511-21 ул. Красного Маяка, 26- мех-2.xls'
