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

from app.model.properties_params import PhysicalPropertyParams
from app.model.ground_type_identifier import define_type_ground

class RandomType(Enum):
    PERCENT = "PERCENT"
    ABSOLUTE = "ABSOLUTE"
    ABSOLUTE_BETWEEN = "ABSOLUTE_BETWEEN"

class DataTypeValidation:
    """Дескриптор для валидации данных

    Проверяет значение на соответствие заданному типу, в случае несовпадения пытается привести к заданному
    типу. При невозможности приведения к типу возбуждает ValueError
    """
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
                    raise ValueError(f"value of '{self.attr}' is '{value}' ({str(type(value))}), it's type must be {str(self.data_type)}")

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get(self.attr, None)

class PhysicalProperties:
    borehole = DataTypeValidation(str)
    depth = DataTypeValidation(int)
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
    slope_angle_dry = DataTypeValidation(int)
    slope_angle_wet = DataTypeValidation(int)
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
    type_ground = DataTypeValidation(str)
    ground_name = DataTypeValidation(str)

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
    slope_angle_dry_modified = DataTypeValidation(int)
    slope_angle_wet_modified = DataTypeValidation(int)
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
    type_ground_modified = DataTypeValidation(str)

    def __init__(self):
        for key in PhysicalProperties.__dict__:
            if isinstance(getattr(PhysicalProperties, key), DataTypeValidation):
                object.__setattr__(self, key, None)

    def defineProperties(self, data_frame: pd.DataFrame, number: int) -> None:
        """Считывание строки свойств

            :argument data_frame: dataframe excel файла ведомости
            :argument number: номер строки пробы в dataframe
            :return None
        """
        for attr_name in PhysicalPropertyParams:
            setattr(self, attr_name, PhysicalProperties.float_df(
                data_frame.iat[number, PhysicalPropertyParams[attr_name][1]])
                    )
        self.sample_number = number
        self.type_ground = define_type_ground(self._granDict(), self.Ir, self.Ip, self.e, self.Il)

        for key in PhysicalProperties.__dict__:
            if "modified" in key:
                object.__setattr__(self, key, getattr(self, key[:-9]))

    def setRandom(self, random_params: Dict[str, Dict[str, Union[str, float]]]) -> bool:
        """Наложения рандома

        Для каждого параметра начинается проход по 100 циклов.
        Если за 100 циклов не получилось получить рандом,
        удовлетворяющий условиям (не меняется тип грунта, e меняется в пределах 0.05), то
        decrease_parameter увеличивается на 1 (данный параметр уменьшает величину приращения).
        Если за 1000 прохождений не удалось получить результат, то возвращается False и устанавливаются
        оригинальные значения

            :argument random_params: словарь рандомных параметров
            :return успешность выпоненния функции
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

            cycles_count = 100
            decrease_parameter = 1
            between = True if random_params[param]["type"] == RandomType.ABSOLUTE_BETWEEN else False

            count = 0
            done = True

            while done:
                if param == "granulometric":
                    self._randomGran(granKeys, (random_params[param]["value"]) / decrease_parameter)
                elif param == "granulometric_areometer":
                    self._randomGran(granKeysAreometer, random_params[param]["value"] / decrease_parameter)
                else:
                    self._randomParam(
                        param_name=param,
                        param_type=random_params[param]["type"],
                        param_value=random_params[param]["value"] / decrease_parameter if not between else
                        random_params[param]["value"]
                    )
                    if self.Wp and self.Wl:
                        while self.Wp_modified == self.Wl_modified:
                            self._randomParam(
                                param_name=param,
                                param_type=random_params[param]["type"],
                                param_value=random_params[param]["value"] / decrease_parameter if not between else
                                random_params[param]["value"]
                            )

                    if param not in ["rd_min", "rd_max", "Kf_min", "Kf_max", "slope_angle_dry", "slope_angle_wet"]:
                        self._reCalculateProperties()

                self.type_ground_modified = define_type_ground(
                    self._granDictModified(), self.Ir_modified, self.Ip_modified, self.e_modified, self.Il_modified)

                e_condition = (self.e - 0.05 < self.e_modified < self.e + 0.05) if self.e else True
                Sr_condition = (self.Sr_modified <= 1) if self.Sr else True

                if self.type_ground == self.type_ground_modified and e_condition and Sr_condition:
                    done = False
                else:
                    cycles_count -= 1

                if cycles_count == 0:
                    decrease_parameter += 1
                    cycles_count = 100

                count += 1
                if count >= 10000:
                    for key in PhysicalProperties.__dict__:
                        if "modified" in key:
                            object.__setattr__(self, key, getattr(self, key[:-9]))
                    return False
        return True

    def _randomParam(self, param_name: str, param_type: str, param_value: float) -> None:
        """Получение значений рандомного параметра для заданных значений

            :argument param_name: имя параметра
            :argument param_type: тип вариации параметра (проценты, абсолютное значение, диапазон)
            :argument param_value: значение оригинального параметра
            :return None
        """
        original_value = getattr(self, param_name)
        if original_value:
            if param_type == RandomType.PERCENT:
                random_value = original_value * np.random.uniform(
                    1 - param_value / 100, 1 + param_value / 100)

            elif param_type == RandomType.ABSOLUTE:
                random_value = original_value + np.random.uniform(
                    param_value, -param_value)

            elif param_type == RandomType.ABSOLUTE_BETWEEN:
                random_value = np.random.uniform(param_value[0], param_value[1])

            accuracy = Decimal(str(original_value)).as_tuple().exponent * (-1)

            setattr(self, f'{param_name}_modified', np.round(random_value, accuracy))

    def _granDict(self) -> dict:
        """Получение словаря с грансоставом оригинальных значний

            :return словарь со значениями грансостава по ключам
        """
        data_gran = {}
        for key in ['10', '5', '2', '1', '05', '025', '01', '005', '001', '0002', '0000']:
            data_gran[key] = getattr(self, f"granulometric_{key}")
        return data_gran

    def _granDictModified(self) -> dict:
        """Получение словаря с грансоставом модифицированных значний

            :return словарь со значениями грансостава по ключам
        """
        data_gran = {}
        for key in ['10', '5', '2', '1', '05', '025', '01', '005', '001', '0002', '0000']:
            data_gran[key] = getattr(self, f"granulometric_{key}_modified")
        return data_gran

    def _reCalculateProperties(self) -> None:
        """Пересчет свойств грунтов при изменении ключевых параметров

        Изменяемые параметры:
            rs, r, W, WL, WP, Угол откоса, rd_min, rd_max, Kf_min, Kf_max, Ir

        Пересчитываемые параметры:
            rd, e, n, Ip, Il, Sr

            :return None
        """
        if self.r:
            self.rd_modified = PhysicalProperties.define_rd(self.r_modified, self.W_modified)
            self.Sr_modified = PhysicalProperties.define_Sr(self.W_modified, self.rd_modified,
                                                            self.n_modified)
            self.e_modified = PhysicalProperties.define_e(self.rs_modified, self.rd_modified)
            self.n_modified = PhysicalProperties.define_n(self.e_modified)

        if self.Ip and self.Ip:
            self.Ip_modified = PhysicalProperties.define_Ip(self.Wl_modified, self.Wp_modified)
            self.Il_modified = PhysicalProperties.define_Il(self.W_modified, self.Wl_modified,
                                                            self.Wp_modified)

    def _randomGran(self, keys, percent) -> None:
        """Наложение рандома на грансостав

        Функция накладывает рандом на гран состав, при этом считая общий баланс грансостава (должно быть 100%).
        После наложения рандома остаточный дисбаланс перекидывается на пустые ячейки справа или слева, далее
        расчитывается дисбаланс еще раз, цикл прекращается при общем дисбалансе < 0.01

            :argument keys: ключи для применения функции. Используются для отделения ареометра
            :argument percent: процент ихменения для вариации параметров
            :return None
        """
        left_zero_key = None
        right_zero_key = None
        change = False

        balance = self._calculateGranBalance()
        if balance == 100.:
            return

        if not sum([getattr(self, key) for key in keys if getattr(self, key)]):
            return

        while True:
            balance = -1
            while balance < 0:
                for key in keys:
                    value = getattr(self, key[:-9])
                    if value:
                        val = np.round(np.random.uniform(value - (value * percent / 100), value + (value * percent / 100)), 1)
                        setattr(self, key, float('{:.1f}'.format(val)) if (val or val == 0.0) else None)
                    else:
                        if change:
                            right_zero_key = key
                        else:
                            left_zero_key = key
                balance = float('{:.1f}'.format(self._calculateGranBalance()))

            keys_for_set_disbalance = None

            if left_zero_key and right_zero_key:
                keys_for_set_disbalance = keys[keys.index(left_zero_key) + 1: keys.index(right_zero_key)]
                if np.round(np.random.uniform(0, 1)):
                    left_zero_key = None
                else:
                    right_zero_key = None

            if left_zero_key or right_zero_key:
                if keys_for_set_disbalance is None:
                    keys_for_set_disbalance = keys[keys.index(left_zero_key) + 1:] if left_zero_key else keys[: keys.index(right_zero_key)]

                limit = min(
                    [
                        balance,
                        getattr(self, keys[keys.index(left_zero_key) + 1]) if left_zero_key else getattr(self, keys[
                            keys.index(right_zero_key)]),
                        0.5
                    ]
                )

                val = np.round(np.random.uniform(0, limit), 1)
                setattr(self,
                        left_zero_key if left_zero_key else right_zero_key,
                        float('{:.1f}'.format(val)) if val else None)

                balance = float('{:.1f}'.format(self._calculateGranBalance()))
                key = np.random.choice(keys_for_set_disbalance)
                setattr(self, key, float('{:.1f}'.format(np.round(getattr(self, key) + balance, 1))))

            else:
                key = np.random.choice(keys)
                setattr(self, key, float('{:.1f}'.format(np.round(getattr(self, key) + balance, 1))))

            balance = float('{:.1f}'.format(self._calculateGranBalance()))

            if abs(balance) <= 0.01:
                break

    def _calculateGranBalance(self) -> float:
        """Расчет остатка процентов по грансоставу

        Возвращает 100, если грансостав не задан

            :return float
        """
        return 100. - sum(
            [value for value in [
                self.granulometric_10_modified, self.granulometric_5_modified, self.granulometric_2_modified,
                self.granulometric_1_modified, self.granulometric_05_modified, self.granulometric_025_modified,
                self.granulometric_01_modified, self.granulometric_005_modified, self.granulometric_001_modified,
                self.granulometric_0002_modified, self.granulometric_0000_modified
            ] if value]
        )

    def getData(self) -> dict:
        """Получение всех параметров

            :return словарь с оригинальными зачениями параметров по ключу origin_data и измененными по ключу modified_data
        """
        return {
            "origin_data": {
                attr_name: self.__dict__[attr_name] for attr_name in self.__dict__
                if "modified" not in attr_name
            },
            "modified_data": {
                attr_name[:-9]: self.__dict__[attr_name] for attr_name in self.__dict__ if "modified" in attr_name}
        }

    def __repr__(self):
        origin_data = ', '.join([f'{attr_name}: {self.__dict__[attr_name]}' for attr_name in self.__dict__ if "modified" not in attr_name and "headler" not in attr_name])
        modified_data = ', '.join([f'{attr_name[:-9]}: {self.__dict__[attr_name]}' for attr_name in self.__dict__ if "modified" in attr_name])
        return f"""
    Исходные данные:
        {origin_data}
    Модифицированные данные:
        {modified_data}
        """

    @staticmethod
    def define_rd(r: float, W: float) -> float:
        """Функция определения плотности сухого грунта

            :argument r: плотность грунта, г/см3
            :argument W: влажность
            :return rd, г/см3
        """
        return np.round(r / (1 + (W / 100)), 2)

    @staticmethod
    def define_e(rs: float, rd: float) -> float:
        """Функция определения коэффициента пористости

            :argument rs: плотность частиц грунта, г/см3
            :argument rd: плотность сухого грунта, г/см3
            :return коэффициент пористости
        """
        return np.round((rs - rd) / rd, 2)

    @staticmethod
    def define_n(e: float) -> float:
        """Функция определения пористости

            :argument e: плотность частиц грунта, г/см3
            :return пористость
        """
        return np.round((e / (1 + e)) * 100, 1)

    @staticmethod
    def define_Ip(Wl: float, Wp: float) -> float:
        """Функция определения числа сластичности

            :argument Wl: граница текучести, %
            :argument Wp: граница раскатывания, %
            :return число пластичности
        """
        return np.round(Wl - Wp, 2)

    @staticmethod
    def define_Il(W: float, Wl: float, Wp: float) -> float:
        """Функция определения показателя текучести

            :argument W: влажность, %
            :argument Wl: граница текучести, %
            :argument Wp: граница раскатывания, %
            :return показатель текучести
        """
        return np.round((W - Wp) / (Wl - Wp), 2)

    @staticmethod
    def define_Sr(W: float, rd: float, n: float) -> float:
        """Функция определения степени влажности

            :argument W: влажность, %
            :argument rd: плотность сухого грунта, г/см3
            :argument n: пористость
            :return степень влажности
        """
        return np.round(W * rd / n, 2)

    @staticmethod
    def float_df(x) -> Union[float, None]:
        """Функия преобразования ячейки dataframe в значение

            :argument x: значение яцейки
            :return float или None
        """
        return None if str(x) in ["nan", "NaT"] else x

    @staticmethod
    def random(percent):
        return np.random.uniform(1 - percent, 1 + percent)