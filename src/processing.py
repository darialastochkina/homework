from typing import List, Dict, Any


def filter_by_state(
    transactions: List[Dict[str, Any]], state: str = "EXECUTED"
) -> List[Dict[str, Any]]:
    """Фильтрует список словарей по значению ключа state."""
    filter_list = []
    for i in transactions:
        if i["state"] == state:
            filter_list.append(i)
    return filter_list


def sort_by_date(
    transactions: List[Dict[str, Any]], reverse: bool = True
) -> List[Dict[str, Any]]:
    """Сортирует список словарей по ключу 'date' без использования datetime."""
    return sorted(transactions, key=lambda tx: tx["date"], reverse=reverse)
