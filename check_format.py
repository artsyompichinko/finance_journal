import re


def check_date_format(date_string: str) -> bool:
    """
    Проверяет формат даты.

    Аргументы:
        date_string (str): Строка с датой в формате "ГГГГ-ММ-ДД".

    Возвращает:
        bool: True, если формат строки соответствует ожидаемому формату, иначе False.

    """
    pattern = r'^\d{4}-\d{2}-\d{2}$'

    if re.match(pattern, date_string):
        return True
    else:
        return False


def check_income_or_expense(input_string: str) -> bool:
    """
    Проверяет, является ли введенная строка "доходом" или "расходом" (в любом регистре).

    Аргументы:
        input_string (str): Введенная строка.

    Возвращает:
        bool: True, если введенная строка является "доходом" или "расходом", иначе False.

    """
    input_lower = input_string.lower()

    if input_lower in ["доход", "расход"]:
        return True
    else:
        return False


def check_numeric(input_string: str) -> bool:
    """
    Проверяет, является ли введенная строка числом (float).

    Аргументы:
        input_string (str): Введенная строка.

    Возвращает:
        bool: True, если введенная строка является числом или десятичным числом, иначе False.

    """
    try:
        float(input_string)
        return True
    except ValueError:
        return False


def check_index(len_list, input_index):
    while True:
        try:
            input_index = int(input_index)
            if input_index < 1 or input_index > len_list:
                print('Неверное значения индекса. Введите числовой индекс существующей записи.')
            else:
                break
        except ValueError:
            print('Неверное значения индекса. Введите числовой индекс существующей записи.')

    return True
