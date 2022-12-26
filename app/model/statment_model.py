import pandas as pd
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

    def setExcelFile(self, path: str):
        """Открытие файла excel"""
        if not all([os.path.exists(path), (path.endswith('.xls') or path.endswith('.xlss'))]):
            raise Exception("Wrong file excel")

        self.excel_path = path

        df = pd.read_excel(self.excel_path, usecols="A:IV", skiprows=[0, 1, 3, 4, 5])
        self.dataframe = df[df['Лаб. № пробы'].notna()]

        for i, laboratory_number in enumerate(self.dataframe["Лаб. № пробы"]):
            self.data[laboratory_number] = PhysicalProperties()
            self.data[laboratory_number].defineProperties(data_frame=self.dataframe, number=i)

    def setRandom(self, params, keys):
        problem_keys = []
        for key in keys:
            res = self.data[key].setRandom(params)
            if not res:
                problem_keys.append(key)
        return problem_keys

    def getData(self):
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



if __name__ == "__main__":
    s = Statment()
    #s.setExcelFile('/Users/mac1/Desktop/projects/databases/511-21 ул. Красного Маяка, 26- мех-2.xls')
    s.setExcelFile('C:/Users/Пользователь/Desktop/test/test.xls')
    s.setRandom()
    print(s.getData())