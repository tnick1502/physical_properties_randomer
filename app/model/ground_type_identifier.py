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

    if type_ground_A in ["D", "E", "F", "G", "H", "I", "J", "R", "K", "L", "M", "N", "S", "O", "P", "Q", "T"]:
        type_ground_D = define_organic(type_ground_A, Ir)
    else:
        type_ground_D = "-"

    '''accumulate_gran_big = 0
    for i in gran_struct[:3]:
        accumulate_gran_big += none_to_zero(data_gran[i])

    elif (Ip >= 1) and (15 <= accumulate_gran_big <= 25):
        type_ground = 15  # Супесь, суглинок, глина с галькой (щебнем), с гравием (дресвой) или ракушкой

    elif (Ip >= 1) and (25 < accumulate_gran_big <= 50):
        type_ground = 16  # Супесь, суглинок, глина галечниковые (щебенистые), гравелистые (дресвяные) или ракушечные'''

    return type_ground_A + type_ground_B + type_ground_С + type_ground_D

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
    Ip = none_to_zero(Ip)
    Ir = none_to_zero(Ir)

    if Ir >= 50:
        return "U"  # Торф

    if accumulate_gran(data_gran, ['10']) > 50:
        return "A"  # Щебень
    elif accumulate_gran(data_gran, ['10', '5', '2']) > 50:
        return "B"  # Дресва

    if 1 <= Ip <= 7:
        if accumulate_gran(data_gran, ['2', '1', '05', '025', '01', '005']) == 0:
            return "R"  # Супесь
        elif accumulate_gran(data_gran, ['2', '1', '05', '025', '01', '005']) >= 50:
            return "I"  # Супесь песчанистая
        elif accumulate_gran(data_gran, ['2', '1', '05', '025', '01', '005']) < 50:
            return "J"  # Супесь пылеватая

    elif 7 < Ip <= 17:
        if accumulate_gran(data_gran, ['2', '1', '05', '025', '01', '005']) == 0:
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
        elif accumulate_gran(data_gran, ['2', '1', '05', '025', '01', '005']) == 0:
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
            if accumulate_gran(data_gran, ['2']) > accumulate_gran(data_gran, ['5']):
                return "B"
            else:
                return "A"
        elif 25 < accumulate_gran(data_gran, ['10', '5', '2']) <= 50:
            if accumulate_gran(data_gran, ['2']) > accumulate_gran(data_gran, ['5']):
                return "F"
            else:
                return "E"

    elif type in ["K", "L", "M", "N", "S"]:
        if 15 <= accumulate_gran(data_gran, ['10', '5', '2']) <= 25:
            if accumulate_gran(data_gran, ['2']) > accumulate_gran(data_gran, ['5']):
                return "B"
            else:
                return "A"
        elif 25 < accumulate_gran(data_gran, ['10', '5', '2']) <= 50:
            if accumulate_gran(data_gran, ['2']) > accumulate_gran(data_gran, ['5']):
                return "D"
            else:
                return "C"

    if type in ["A", "B", "C"]:
        if accumulate_gran(data_gran, ['1', '05', '025', '01', "005", "001", "0002", "0000"]) >= 30:
            if 1 <= Ip <= 7:
                return "H"  # с супесью
            elif 7 < Ip <= 17:
                return "I"  # с суглинком
            elif Ip > 17:
                return "J"  # с глиной
        elif accumulate_gran(data_gran, ['1', '05', '025', '01']) >= 40:
            return "G"  # с песком

    return "-"


    raise ValueError("Can't define organic ground type")

def convert_type_to_name(type_ground: str):
    A, B, C, D = list(type_ground)
    A = GroundTypes[A]
    B = " " + GroundTypes_B.get(B, None) if GroundTypes_B.get(B, None) else ""
    C = " " + GroundTypes_C.get(C, None) if GroundTypes_C.get(C, None) else ""
    D = " " + GroundTypes_D.get(D, None) if GroundTypes_D.get(D, None) else ""

    return A + B + C + D

GroundTypes = {
    "A": "Щебень",
    "B": "Дресва",
    "C": "Грунт дресвяно-щебенистый",
    "D": "Песок гравелистый",
    "E": "Песок крупный",
    "F": "Песок средней крупности",
    "G": "Песок мелкий",
    "H": "Песок пылеватый",
    "I": "Супесь песчанистая",
    "J": "Супесь пылеватая",
    "K": "Суглинок легкий песчанистый",
    "L": "Суглинок тяжелый песчанистый",
    "M": "Суглинок легкий пылеватый",
    "N": "Суглинок тяжелый пылеватый",
    "O": "Глина легкая песчанистая",
    "P": "Глина легкая пылеватая",
    "Q": "Глина тяжелая",
    "R": "Супесь",
    "S": "Суглинок",
    "T": "Глина",
    "U": "Торф",
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
    "A": "с щебнем",
    "B": "с дресвой",
    "C": "щебенистый",
    "D": "дресвяный",
    "E": "щебенистая",
    "F": "дресвяная",
    "G": "с песком",
    "H": "с супесью",
    "I": "с суглинком",
    "J": "с глиной",
}

GroundTypes_D = {
    "A": "с примесью органического вещества",
    "B": "с низким содержанием органического вещества",
    "C": "со средним содержанием органического вещества",
    "D": "с высоким содержанием органического вещества",
}





