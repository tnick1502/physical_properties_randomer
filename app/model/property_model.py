import pandas as pd
import numpy as np
from enum import Enum
from decimal import Decimal
from typing import Dict, Union

from properties_params import PhysicalPropertyParams

class RandomType(Enum):
    PERCENT = "PERCENT"
    ABSOLUTE = "ABSOLUTE"

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

class DataTypeValidation:
    """Data type validation"""
    def __init__(self, *args):
        self.data_types = args

    def __set_name__(self, owner, name):
        self.attr = name

    def __set__(self, instance, value):
        if value is None:
            instance.__dict__[self.attr] = value
        elif any(isinstance(value, i) for i in self.data_types):
            instance.__dict__[self.attr] = value
        else:
            raise ValueError(f"{value} typy must be in {str(self.data_types)}, but it is {str(type(value))}")

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get(self.attr, None)

class PhysicalProperties:
    rs = DataTypeValidation(float)
    r = DataTypeValidation(float)
    rd = DataTypeValidation(float)
    n = DataTypeValidation(float)
    e = DataTypeValidation(float)
    W = DataTypeValidation(float)
    Sr = DataTypeValidation(float)
    Wl = DataTypeValidation(float)
    Wp = DataTypeValidation(float)
    Ip = DataTypeValidation(float)
    Il = DataTypeValidation(float)
    Ir = DataTypeValidation(float)
    granulometric_10 = DataTypeValidation(float)
    granulometric_5 = DataTypeValidation(float)
    granulometric_2 = DataTypeValidation(float)
    granulometric_1 = DataTypeValidation(float)
    granulometric_05 = DataTypeValidation(float)
    granulometric_025 = DataTypeValidation(float)
    granulometric_01 = DataTypeValidation(float)
    granulometric_005 = DataTypeValidation(float)
    granulometric_001 = DataTypeValidation(float)
    granulometric_0002 = DataTypeValidation(float)
    granulometric_0000 = DataTypeValidation(float)
    sample_number = DataTypeValidation(int)
    type_ground = DataTypeValidation(int)

    rs_modified = DataTypeValidation(float)
    r_modified = DataTypeValidation(float)
    rd_modified = DataTypeValidation(float)
    n_modified = DataTypeValidation(float)
    e_modified = DataTypeValidation(float)
    W_modified = DataTypeValidation(float)
    Sr_modified = DataTypeValidation(float)
    Wl_modified = DataTypeValidation(float)
    Wp_modified = DataTypeValidation(float)
    Ip_modified = DataTypeValidation(float)
    Il_modified = DataTypeValidation(float)
    Ir_modified = DataTypeValidation(float)
    granulometric_10_modified = DataTypeValidation(float)
    granulometric_5_modified = DataTypeValidation(float)
    granulometric_2_modified = DataTypeValidation(float)
    granulometric_1_modified = DataTypeValidation(float)
    granulometric_05_modified = DataTypeValidation(float)
    granulometric_025_modified = DataTypeValidation(float)
    granulometric_01_modified = DataTypeValidation(float)
    granulometric_005_modified = DataTypeValidation(float)
    granulometric_001_modified = DataTypeValidation(float)
    granulometric_0002_modified = DataTypeValidation(float)
    granulometric_0000_modified = DataTypeValidation(float)

    def __init__(self):
        for key in PhysicalProperties.__dict__:
            if isinstance(getattr(PhysicalProperties, key), DataTypeValidation):
                object.__setattr__(self, key, None)

    def defineProperties(self, data_frame: pd.DataFrame, number: int) -> None:
        """Считывание строки свойств"""
        for attr_name in PhysicalPropertyParams:
            setattr(self, attr_name, PhysicalProperties.float_df(
                data_frame.iat[number, PhysicalPropertyParams[attr_name][1]])
                    )
        self.sample_number = number
        self.type_ground = PhysicalProperties.define_type_ground(self.granDict(), self.Ir, self.Ip)

    def granDict(self):
        data_gran = {}
        for key in ['10', '5', '2', '1', '05', '025', '01', '005', '001', '0002', '0000']:
            data_gran[key] = getattr(self, f"granulometric_{key}")
        return data_gran

    def granDictModified(self):
        data_gran = {}
        for key in ['10', '5', '2', '1', '05', '025', '01', '005', '001', '0002', '0000']:
            data_gran[key] = getattr(self, f"granulometric_{key}_modified")
        return data_gran

    def setRandom(self, random_params: Dict[str, Dict[str, Union[str, float]]]):
        for param in random_params:
            if param != "granulometric":
                original_value = getattr(self, param)
                if original_value:
                    if random_params[param]["type"] == RandomType.PERCENT:
                        random_value = original_value * np.random.uniform(
                            1 - random_params[param]["value"]/100, 1 + random_params[param]["value"]/100)
                    elif random_params[param]["type"] == RandomType.ABSOLUTE:
                        random_value = original_value + np.random.uniform(
                            random_params[param]["value"], -random_params[param]["value"])

                    accuracy = Decimal(str(original_value)).as_tuple().exponent*(-1)

                    setattr(self, f'{param}_modified', np.round(random_value, accuracy))

                    #self.granDictModified()

                    print(self.type_ground == PhysicalProperties.define_type_ground(self.granDictModified(), self.Ir_modified, self.Ip_modified))



    def __repr__(self):
        origin_data = ', '.join([f'{attr_name}: {self.__dict__[attr_name]}' for attr_name in self.__dict__ if "modified" not in attr_name])
        modified_data = ', '.join([f'{attr_name}: {self.__dict__[attr_name]}' for attr_name in self.__dict__ if "modified" in attr_name])
        return f"""
    Исходные данные:
        {origin_data}
    Модифицированные данные:
        {modified_data}
        """

    @staticmethod
    def define_type_ground(data_gran, Ir, Ip) -> int:
        """Функция определения типа грунта через грансостав"""
        none_to_zero = lambda x: 0 if not x else x

        gran_struct = ['10', '5', '2', '1', '05', '025', '01', '005', '001', '0002', '0000']  # гран состав
        accumulate_gran = [none_to_zero(data_gran[gran_struct[0]])]  # Накоплено процентное содержание
        for i in range(10):
            accumulate_gran.append(accumulate_gran[i] + none_to_zero(data_gran[gran_struct[i + 1]]))

        if none_to_zero(Ir) >= 50:  # содержание органического вещества Iom=hg10=Ir
            type_ground = 9  # Торф
        elif none_to_zero(Ip) < 1:  # число пластичности
            if accumulate_gran[2] > 25:
                type_ground = 1  # Песок гравелистый
            elif accumulate_gran[4] > 50:
                type_ground = 2  # Песок крупный
            elif accumulate_gran[5] > 50:
                type_ground = 3  # Песок средней крупности
            elif accumulate_gran[6] >= 75:
                type_ground = 4  # Песок мелкий
            else:
                type_ground = 5  # Песок пылеватый
        elif 1 <= Ip < 7:
            type_ground = 6  # Супесь
        elif 7 <= Ip < 17:
            type_ground = 7  # Суглинок
        else:  # data['Ip'] >= 17:
            type_ground = 8  # Глина

        return type_ground

    @staticmethod
    def float_df(x):
        return None if str(x) in ["nan", "NaT"] else x



