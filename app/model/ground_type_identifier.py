def define_type_ground(data_gran: dict, Ir: float, Ip: float, e: float, Il: float) -> int:
    """Функция определения типа грунта через грансостав

        :argument data_gran: словарь грансостава, полуенный из granDict или granDictModified
        :argument Ir: содержание органики
        :argument Ip: число пластичности
        :argument e: коэффициент пористости
        :argument Il: Индекс текучести
        :return тип грунта
    """
    type_ground_A = define_A(Ir, Ip)

    type_ground_B_from_A = {
        1: lambda: define_B1(data_gran),
        2: lambda: define_B2(data_gran),
        3: lambda: define_B3(data_gran, Ip),
        4: lambda: define_B4(data_gran, Ip)
    }

    type_ground_B = type_ground_B_from_A[type_ground_A]()

    type_ground_С_from_A = {
        1: lambda: define_C1(type_ground_B, e),
        2: lambda: define_C2(Il),
        3: lambda: define_C3_4(Il),
        4: lambda: define_C3_4(Il)
    }

    type_ground_C = type_ground_С_from_A[type_ground_A]()

    '''accumulate_gran_big = 0
    for i in gran_struct[:3]:
        accumulate_gran_big += none_to_zero(data_gran[i])

    elif (Ip >= 1) and (15 <= accumulate_gran_big <= 25):
        type_ground = 15  # Супесь, суглинок, глина с галькой (щебнем), с гравием (дресвой) или ракушкой

    elif (Ip >= 1) and (25 < accumulate_gran_big <= 50):
        type_ground = 16  # Супесь, суглинок, глина галечниковые (щебенистые), гравелистые (дресвяные) или ракушечные'''

    print(int(str(type_ground_A) + str(type_ground_B) + str(type_ground_C)))

    return int(type_ground_A + type_ground_B)

def none_to_zero(x):
    return x if x else 0

def accumulate_gran(data_gran: dict, keys: list):
    accumulate = 0
    for key in keys:
        accumulate += none_to_zero(data_gran[key])
    return accumulate

def define_A(Ir: float, Ip: float) -> int:
    """Функция определения типа грунта через грансостав

        :argument Ir: содержание органики
        :argument Ip: число пластичности
        :return тип грунта
    """
    Ip = none_to_zero(Ip)
    Ir = none_to_zero(Ir)

    if Ir >= 50:
        return 5  # Торф
    elif Ip < 1:
        return 1  # Песок
    elif 1 <= Ip <= 7:
        return 2  # Супесь
    elif 7 < Ip <= 17:
        return 3  # Суглинок
    elif Ip > 17:
        return 4  # Глина

    raise ValueError("Can't define ground type A")

def define_B1(data_gran: dict) -> int:
    """Функция определения типа песка через грансостав

        :argument data_gran: словарь грансостава, полуенный из granDict или granDictModified
        :return тип грунта
    """
    if accumulate_gran(data_gran, ['10', '5', '2']) > 25:
        return 1  # Песок гравелистый
    elif accumulate_gran(data_gran, ['10', '5', '2', '1', '05']) > 50:
        return 2  # Песок крупный
    elif accumulate_gran(data_gran, ['10', '5', '2', '1', '05', '025']) > 50:
        return 3  # Песок средней крупности
    elif accumulate_gran(data_gran, ['10', '5', '2', '1', '05', '025', '01']) >= 75:
        return 4  # Песок мелкий
    else:
        return 5  # Песок пылеватый

    raise ValueError("Can't define ground type B1")

def define_B2(data_gran: dict) -> int:
    """Функция определения типа супеси

        :argument data_gran: словарь грансостава, полуенный из granDict или granDictModified
        :return тип грунта
    """
    if accumulate_gran(data_gran, ['2', '1', '05', '025', '01', '005']) >= 50:
        return 1  # Супесь песчанистая
    elif accumulate_gran(data_gran, ['2', '1', '05', '025', '01', '005']) < 50:
        return 2  # Супесь пылеватая

    raise ValueError("Can't define ground type B2")

def define_B3(data_gran: dict, Ip: float) -> int:
    """Функция определения типа суглинка

        :argument data_gran: словарь грансостава, полуенный из granDict или granDictModified
        :argument Ip: число пластичности
        :return тип грунта
    """
    if accumulate_gran(data_gran, ['2', '1', '05', '025', '01', '005']) >= 40:
        if Ip <= 12:
            return 1  # Суглинок легкий песчаныстый
        else:
            return 2  # Суглинок тяжелый песчаныстый
    elif accumulate_gran(data_gran, ['2', '1', '05', '025', '01', '005']) < 40:
        if Ip <= 12:
            return 3  # Суглинок легкий пылеватый
        else:
            return 4  # Суглинок тяжелый пылеватый

    raise ValueError("Can't define ground type B3")

def define_B4(data_gran: dict, Ip: float) -> int:
    """Функция определения типа глины

        :argument data_gran: словарь грансостава, полуенный из granDict или granDictModified
        :argument Ip: число пластичности
        :return тип грунта
    """
    if Ip > 27:
        return 3  # Глина тяжелая
    elif accumulate_gran(data_gran, ['2', '1', '05', '025', '01', '005']) >= 40:
        return 1  # Глина легкая песчанистая
    elif accumulate_gran(data_gran, ['2', '1', '05', '025', '01', '005']) < 40:
        return 2  # Глина легкая пылеватая

    raise ValueError("Can't define ground type B4")

def define_C1(B1: int, e: float) -> int:
    """Функция определения типа песка

        :argument B1: тип песка
        :argument e: Коэффициент пористости
        :return тип грунта
    """
    if e is None:
        return 0

    if B1 in [1, 2, 3]:
        if e <= 0.55:
            return 1  # Плотный
        elif 0.55 < e <= 70:
            return 2  # Средней плотности
        elif e > 0.7:
            return 3  # Рыхлый
    elif B1 == 4:
        if e <= 0.60:
            return 1  # Плотный
        elif 0.60 < e <= 75:
            return 2  # Средней плотности
        elif e > 0.75:
            return 3  # Рыхлый
    elif B1 == 5:
        if e <= 0.60:
            return 1  # Плотный
        elif 0.60 < e <= 80:
            return 2  # Средней плотности
        elif e > 0.8:
            return 3  # Рыхлый

    raise ValueError("Can't define ground type C1")

def define_C2(Il: float) -> int:
    """Функция определения типа супеси

        :argument Il: Индекс текучести
        :return тип грунта
    """
    if Il is None:
        return 0

    if Il < 0:
        return 1  # Твердая
    elif 0 <= Il <= 1:
        return 2  # Пластичная
    elif Il > 1:
        return 3  # Текучая

    raise ValueError("Can't define ground type C2")

def define_C3_4(Il: float) -> int:
    """Функция определения типа сугленка и глины

        :argument Il: Индекс текучести
        :return тип грунта
    """
    if Il is None:
        return 0

    if Il < 0:
        return 1  # Твердый
    elif 0 <= Il <= 0.25:
        return 2  # Полутвердый
    elif 0.25 < Il <= 0.5:
        return 2  # Тугопластичный
    elif 0.5 <= Il <= 0.75:
        return 2  # Мягкопластичный
    elif 0.75 <= Il <= 1:
        return 2  # Текучепластичный
    elif Il > 1:
        return 3  # Текучий

    raise ValueError("Can't define ground type C34")







