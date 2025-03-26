def filter_by_currency(operations, currency):
    """Фильтрует список транзакций по валюте."""
    return (
        operation for operation in operations
        if operation.get("operationAmount").get("currency").get("code") == currency
    )


def transaction_descriptions(transactions):
    """Возвращает список описаний транзакций."""
    return (
        transaction.get("description") for transaction in transactions
    )


def format_number(number):
    """Форматирует номер карты."""
    st = ""
    for i in range(16):
        a = number % 10
        s = str(a)
        st = s + st
        number = number // 10
        if (i + 1) % 4 == 0 and i != 15:
            st = " " + st
    return st


def card_number_generator(start, finish):
    """Генерирует список номеров карт."""
    for i in range(start, finish + 1):
        yield format_number(i)
