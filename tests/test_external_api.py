from unittest.mock import patch, MagicMock
from src.external_api import convert_to_rubles, get_exchange_rate


def test_convert_to_rubles_rub_transaction():
    """Тест конвертации транзакции в рублях"""
    transaction = {
        "id": 1,
        "operationAmount": {
            "amount": "100.50",
            "currency": {
                "code": "RUB"
            }
        }
    }
    result = convert_to_rubles(transaction)
    assert result == 100.50


@patch('src.external_api.get_exchange_rate')
def test_convert_to_rubles_usd_transaction(mock_get_rate):
    """Тест конвертации транзакции в долларах"""
    mock_get_rate.return_value = 75.0
    transaction = {
        "id": 2,
        "operationAmount": {
            "amount": "50.0",
            "currency": {
                "code": "USD"
            }
        }
    }
    result = convert_to_rubles(transaction)
    assert result == 3750.0
    mock_get_rate.assert_called_once_with('USD', 'RUB')


@patch('src.external_api.get_exchange_rate')
def test_convert_to_rubles_eur_transaction(mock_get_rate):
    """Тест конвертации транзакции в евро"""
    mock_get_rate.return_value = 85.0
    transaction = {
        "id": 3,
        "operationAmount": {
            "amount": "30.0",
            "currency": {
                "code": "EUR"
            }
        }
    }
    result = convert_to_rubles(transaction)
    assert result == 2550.0
    mock_get_rate.assert_called_once_with('EUR', 'RUB')


@patch('src.external_api.get_exchange_rate')
def test_convert_to_rubles_api_failure(mock_get_rate):
    """Тест конвертации при недоступности API"""
    mock_get_rate.return_value = None
    transaction = {
        "id": 4,
        "operationAmount": {
            "amount": "25.0",
            "currency": {
                "code": "USD"
            }
        }
    }
    result = convert_to_rubles(transaction)
    assert result == 25.0


@patch('requests.get')
def test_get_exchange_rate_success(mock_get):
    """Тест успешного получения курса обмена"""
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "success": True,
        "result": 75.5,
        "info": {
            "rate": 75.5
        }
    }
    mock_response.status_code = 200
    mock_get.return_value = mock_response

    with patch('src.external_api.API_KEY', 'test_key'):
        rate = get_exchange_rate('USD', 'RUB')
    assert rate == 75.5
    mock_get.assert_called_once()
    args, kwargs = mock_get.call_args
    assert kwargs['params'] == {
        "to": "RUB",
        "from": "USD",
        "amount": 1
    }
    assert kwargs['headers'] == {"apikey": "test_key"}


@patch('requests.get')
def test_get_exchange_rate_api_error(mock_get):
    """Тест обработки ошибки API"""
    mock_get.side_effect = Exception("API Error")
    with patch('src.external_api.API_KEY', 'test_key'):
        rate = get_exchange_rate('USD', 'RUB')
    assert rate is None
    mock_get.assert_called_once()


def test_get_exchange_rate_no_api_key():
    """Тест поведения при отсутствии API ключа"""
    with patch('src.external_api.API_KEY', None):
        rate = get_exchange_rate('USD', 'RUB')
    assert rate is None
