import datetime
import time
import inputs_func as inputs_f
from typing import List, Dict, Union


class FinanceJournal:
    """
    Класс FinanceJournal описывает журнал финансовых операций.

    Атрибуты:
        filename (str): Имя файла для сохранения журнала. По умолчанию "finance_journal.txt".
        entries (List[Dict[str, Union[str, datetime.datetime, float]]]): Список записей в журнале.

    Методы:
        load_entries(): Загружает записи из файла в журнал.
        get_all_entries(): Выводит все записи в журнале.
        save_entries(): Сохраняет записи из журнала в файл.
        add_entry(date: datetime.datetime, category: str, amount: float, description: str): Добавляет новую запись
        в журнал.
        get_balance() -> float: Возвращает текущий баланс.
        get_income() -> float: Возвращает сумму всех доходов.
        get_expenses() -> float: Возвращает сумму всех расходов.
        search_entries(category: str = None, date: str = None, amount: str = None) -> List[Dict[str,
        Union[str, datetime.datetime, float]]]: записей по категории, дате или сумме.

    """

    def __init__(self, filename: str = "finance_journal.txt") -> None:
        """
        Инициализация журнала финансовых операций.

        Аргументы:
            filename (str, optional): Имя файла для сохранения журнала.

        """
        self.filename = filename
        self.entries: List[Dict[str, Union[str, datetime.datetime, float]]] = []
        self.load_entries()

    def load_entries(self) -> None:
        """
        Загружает записи из файла в журнал.

        """
        try:
            with open(self.filename, "r") as file:
                for line in file:
                    entry_data = line.strip().split(",")
                    entry = {
                        "date": datetime.datetime.strptime(entry_data[0], "%Y-%m-%d"),
                        "category": entry_data[1],
                        "amount": float(entry_data[2]),
                        "description": entry_data[3]
                    }
                    self.entries.append(entry)
        except FileNotFoundError:
            pass

    def get_all_entries(self) -> None:
        """
        Выводит все записи в журнале.

        """
        print('\n')
        for entry in self.entries:
            date_str = entry["date"].strftime("%Y-%m-%d")
            category_str = entry["category"]
            amount_str = str(entry["amount"])
            description_str = entry["description"]

            print('{:<12} {:<10} {:<10} {:<20}'.format(date_str, category_str, amount_str, description_str))

    def save_entries(self) -> None:
        """

        Сохраняет записи из объекта в файл. Полностью перезаписывает файл!!!

        """
        with open(self.filename, "w") as file:
            for entry in self.entries:
                file.write(f"{entry['date'].strftime('%Y-%m-%d')},{entry['category']},"
                           f"{entry['amount']},{entry['description']}\n")

    def add_entry(self, date: datetime.datetime, category: str, amount: float, description: str) -> None:
        """
        Добавляет новую запись в журнал.

        Аргументы:
            date (datetime.datetime): Дата.
            category (str): Категория.
            amount (float): Сумма.
            description (str): Описание.

        """
        entry = {
            "date": date,
            "category": category,
            "amount": amount,
            "description": description
        }
        self.entries.append(entry)
        self.save_entries()

    def get_balance(self) -> float:
        """

            Возвращает:
            float: Текущий баланс.

        """
        income = sum(entry['amount'] for entry in self.entries if entry['category'].lower() == 'доход')
        expenses = sum(entry['amount'] for entry in self.entries if entry['category'].lower() == 'расход')
        balance = income - expenses
        return balance

    def get_income(self) -> float:
        """

        Возвращает:
            float: Сумма всех доходов.

        """
        income = sum(entry['amount'] for entry in self.entries if entry['category'].lower() == 'доход')
        return income

    def get_expenses(self) -> float:
        """

        Возвращает:
            float: Сумма всех расходов.

        """
        expenses = sum(entry['amount'] for entry in self.entries if entry['category'].lower() == 'расход')
        return expenses

    def search_entries(self, category: str = None, date: str = None, amount: str = None) -> \
            List[Dict[str, Union[str, datetime.datetime, float]]]:
        """
        Поиск записей по категории, дате или сумме.

        Аргументы:
            category (str, optional): Категория операции (Доход/Расход).
            date (str, optional): Дата операции в формате "ГГГГ-ММ-ДД".
            amount (str, optional): Сумма операции.

        Возвращает:
            List[Dict[str, Union[str, datetime.datetime, float]]]: Список записей, соответствующих критериям поиска.

        """
        results = []

        for entry in self.entries:
            if category is not None and entry['category'].lower() != category.lower():
                continue
            if date is not None and entry['date'] != datetime.datetime.strptime(date, '%Y-%m-%d'):
                continue
            if amount is not None and entry['amount'] != float(amount):
                continue
            results.append(entry)

        return results


def main() -> None:
    """

    Основная функция программы для управления журналом финансовых операций.

    """
    journal = FinanceJournal()

    while True:
        print("\n1. Вывод баланса")
        print("2. Добавление записи")
        print("3. Вывод всех записей")
        print("4. Поиск и редактирование записей")
        print("5. Выход")

        choice = input("Выберите действие: ")

        if choice == "1":
            print(f"\nТекущий баланс: {journal.get_balance()}")
            print(f"Доходы: {journal.get_income()}")
            print(f"Расходы: {journal.get_expenses()}")
            time.sleep(1)

        elif choice == "2":
            inputs_f.inputs_for_add_entry(journal)

        elif choice == "3":
            journal.get_all_entries()

        elif choice == "4":
            # Получаем список записей, отфильтрованных поиском
            filtered_entries = inputs_f.inputs_for_search(journal)

            if filtered_entries:
                print('\n1. Изменить запись')
                print('2. Назад')

                while True:
                    choice = input('\nВыберите нужную функцию: ')

                    if choice not in ['1', '2']:
                        print("Некорректный выбор. Пожалуйста, выберите существующую опцию.")
                        continue

                    if choice == '1':
                        # Получаем запись которою хотят изменить
                        edit_entry = filtered_entries[inputs_f.input_index_for_edit(len(filtered_entries))]
                        print(f'\nРедактирование записи '
                              f'{edit_entry["date"].strftime("%Y-%m-%d"), edit_entry["category"],edit_entry["amount"], edit_entry["description"]}')

                        inputs_f.inputs_for_edit_entry(edit_entry, journal)
                        break
                    elif choice == '2':
                        break

            else:
                print('Не найдено записей по введённым параметрам')

        elif choice == "5":
            print("Выход из программы.")
            break

        else:
            print("Некорректный выбор. Пожалуйста, выберите существующую опцию.")


if __name__ == "__main__":
    main()
