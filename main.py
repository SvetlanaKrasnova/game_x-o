import random

def current_maps():
    """
    Функция возвращает текущую карту
    Формат:
        0 1 2
    0   X X 0
    1   0 x -
    2   - 0 -
    :return: str
    """
    str = ['    0 1 2']
    for i, l in enumerate(maps):
        str.append(f'{i}   {" ".join(l)}')

    return '\n'.join(str)


def put_value(x: int, y: int, value):
    """
    Функция ставит значение value в указанную ячейку
    :param x: номер строки
    :param y: номер колонки
    :return:
    """
    maps[x][y] = value
    return True


def finish(user):
    """
    Функция проверяет выигрышные комбинации.
    Если кто-то выиграл или есть нечья -
    :param user: текущий игрок
    :return: {
        'status': True - выигрыш есть / False - игра продолжается
        'user_finish': кто выиграл или 'Нечья'
    }
    """
    vect_left, vect_right = [], []
    user_finish = user

    for i, line in enumerate(maps):
        # Если все элементы в строке равны "х" или "о", значит кто-то выиграл
        for _p in [['x', 'х'], ['о', 'o']]:
            if all([True if _i in _p else False for _i in line]):
                return {'status': True,
                        'user_finish': user_finish}

        # Собираем данные по диагоналям
        for k, index in enumerate(line):
            if maps[i][k].lower() != '-':
                if f'{i} {k}' in ['0 0', '1 1', '2 2']:
                    vect_right.append(maps[i][k])
                if f'{i} {k}' in ['0 2', '1 1', '2 0']:
                    vect_left.append(maps[i][k])

    # Проверяем диагонали
    for vector in [vect_right, vect_left]:
        # Если по одной из диагонали проставлены все 3 значения
        if vector.__len__() == 3:
            for _p in [['x', 'х'], ['о', 'o']]:
                # Если все одинаковые значения (либо русская буква, либо английская)
                if all([True if i in _p else False for i in vector]):
                    return {'status': True,
                            'user_finish': user_finish}

    # Переворачиваем мертицу (колонки теперь строки)
    # И проверяем выигрыш по колонкам
    for l in list(zip(*maps)):
        for _p in [['x', 'х'], ['о', 'o']]:
            if all([True if i in _p else False for i in l]):
                return {'status': True,
                        'user_finish': user_finish}

    # Проверяем, есть ли свободные ячейки
    col = 0
    for l in maps:
        col += [_i for _i in l if _i == '-'].__len__()
    if col == 0:
        # Если свободных ячеек нет и мы тут, значит нечья
        return {'status': True,
                'user_finish': 'Ничья'}

    return {'status': False,
            'user_finish': user_finish}


def check_step(current_maps, value: str = 'o'):
    """
    Функция проверяет, есть ли где-то "почти" выигрышная комбинация
    (когда нужно поставить одно значение до выигрыша)
    :param current_maps: текущая карта с расположениями "X" и "O"
    :param value: "o" или "x"
    :return: строку, столбец свободной ячейки куда поставим value
    Почти выигрышной комбинации может и не быть, тогда вернем None, None
    """
    x, y = None, None
    for i, l in enumerate(current_maps):
        if [_l for _l in l if _l == value].__len__() == 2:
            if [_l for _l in l if _l == '-']:
                x = i
                y = [current_maps[i].index(_l) for _l in l if _l == '-'][0]
                break
    return x, y


def get_value_computer(step=1):
    """
    Функция возвращает свободную клетку для "O", значение где стоит "-".
    Функция была написана с мыслью "не дать Х выиграть" (для интереса, чтобы не играть за двоих)
    :return: номер строки, номер столбца
    """

    # Если это первый шаг "О", то не важно куда поставим значение
    # Для интереса - выбираем рандомную ячейку (если она будет занята "Х"
    # - пойдем по обычной логике выбора
    if step == 1:
        k = 0
        while k <= 5:
            x = random.randrange(3)
            y = random.randrange(3)
            if maps[x][y] == '-':
                return x, y
            else:
                k += 1

    # Проверяем, а не можем ли выиграть мы?
    # (по строкам)
    x, y = check_step(value='o', current_maps=maps)
    if not x is None and not y is None:
        return x, y

    # (по колонкам)
    revers_maps = list(zip(*maps))
    y, x = check_step(value='o', current_maps=revers_maps)
    if not x is None and not y is None:
        return x, y

    # Проверяем, есть ли где-то два "х",
    # Если есть, ставим в свободную ячейку "o", чтобы "x" не выиграл
    # (по строкам)
    x, y = check_step(value='x', current_maps=maps)
    if not x is None and not y is None:
        return x, y

    # (по колонкам)
    y, x = check_step(value='x', current_maps=revers_maps)
    if not x is None and not y is None:
        return x, y

    # Проверяем диагонали
    vector_left = [maps[i][i] for i in range(3) if maps[i][i] == 'x']
    vector_right = [maps[l][s] for l, s in zip(range(3), range(2, -1, -1)) if maps[l][s] == 'x']

    # Если по диагоналям есть 2 одинаковых значения
    # - ставим туда "o", чтобы "x" не выиграл
    if vector_right.__len__() == 2:
        for l, s in zip(range(3), range(2, -1, -1)):
            if maps[l][s] == '-':
                return l, s

    if vector_left.__len__() == 2:
        for l in range(3):
            if maps[l][l] == '-':
                return l, l

    # Если ничего не нашли, ставим первую свободную ячейку
    # (ситуация, когда будет ничья)
    for i, l in enumerate(maps):
        for k, _j in enumerate(l):
            if maps[i][k] == '-':
                return i, k

    return x, y


print(''.join(['*' for i in range(20)]))
print('ИГРА КРЕСТИКИ-НОЛИКИ')
print(''.join(['*' for i in range(20)]))
print('Пример ввода')
print('Необходимо вводить индексы строк и столбцов через пробел:')
print('\t"Введите номер строки, столбца: 0 0"')
print('\t"Введите номер строки, столбца: 2 1"\n')
print("СТАРТ ИГРЫ!")

with_computer = str(input("Хотите играть с компьютером (Y/N)? ")).strip().lower()
if not with_computer in ['y', 'n']:
    with_computer = False
    print('Вы ввели некорректное значение. Будет игра без компьютера.')
elif with_computer == 'y':
    with_computer = True
    print('Игра с компьютером')
elif with_computer == 'n':
    with_computer = False
    print('Игра без компьютера')
else:
    with_computer = False
    print('Неудалось распознать ввод. Будет игра без компьютера.')

# Для игры с компьютером
# (для первого шага - выбираем любую ячейку)
step = 1

# Объявляем карту
maps = [['-', '-', '-'],
        ['-', '-', '-'],
        ['-', '-', '-']]

# Всего два игрока "Пользователь X" и "Пользователь O"
# По умолчанию ходит "Пользователь X" первым
user = 'Пользователь X'

while True:
    try:
        # Печатаем текущую карту
        print(f'\nТекущая матрица:\n{current_maps()}\n')

        # Если ход "Пользователь O" и если игра с копьютером
        # - пропускаем запрос ввода
        print(f'Ваш ход "{user}"')
        if user == 'Пользователь O' and with_computer:
            x, y = get_value_computer(step=step)
            step += 1
            print(f'Ход компьютера: {x} {y}')
        else:
            x, y = str(input('Введите номер строки, столбца: ')).strip().split(' ')

        if maps[int(x)][int(y)] in ['x', 'o']:
            print('Эта клетка уже занята! Попробуйте ещё раз!')
            continue

        put_value(x=int(x), y=int(y), value='x' if user == 'Пользователь X' else 'o')

        # Проверяем выиграл ли пользователь
        res = finish(user)
        if res['status']:
            user = res['user_finish']
            break

        # Меняем игрока
        if user == 'Пользователь X':
            user = 'Пользователь O'
        else:
            user = 'Пользователь X'

    except Exception as e:
        print('Некорректные значения. Попробуйте ещё раз')

# Печатаем итог
print(f'{f"{user} победил!" if user.__contains__("Пользователь") else f"{user}!"}')
print(current_maps())
print('ИГРА ОКОНЧЕНА!')
