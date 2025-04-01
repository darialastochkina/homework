import pandas as pd
import os
import csv
from typing import List, Dict, Any


def read_transactions_csv(file_path: str) -> List[Dict[str, Any]]:
    """Считывает финансовые операции из CSV файла."""
    transactions = []

    if not os.path.exists(file_path):
        print(f"Ошибка: Файл '{file_path}' не найден.")
        return transactions

    try:
        with open(file_path, mode='r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row.get('state'):
                    formatted_transaction = {
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
                    transactions.append(formatted_transaction)
    except Exception as e:
        print(f"Ошибка при чтении CSV файла: {e}")

    return transactions


def read_transactions_excel(file_path: str) -> List[Dict[str, Any]]:
    """Считывает финансовые операции из Excel файла."""
    transactions = []

    if not os.path.exists(file_path):
        print(f"Ошибка: Файл '{file_path}' не найден.")
        return transactions

    try:
        df = pd.read_excel(file_path, engine='openpyxl')
        df.columns = df.columns.str.lower()
        raw_transactions = df.to_dict('records')
        for row in raw_transactions:
            if pd.notna(row.get('state')):
                formatted_transaction = {
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
                transactions.append(formatted_transaction)
    except Exception as e:
        print(f"Ошибка при чтении Excel файла: {e}")
        import traceback
        print(traceback.format_exc())

    return transactions
