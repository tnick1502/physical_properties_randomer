import pandas as pd
import os

from property_model import PhysicalProperties, RandomType

random_params = {
    "rs": {
        "type": RandomType.PERCENT,
        "value": 20
    },
    "r": {
        "type": RandomType.PERCENT,
        "value": 20
    },
    "rd": {
        "type": RandomType.PERCENT,
        "value": 20
    },
    "n": {
        "type": RandomType.PERCENT,
        "value": 20
    },
    "e": {
        "type": RandomType.PERCENT,
        "value": 20
    },
    "W": {
        "type": RandomType.PERCENT,
        "value": 20
    },
    "Sr": {
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
    "Ip": {
        "type": RandomType.PERCENT,
        "value": 20
    },
    "Il": {
        "type": RandomType.PERCENT,
        "value": 20
    },
    "Ir": {
        "type": RandomType.PERCENT,
        "value": 20
    },
    "granulometric": {
        "type": RandomType.PERCENT,
        "value": 20
    },
}

class Statment:
    data: dict = {}
    excel_path: str = ''
    dataframe: pd.DataFrame

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

    def setRandom(self):
        for key in self.data:
            self.data[key].setRandom(random_params)

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
    s.setExcelFile('/Users/mac1/Desktop/projects/databases/511-21 ул. Красного Маяка, 26- мех-2.xls')
    print(s)