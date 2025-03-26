import logging
import json
import os
from typing import List, Dict, Any


if not os.path.exists('logs'):
    os.makedirs('logs')

logger = logging.getLogger('app.utils')
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler('logs/utils.log', mode='w')
file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_formatter)

logger.addHandler(file_handler)


def read_operations_from_json(file_path: str) -> List[Dict[str, Any]]:
    """Читает операции из JSON-файла и возвращает список транзакций."""
    logger.info(f"Загрузка транзакций из файла {file_path}")
    if not os.path.exists(file_path):
        logger.error(f"Файл {file_path} не найден")
        return []

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        if isinstance(data, list):
            logger.info(f"Файл {file_path} загружен успешно")
            return data
        logger.warning(f"Данные в файле {file_path} не являются списком")
        return []
    except json.JSONDecodeError:
        logger.error(f"Ошибка декодирования JSON в файле {file_path}")
        return []
    except Exception as e:
        logger.error(f"Неожиданная ошибка при чтении файла {file_path}: {str(e)}")
        return []
