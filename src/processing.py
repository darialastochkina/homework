def filter_by_state(transactions, state="EXECUTED"):
    """Фильтрует список словарей по значению ключа state."""
    filter_list = []
    for i in transactions:
        if i["state"] == state:
            filter_list.append(i)
    return filter_list


def sort_by_date(transactions, reverse=True):
    """Сортирует список словарей по ключу 'date' без использования datetime."""
    return sorted(transactions, key=lambda tx: tx["date"], reverse=reverse)
