"""Модуль построения модели свойств

Каждое свойство проходит валидацию DataTypeValidation

Для использования создается экземпляр класса. Далее для него вызывается метод defineProperties, 
который определит все параметры из датафрейма, а модифицированным параметрам присвоит значение текущих.

Метод setRandom изменяет значение всех модифицированных параметров по передаваемым заканам изменения. 
Внури метода происходит проверка на несоответствие текущему типу грунта и на отклонение значения e более чем на 0.05


Изменяемые параметры:
    rs, r, W, WL, WP, Угол откоса, rd_min, rd_max, Kf_min, Kf_max, Ir

Пересчитываемые параметры:
    rd, e, n, Ip, Il, Sr
"""

import pandas as pd
import numpy as np
from enum import Enum
from decimal import Decimal
from typing import Dict, Union

from properties_params import PhysicalPropertyParams

class RandomType(Enum):
    PERCENT = "PERCENT"
    ABSOLUTE = "ABSOLUTE"

class DataTypeValidation:
    """Data type validation"""
    data_type: object = None

    def __init__(self, *args):
        self.data_type = args[0]

    def __set_name__(self, owner, name):
        self.attr = name

    def __set__(self, instance, value):
        if value is None:
            instance.__dict__[self.attr] = value
        else:
            if isinstance(value, self.data_type):
                instance.__dict__[self.attr] = value
            else:
                try:
                    instance.__dict__[self.attr] = self.data_type(value)
                except:
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
    rd_min = DataTypeValidation(float)
    rd_max = DataTypeValidation(float)
    Kf_min = DataTypeValidation(float)
    Kf_max = DataTypeValidation(float)
    slope_angle_dry = DataTypeValidation(float)
    slope_angle_wet = DataTypeValidation(float)
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
    rd_min_modified = DataTypeValidation(float)
    rd_max_modified = DataTypeValidation(float)
    Kf_min_modified = DataTypeValidation(float)
    Kf_max_modified = DataTypeValidation(float)
    slope_angle_dry_modified = DataTypeValidation(float)
    slope_angle_wet_modified = DataTypeValidation(float)
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

    def __init__(self, headler=None):
        if not headler:
            self.headler = lambda: None
        else:
            self.headler = headler

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

        for key in PhysicalProperties.__dict__:
            if "modified" in key:
                object.__setattr__(self, key, getattr(self, key[:-9]))

    def setRandom(self, random_params: Dict[str, Dict[str, Union[str, float]]]):
        """Функция наложения рандома

        Для каждого параметра начинается проход по 10 циклов.
        Если за 10 циклов не получилось получить рандом,
        удовлетворяющий условиям (не меняется тип грунта, e меняется в пределах 0.05), то
        decrease_parameter увеличивается на 1 (данный параметр уменьшает величину приращения)

        """

        granKeys = [
            "granulometric_10_modified", "granulometric_5_modified", "granulometric_2_modified",
            "granulometric_1_modified", "granulometric_05_modified", "granulometric_025_modified",
            "granulometric_01_modified", "granulometric_005_modified"
        ]

        granKeysAreometer = [
            "granulometric_001_modified", "granulometric_0002_modified", "granulometric_0000_modified"
        ]

        for param in random_params:

            cycles_count = 10
            decrease_parameter = 1

            while True:
                if param == "granulometric":
                    self.randomGran(granKeys, (random_params[param]["value"]) / decrease_parameter)
                elif param == "granulometric_areometer":
                    self.randomGran(granKeysAreometer, random_params[param]["value"] / decrease_parameter)
                else:
                    self.randomParam(
                        param_name=param,
                        param_type=random_params[param]["type"],
                        param_value=random_params[param]["value"] / decrease_parameter
                    )

                    if param not in ["rd_min", "rd_max", "Kf_min", "Kf_max", "slope_angle_dry", "slope_angle_wet"]:
                        self.reCalculateProperties()

                type_ground = PhysicalProperties.define_type_ground(
                    self.granDictModified(), self.Ir_modified, self.Ip_modified)

                if self.type_ground == type_ground and (
                        (self.e - 0.05 < self.e_modified < self.e + 0.05) if self.e else True
                ):
                    break
                else:
                    cycles_count -= 1

                if cycles_count == 0:
                    decrease_parameter += 1
                    cycles_count = 10

    def randomParam(self, param_name: str, param_type: str, param_value: float):
        """Получение значений рандомного параметра для заданных значений"""
        original_value = getattr(self, param_name)
        if original_value:
            if param_type == RandomType.PERCENT:
                random_value = original_value * np.random.uniform(
                    1 - param_value / 100, 1 + param_value / 100)

            elif param_type == RandomType.ABSOLUTE:
                random_value = original_value + np.random.uniform(
                    param_value, -param_value)

            accuracy = Decimal(str(original_value)).as_tuple().exponent * (-1)

            setattr(self, f'{param_name}_modified', np.round(random_value, accuracy))

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

    def reCalculateProperties(self):
        """Пересчет свойств грунтов при изменении ключевых параметров"""
        if self.r:
            self.rd_modified = PhysicalProperties.define_rd(self.r_modified, self.W_modified)
            self.Sr_modified = PhysicalProperties.define_Sr(self.W_modified, self.r_modified,
                                                            self.n_modified)
            self.e_modified = PhysicalProperties.define_e(self.rs_modified, self.rd_modified)
            self.n_modified = PhysicalProperties.define_n(self.e_modified)

        if self.Ip and self.Ip:
            self.Ip_modified = PhysicalProperties.define_Ip(self.Wl_modified, self.Wp_modified)
            self.Il_modified = PhysicalProperties.define_Il(self.W_modified, self.Wl_modified,
                                                            self.Wp_modified)

    def randomGran(self, keys, percent):
        left_zero_key = None
        right_zero_key = None
        change = False

        balance = self.calculateGranBalance()
        if balance == 100.:
            return
        else:
            balance = -1

        while balance < 0:
            for key in keys:
                value = getattr(self, key)
                if value:
                    if percent >= value:
                        setattr(self, key, np.round(np.random.uniform(0, value + percent), 1))
                    else:
                        setattr(self, key, np.round(np.random.uniform(value - percent, value + percent), 1))
                else:
                    if change:
                        right_zero_key = key
                    else:
                        left_zero_key = key

            balance = self.calculateGranBalance()

        zero_keys = [key for key in [left_zero_key, right_zero_key] if key]

        if len(zero_keys):
            setattr(self, np.random.choice(zero_keys), balance)
        else:
            key = np.random.choice(keys)
            print(key)
            setattr(self, key, getattr(self, key) + balance)

    def calculateGranBalance(self):
        """Расчет остатка процентов по грансоставу, чтобы суммарно было 100"""
        return 100. - sum(
            [value for value in [
                self.granulometric_10_modified, self.granulometric_5_modified, self.granulometric_2_modified,
                self.granulometric_1_modified, self.granulometric_05_modified, self.granulometric_025_modified,
                self.granulometric_01_modified, self.granulometric_005_modified, self.granulometric_001_modified,
                self.granulometric_0002_modified, self.granulometric_0000_modified
            ] if value]
        )

    def __repr__(self):
        origin_data = ', '.join([f'{attr_name}: {self.__dict__[attr_name]}' for attr_name in self.__dict__ if "modified" not in attr_name and "headler" not in attr_name])
        modified_data = ', '.join([f'{attr_name[:-9]}: {self.__dict__[attr_name]}' for attr_name in self.__dict__ if "modified" in attr_name])
        return f"""
    Исходные данные:
        {origin_data}
    Модифицированные данные:
        {modified_data}
        """

    def __setattr__(self, key, value):
        if "modified" in key:
            self.headler()
        object.__setattr__(self, key, value)


    @staticmethod
    def define_type_ground(data_gran: dict, Ir: float, Ip: float) -> int:
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
    def define_rd(r: float, W: float) -> float:
        return np.round(r / (1 + (W / 100)), 2)

    @staticmethod
    def define_e(rs: float, rd: float) -> float:
        return np.round((rs - rd) / rd, 2)

    @staticmethod
    def define_n(e: float) -> float:
        return np.round((e / (1 + e)) * 100, 1)

    @staticmethod
    def define_Ip(Wl: float, Wp: float) -> float:
        return np.round(Wl - Wp, 2)

    @staticmethod
    def define_Il(W: float, Wl: float, Wp: float) -> float:
        return np.round((W - Wp) / (Wl - Wp), 2)

    @staticmethod
    def define_Sr(W: float, r: float, n: float) -> float:
        return np.round((W * r) / (n * (1 + W)), 2)

    @staticmethod
    def float_df(x):
        return None if str(x) in ["nan", "NaT"] else x

    @staticmethod
    def random(percent):
        return np.random.uniform(1 - percent, 1 + percent)