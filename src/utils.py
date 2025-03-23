import json
import os
from typing import List, Dict, Any


def read_operations_from_json(file_path: str) -> List[Dict[str, Any]]:
    """Читает операции из JSON-файла и возвращает список транзакций."""
    try:
        if not os.path.exists(file_path):
            return []

        with open(file_path) as file:
            data = json.load(file)
        if not isinstance(data, list):
            return []
        return data
    except (json.JSONDecodeError):
        return []
