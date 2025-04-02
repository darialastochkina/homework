import json
import csv
import pandas as pd
import re
import os


VALID_STATUSES = ['EXECUTED', 'CANCELED', 'PENDING']


def sort_by_date(transactions, reverse=True):
    """Сортирует список транзакций по дате."""
    return sorted(transactions, key=lambda x: x.get('date', ''), reverse=reverse)


def search_by_description(transactions, search_string):
    """Ищет транзакции, содержащие указанную строку в описании."""
    pattern = re.compile(search_string, re.IGNORECASE)
    return [t for t in transactions if pattern.search(t.get('description', ''))]


def count_categories(transactions, categories):
    """Подсчитывает количество операций в каждой категории."""
    result = {category: 0 for category in categories}
    for t in transactions:
        desc = t.get('description', '').lower()
        for category in categories:
            if category.lower() in desc:
                result[category] += 1
    return result


def filter_by_currency(operations, currency):
    """Фильтрует список транзакций по валюте."""
    return [op for op in operations
            if isinstance(op.get("operationAmount"), dict)
            and isinstance(op.get("operationAmount", {}).get("currency"), dict)
            and op.get("operationAmount", {}).get("currency", {}).get("code") == currency]


def format_account(account):
    """Форматирует номер счета или карты."""
    if not account:
        return
    if 'Счет' in account:
        return f"Счет **{account[-4:]}"
    card_parts = account.split()
    if len(card_parts) >= 2:
        card_num = card_parts[-1]
        if len(card_num) >= 16:
            masked_card = f"{card_num[:4]} {card_num[4:6]}** **** {card_num[-4:]}"
            return f"{' '.join(card_parts[:-1])} {masked_card}"
    return account


def load_transactions(file_path, file_type):
    """Загружает транзакции из файла указанного типа."""
    if not os.path.exists(file_path):
        return None
    try:
        if file_type == 'json':
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                return data if isinstance(data, list) else None
        elif file_type == 'csv':
            with open(file_path, 'r', encoding='utf-8-sig') as file:
                sample = file.read(1024)
                file.seek(0)
                delimiter = ';' if ';' in sample else ','
                reader = csv.DictReader(file, delimiter=delimiter)
                raw_data = list(reader)
                return [
                    {
                        'id': int(row.get('id', 0)),
                        'state': row.get('state', ''),
                        'date': row.get('date', ''),
                        'operationAmount': {
                            'amount': str(row.get('amount', '0')),
                            'currency': {
                                'name': row.get('currency_name', 'руб.'),
                                'code': row.get('currency_code', 'RUB')
                            }
                        },
                        'description': row.get('description', ''),
                        'from': row.get('from', ''),
                        'to': row.get('to', '')
                    }
                    for row in raw_data if row.get('state')
                ]
        elif file_type == 'excel':
            df = pd.read_excel(file_path)
            raw_data = df.to_dict('records')
            return [
                {
                    'id': int(row.get('id', 0)),
                    'state': str(row.get('state', '')),
                    'date': str(row.get('date', '')),
                    'operationAmount': {
                        'amount': str(row.get('amount', '0')),
                        'currency': {
                            'name': str(row.get('currency_name', 'руб.')),
                            'code': str(row.get('currency_code', 'RUB'))
                        }
                    },
                    'description': str(row.get('description', '')),
                    'from': str(row.get('from', '')),
                    'to': str(row.get('to', ''))
                }
                for row in raw_data if pd.notna(row.get('state'))
            ]
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return None


def main():
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    choice = input()
    transactions = []

    if choice == '1':
        print("Для обработки выбран JSON-файл.")
        transactions = (load_transactions('data/operations.json', 'json')
                        or load_transactions('operations.json', 'json'))
    elif choice == '2':
        print("Для обработки выбран CSV-файл.")
        transactions = (load_transactions('data/Transactions (3).csv', 'csv')
                        or load_transactions('data/transactions.csv', 'csv'))
    elif choice == '3':
        print("Для обработки выбран Excel-файл.")
        transactions = (load_transactions('data/Transactions Excel.xlsx', 'excel')
                        or load_transactions('data/transactions.xlsx', 'excel'))
    else:
        print("Неверный выбор")
        return
    if not transactions:
        print("Не найдено ни одной транзакции в файле")
        return
    while True:
        print("\nВведите статус, по которому необходимо выполнить фильтрацию.")
        print("Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING")
        status = input().upper()
        if status not in VALID_STATUSES:
            print(f'Статус операции "{status}" недоступен.')
            continue
        filtered_transactions = [t for t in transactions if t.get('state', '').upper() == status]
        if not filtered_transactions:
            print(f'В файле нет транзакций со статусом "{status}". Попробуйте другой статус.')
            continue
        transactions = filtered_transactions
        print(f'Операции отфильтрованы по статусу "{status}"')
        break

    sort_choice = input("\nОтсортировать операции по дате? Да/Нет\n").lower()
    if sort_choice in ['да', 'yes', 'y']:
        sort_direction = input("\nОтсортировать по возрастанию или по убыванию?\n").lower()
        reverse = 'возрастани' not in sort_direction
        transactions = sort_by_date(transactions, reverse=reverse)

    currency_choice = input("\nВыводить только рублевые тразакции? Да/Нет\n").lower()
    if currency_choice in ['да', 'yes', 'y']:
        filtered = filter_by_currency(transactions, 'RUB')
        transactions = filtered if filtered else transactions
        if not filtered:
            print("Нет транзакций в рублях. Показываем все транзакции.")
    search_choice = input("\nОтфильтровать список транзакций по определенному слову в описании? Да/Нет\n").lower()
    if search_choice in ['да', 'yes', 'y']:
        search_string = input("\nВведите слово для поиска: ")
        filtered = search_by_description(transactions, search_string)
        transactions = filtered if filtered else transactions
        if not filtered:
            print(f'Не найдено транзакций с "{search_string}" в описании. Показываем все транзакции.')

    if not transactions:
        print("\nНе найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return
    print("\nРаспечатываю итоговый список транзакций...")
    print(f"\nВсего банковских операций в выборке: {len(transactions)}\n")

    for t in transactions:
        try:
            date_parts = t['date'].split('T')[0].split('-')
            date = f"{date_parts[2]}.{date_parts[1]}.{date_parts[0]}" if len(date_parts) == 3 else t['date']
            print(f"{date} {t['description']}")

            from_acc = format_account(t.get('from', ''))
            to_acc = format_account(t.get('to', ''))
            if from_acc and to_acc:
                print(f"{from_acc} -> {to_acc}")
            elif to_acc:
                print(to_acc)

            amount = t['operationAmount']['amount']
            currency = t['operationAmount']['currency']['code']
            print(f"Сумма: {amount} {'руб.' if currency == 'RUB' else currency}\n")
        except Exception as e:
            print(f"Ошибка при выводе транзакции: {e}")
            print(f"Транзакция: {t}\n")


if __name__ == "__main__":
    main()
