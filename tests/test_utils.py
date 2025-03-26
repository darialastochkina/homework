import json
from unittest.mock import patch, mock_open
from src.utils import read_operations_from_json


def test_read_operations_from_json_valid_file():
    """Тест чтения корректного JSON-файла с транзакциями"""
    test_data = [
        {"id": 1, "state": "EXECUTED"},
        {"id": 2, "state": "CANCELED"}
    ]
    mock_json = json.dumps(test_data)
    with patch("builtins.open", mock_open(read_data=mock_json)):
        with patch("os.path.exists", return_value=True):
            result = read_operations_from_json("test_file.json")
    assert result == test_data
    assert len(result) == 2


def test_read_operations_from_json_empty_file():
    """Тест чтения пустого JSON-файла"""
    with patch("builtins.open", mock_open(read_data="[]")):
        with patch("os.path.exists", return_value=True):
            result = read_operations_from_json("empty_file.json")
    assert result == []


def test_read_operations_from_json_not_list():
    """Тест чтения JSON-файла, содержащего не список"""
    with patch("builtins.open", mock_open(read_data='{"key": "value"}')):
        with patch("os.path.exists", return_value=True):
            result = read_operations_from_json("not_list.json")
    assert result == []


def test_read_operations_from_json_file_not_found():
    """Тест чтения несуществующего файла"""
    with patch("os.path.exists", return_value=False):
        result = read_operations_from_json("nonexistent_file.json")
    assert result == []


def test_read_operations_from_json_invalid_json():
    """Тест чтения некорректного JSON-файла"""
    with patch("builtins.open", mock_open(read_data="invalid json")):
        with patch("os.path.exists", return_value=True):
            result = read_operations_from_json("invalid.json")
    assert result == []
