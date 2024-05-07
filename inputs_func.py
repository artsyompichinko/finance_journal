import check_format as check_f
import datetime
from typing import List, Dict, Union, Any


def inputs_for_add_entry(journal_: Any) -> None:
    """
    Ввод данных для добавления новой записи в журнал.

    Аргумент:
        journal_ (FinanceJournal): Экземпляр класса FinanceJournal.

    """
    while True:
        date = input("Введите дату (ГГГГ-ММ-ДД) или введите 'отмена' для отмены действия: ")
        if date.lower() == 'отмена':
            print("Отмена операции.")
            return
        if not check_f.check_date_format(date):
            print("Ошибка. Неправильный формат даты. Попробуйте еще раз.")
            continue

        category = input("Введите категорию (Доход/Расход) или введите 'отмена' для отмены действия: ")
        if category.lower() == 'отмена':
            print("Отмена операции.")
            return
        if not check_f.check_income_or_expense(category):
            print("Ошибка. Введите 'Доход' или 'Расход'. Попробуйте еще раз.")
            continue

        amount = input("Введите сумму или введите 'отмена' для отмены действия: ")
        if amount.lower() == 'отмена':
            print("Отмена операции.")
            return
        if not check_f.check_numeric(amount):
            print("Ошибка. Введите число. Попробуйте еще раз.")
            continue

        description = input("Введите описание: ")
        journal_.add_entry(datetime.datetime.strptime(date, "%Y-%m-%d"), category.lower, float(amount), description)
        print("Запись добавлена успешно!")
        break


def inputs_for_edit_entry(entry_: Dict[str, Union[str, datetime.datetime, float]], journal_: Any) -> None:
    """

    Ввод данных для редактирования существующей записи в журнале.

    Аргументы:
        entry_ (Dict[str, Union[str, datetime.datetime, float]]): Словарь, представляющий запись в журнале.
        journal_ (FinanceJournal): Экземпляр класса FinanceJournal.

    """
    while True:
        date_ = input("Введите новую дату (ГГГГ-ММ-ДД) или оставьте строку пустой "
                      "и нажмите Enter, чтобы не изменять дату: ")
        if date_.lower() != '':
            if not check_f.check_date_format(date_):
                print("Ошибка. Неправильный формат даты. Попробуйте еще раз.")
                continue
            else:
                entry_['date'] = datetime.datetime.strptime(date_, "%Y-%m-%d")
        category_ = input("Введите категорию (Доход/Расход) или оставьте строку пустой "
                          "и нажмите Enter, чтобы не изменять категорию: ")
        if category_.lower() != '':
            if not check_f.check_income_or_expense(category_):
                print("Ошибка. Введите 'Доход' или 'Расход'. Попробуйте еще раз.")
                continue
            else:
                entry_['category'] = category_.lower()
        amount_ = input("Введите сумму или оставьте строку пустой и нажмите Enter, чтобы не изменять сумму: ")
        if amount_ != '':
            if not check_f.check_numeric(amount_):
                print("Ошибка. Введите число. Попробуйте еще раз.")
                continue
            else:
                entry_['amount'] = float(amount_)
        description_ = input("Введите описание или оставьте строку пустой "
                             "и нажмите Enter, чтобы не изменять описание: ")
        if description_ != '':
            entry_['description'] = description_
            print('***', description_)
        break

    journal_.save_entries()
    print('Изменения сохранены')


def inputs_for_search(journal_: Any) -> List[Dict[str, Union[str, datetime.datetime, float]]]:
    """

    Ввод критериев поиска и поиск записей в журнале.

    Аргумент:
        journal_ (FinanceJournal): Экземпляр класса FinanceJournal.

    Возвращает:
        List[Dict[str, Union[str, datetime.datetime, float]]]: Список записей, соответствующих критериям поиска.

    """
    while True:
        date_ = input("\nВведите дату (ГГГГ-ММ-ДД) или оставьте поле пустым и нажмите Enter: ")
        if date_.lower() != '':
            if not check_f.check_date_format(date_):
                print("Ошибка. Неправильный формат даты. Попробуйте еще раз.")
                continue
        else:
            date_ = None
        category_ = input("Введите категорию (Доход/Расход) или оставьте поле пустым и нажмите Enter: ").lower()
        if category_.lower() != '':
            if not check_f.check_income_or_expense(category_):
                print("Ошибка. Введите 'Доход' или 'Расход'. Попробуйте еще раз.")
                continue
        else:
            category_ = None
        amount_ = input("Введите сумму или оставьте поле пустым и нажмите Enter: ")
        if amount_ != '':
            if not check_f.check_numeric(amount_):
                print("Ошибка. Введите число. Попробуйте еще раз.")
                continue
        else:
            amount_ = None

        break
    print('\n')
    print('{:<10} {:<12} {:<10} {:<10} {:<20}'.format('индекс', 'дата', 'категория', 'сумма', 'описание'))
    filtered_entries = journal_.search_entries(category=category_, date=date_, amount=amount_)
    for entry_id, entry in enumerate(filtered_entries):
        date_str = entry["date"].strftime("%Y-%m-%d")
        category_str = entry["category"]
        amount_str = str(entry["amount"])
        description_str = entry["description"]
        print('{:<10} {:<12} {:<10} {:<10} {:<20}'.format(entry_id + 1, date_str, category_str, amount_str,
                                                          description_str))
    return filtered_entries


def input_index_for_edit(len_list: int) -> int:
    """

    Ввод индекса записи для редактирования.

    Аргумент:
        len_list (int): Длина списка записей.

    Возвращает:
        int: Индекс записи для редактирования.

    Обработка исключения:
        ValueError: Если введенное значение не является целым числом.

    """
    while True:
        input_index = input('\nВведите индекс записи, которую хотите изменить: ')
        try:
            input_index = int(input_index) - 1
            if input_index < 0 or input_index >= len_list:
                print('Неверное значение индекса. Введите числовой индекс существующей записи.')
            else:
                break
        except ValueError:
            print('Неверное значение индекса. Введите числовой индекс существующей записи.')
    return input_index
