

def define_type_ground(data_gran: dict, Ir: float, Ip: float, e: float, Il: float) -> int:
    """Функция определения типа грунта через грансостав

        :argument data_gran: словарь грансостава, полуенный из granDict или granDictModified
        :argument Ir: содержание органики
        :argument Ip: число пластичности
        :argument e: коэффициент пористости
        :argument Il: Индекс текучести
        :return тип грунта
    """
    type_ground_A = define_main_type(data_gran, Ir, Ip)

    if type_ground_A == "Z":
        return "Z---"

    if type_ground_A in ["D", "E", "F", "G", "H"]:
        type_ground_B = define_sand_stack(type_ground_A, e)
    elif type_ground_A in ["I", "J", "R", "K", "L", "M", "N", "S", "O", "P", "Q", "T"]:
        type_ground_B = define_clay_liquid(type_ground_A, Il)
    else:
        type_ground_B = "-"

    if type_ground_A in ["A", "B", "C", "I", "J", "R", "O", "P", "Q", "T", "K", "L", "M", "N", "S"]:
        type_ground_С = define_mixed(type_ground_A, data_gran, Ip)
    else:
        type_ground_С = "-"

    if type_ground_С != "-" and type_ground_С not in GroundTypes_C.keys():
        type_ground_С = define_type_ground(recalculate_gran_without_big(data_gran), Ir, Ip, e, Il)

    if type_ground_A in ["D", "E", "F", "G", "H", "I", "J", "R", "K", "L", "M", "N", "S", "O", "P", "Q", "T"]:
        type_ground_D = define_organic(type_ground_A, Ir)
    else:
        type_ground_D = "-"

    return [type_ground_A, type_ground_B, type_ground_С, type_ground_D]

def none_to_zero(x):
    return x if x else 0

def accumulate_gran(data_gran: dict, keys: list):
    accumulate = 0
    for key in keys:
        accumulate += none_to_zero(data_gran[key])
    return accumulate

def define_main_type(data_gran: dict, Ir: float, Ip: float) -> str:
    """Функция определения типа грунта через грансостав

        :argument data_gran: словарь грансостава, полуенный из granDict или granDictModified
        :argument Ir: содержание органики
        :argument Ip: число пластичности
        :return тип грунта
    """
    if accumulate_gran(data_gran,
                       ['10', '5', '2', '1', '05', '025', '01', '005', '001', '0002', '0000']
                       ) == 0 and not Ip and not Ir:
        return "Z"

    Ip = none_to_zero(Ip)
    Ir = none_to_zero(Ir)

    if Ir >= 50:
        return "U"  # Торф

    if accumulate_gran(data_gran, ['10']) > 50:
        return "A"  # Щебень
    elif accumulate_gran(data_gran, ['10', '5', '2']) > 50:
        return "B"  # Дресва

    if 1 <= Ip <= 7:
        if accumulate_gran(data_gran, ['2', '1', '05', '025', '01', '005']) == 0 or accumulate_gran(data_gran, ['001', '0002', '0000']) == 0:
            return "R"  # Супесь
        elif accumulate_gran(data_gran, ['2', '1', '05', '025', '01', '005']) >= 50:
            return "I"  # Супесь песчанистая
        elif accumulate_gran(data_gran, ['2', '1', '05', '025', '01', '005']) < 50:
            return "J"  # Супесь пылеватая

    elif 7 < Ip <= 17:
        if accumulate_gran(data_gran, ['2', '1', '05', '025', '01', '005']) == 0 or accumulate_gran(data_gran, ['001', '0002', '0000']) == 0:
            return "S"  # Суглинок
        elif accumulate_gran(data_gran, ['2', '1', '05', '025', '01', '005']) >= 40 and (7 < Ip <= 12):
            return "K"  # Суглинок легкий песчаныстый
        elif accumulate_gran(data_gran, ['2', '1', '05', '025', '01', '005']) >= 40 and (12 < Ip <= 17):
            return "L"  # Суглинок тяжелый песчаныстый
        elif accumulate_gran(data_gran, ['2', '1', '05', '025', '01', '005']) < 40 and (7 < Ip <= 12):
            return "M"  # Суглинок легкий пылеватый
        elif accumulate_gran(data_gran, ['2', '1', '05', '025', '01', '005']) < 40 and (12 < Ip <= 17):
            return "N"  # Суглинок тяжелый пылеватый

    elif Ip > 17:
        if Ip > 27:
            return "Q"  # Глина тяжелая
        elif accumulate_gran(data_gran, ['2', '1', '05', '025', '01', '005']) == 0 or accumulate_gran(data_gran, ['001', '0002', '0000']) == 0:
            return "T"  # Глина
        elif accumulate_gran(data_gran, ['2', '1', '05', '025', '01', '005']) >= 40 and (17 < Ip <= 27):
            return "O"  # Глина легкая песчанистая
        elif accumulate_gran(data_gran, ['2', '1', '05', '025', '01', '005']) < 40 and (17 < Ip <= 27):
            return "P"  # Глина легкая пылеватая

    elif accumulate_gran(data_gran, ['10', '5', '2']) > 25:
        return "D"  # Песок гравелистый
    elif accumulate_gran(data_gran, ['10', '5', '2', '1', '05']) > 50:
        return "E"  # Песок крупный
    elif accumulate_gran(data_gran, ['10', '5', '2', '1', '05', '025']) > 50:
        return "F"  # Песок средней крупности
    elif accumulate_gran(data_gran, ['10', '5', '2', '1', '05', '025', '01']) >= 75:
        return "G"  # Песок мелкий
    elif accumulate_gran(data_gran, ['10', '5', '2', '1', '05', '025', '01']) < 75:
        return "H"  # Песок пылеватый

    raise ValueError("Can't define ground type A")

def define_sand_stack(sand_type: str, e: float) -> str:
    """Функция определения типа сложения песка

        :argument sand_type: тип песка
        :argument e: Коэффициент пористости
        :return тип грунта
    """
    if e is None:
        return "-"

    if sand_type in ["D", "E", "F"]:
        if e <= 0.55:
            return "A"  # Плотный
        elif 0.55 < e <= 70:
            return "B"  # Средней плотности
        elif e > 0.7:
            return "C"  # Рыхлый
    elif sand_type == "G":
        if e <= 0.60:
            return "A"  # Плотный
        elif 0.60 < e <= 75:
            return "B"  # Средней плотности
        elif e > 0.75:
            return "C"  # Рыхлый
    elif sand_type == "H":
        if e <= 0.60:
            return "A"  # Плотный
        elif 0.60 < e <= 80:
            return "B"  # Средней плотности
        elif e > 0.8:
            return "C"  # Рыхлый

    raise ValueError("Can't define sand stacking type")

def define_clay_liquid(type: str, Il: float) -> str:
    """Функция определения типа глинистых гругтов по показателю текучести

        :argument type: тип песка
        :argument Il: Индекс текучести
        :return тип грунта
    """
    if Il is None:
        return "-"

    if type in ["I", "J", "R"]:
        if Il < 0:
            return "D"  # Твердая
        elif 0 <= Il <= 1:
            return "E"  # Пластичная
        elif Il > 1:
            return "F"  # Текучая

    elif type in ["K", "L", "M", "N", "S"]:
        if Il < 0:
            return "G"  # Твердый
        elif 0 <= Il <= 0.25:
            return "H"  # Полутвердый
        elif 0.25 < Il <= 0.5:
            return "I"  # Тугопластичный
        elif 0.5 <= Il <= 0.75:
            return "J"  # Мягкопластичный
        elif 0.75 <= Il <= 1:
            return "K"  # Текучепластичный
        elif Il > 1:
            return "L"  # Текучий

    elif type in ["O", "P", "Q", "T"]:
        if Il < 0:
            return "M"  # Твердая
        elif 0 <= Il <= 0.25:
            return "N"  # Полутвердая
        elif 0.25 < Il <= 0.5:
            return "O"  # Тугопластичная
        elif 0.5 <= Il <= 0.75:
            return "P"  # Мягкопластичная
        elif 0.75 <= Il <= 1:
            return "Q"  # Текучепластичная
        elif Il > 1:
            return "R"  # Текучая

    raise ValueError("Can't define clay liquid ground type")

def define_organic(type: str, Ir: float) -> str:
    """Функция определения типа глинистых гругтов по показателю текучести

        :argument type: тип песка
        :argument Ir: Содержание органики
        :return тип грунта
    """
    if Ir is None:
        return "-"
    else:
        Ir /= 100

    if type in ["D", "E", "F", "G", "H"]:
        if 0.03 < Ir <= 0.10:
            return "A"  # с примесью органического вещества
        elif 0.10 < Ir <= 0.25:
            return "B"  # с низким содержанием органического вещества
        elif 0.25 < Ir <= 0.40:
            return "C"  # со средним содержанием органического вещества
        elif 0.40 < Ir < 0.50:
            return "D"  # с высоким содержанием органического вещества
        else:
            return "-"

    elif type in ["I", "J", "R", "K", "L", "M", "N", "S", "O", "P", "Q", "T"]:
        if 0.05 < Ir <= 0.10:
            return "A"  # с примесью органического вещества
        elif 0.10 < Ir <= 0.25:
            return "B"  # с низким содержанием органического вещества
        elif 0.25 < Ir <= 0.40:
            return "C"  # со средним содержанием органического вещества
        elif 0.40 < Ir < 0.50:
            return "D"  # с высоким содержанием органического вещества
        else:
            return "-"

    raise ValueError("Can't define organic ground type")

def define_mixed(type: str, data_gran: dict, Ip: float) -> str:
    """Функция определения типа глинистых гругтов по показателю текучести

        :argument data_gran: словарь грансостава, полуенный из granDict или granDictModified
        :argument type: тип песка
        :argument Ip: число пластичности
        :return тип грунта
    """
    if Ip is None:
       Ip = 0

    if type in ["I", "J", "R", "O", "P", "Q", "T"]:
        if 15 <= accumulate_gran(data_gran, ['10', '5', '2']) <= 25:
            if accumulate_gran(data_gran, ['5', '2']) > accumulate_gran(data_gran, ['10']):
                return "2"
            else:
                return "1"
        elif 25 < accumulate_gran(data_gran, ['10', '5', '2']) <= 50:
            if accumulate_gran(data_gran, ['5', '2']) > accumulate_gran(data_gran, ['10']):
                return "6"
            else:
                return "5"

    elif type in ["K", "L", "M", "N", "S"]:
        if 15 <= accumulate_gran(data_gran, ['10', '5', '2']) <= 25:
            if accumulate_gran(data_gran, ['5', '2']) > accumulate_gran(data_gran, ['10']):
                return "2"
            else:
                return "1"
        elif 25 < accumulate_gran(data_gran, ['10', '5', '2']) <= 50:
            if accumulate_gran(data_gran, ['5', '2']) > accumulate_gran(data_gran, ['10']):
                return "4"
            else:
                return "3"

    elif type in ["A", "B", "C"]:
        mix = define_main_type(recalculate_gran_without_big(data_gran), Ir=0, Ip=Ip)
        if mix in ["I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T"]:
            if accumulate_gran(data_gran, ['1', '05', '025', '01', "005", "001", "0002", "0000"]) >= 30:
                return mix
        elif mix in ["D", "E", "F", "G", "H"]:
            if accumulate_gran(data_gran, ['1', '05', '025', '01', "005", "001", "0002", "0000"]) >= 40:
                return mix

    return "-"

def recalculate_gran_without_big(data_gran: dict):
    """Функция пересчета грансостава при вычете крупнообломовочного грунта

        :argument data_gran: словарь грансостава, полуенный из granDict или granDictModified
        :return data_gran
    """
    big_keys = ['10', '5', '2']
    gran = dict(data_gran)

    big_gran = sum([gran[i] for i in big_keys if gran[i]])

    for key in big_keys:
        gran[key] = 0

    for key in gran:
        if gran[key]:
            gran[key] = (gran[key] / (100 - big_gran)) * 100

    return gran


GroundTypes = {
    "A": "грунт щебенистый",
    "B": "грунт дресвяный",
    "C": "грунт дресвяно-щебенистый",
    "D": "песок гравелистый",
    "E": "песок крупный",
    "F": "песок средней крупности",
    "G": "песок мелкий",
    "H": "песок пылеватый",
    "I": "супесь песчанистая",
    "J": "супесь пылеватая",
    "K": "суглинок легкий песчанистый",
    "L": "суглинок тяжелый песчанистый",
    "M": "суглинок легкий пылеватый",
    "N": "суглинок тяжелый пылеватый",
    "O": "глина легкая песчанистая",
    "P": "глина легкая пылеватая",
    "Q": "глина тяжелая",
    "R": "супесь",
    "S": "суглинок",
    "T": "глина",
    "U": "торф",
    "Z": "не определяется"
}

GroundTypes_B = {
    "A": "плотный",
    "B": "средней плотности",
    "C": "рыхлый",
    "D": "твердая",
    "E": "пластичная",
    "F": "текучая",
    "G": "твердый",
    "H": "полутвердый",
    "I": "тугопластичный",
    "J": "мягкопластичный",
    "K": "текучепластичный",
    "L": "текучий",
    "M": "твердая",
    "N": "полутвердая",
    "O": "тугопластичная",
    "P": "мягкопластичная",
    "Q": "текучепластичная",
    "R": "текучая",
}

GroundTypes_C = {
    "1": "с щебнем",
    "2": "с дресвой",
    "3": "щебенистый",
    "4": "дресвяный",
    "5": "щебенистая",
    "6": "дресвяная",
}

GroundTypes_D = {
    "A": "с примесью органического вещества",
    "B": "с низким содержанием органического вещества",
    "C": "со средним содержанием органического вещества",
    "D": "с высоким содержанием органического вещества",
}



