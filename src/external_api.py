import os
import requests
from typing import Dict, Any, Optional
from dotenv import load_dotenv


load_dotenv()

API_KEY = os.getenv("EXCHANGE_API_KEY")


def get_exchange_rate(from_currency: str, to_currency: str) -> Optional[float]:
    """Получает курс обмена валют через API."""
    if not API_KEY:
        return None

    url = "https://api.apilayer.com/exchangerates_data/convert"
    params = {
        "to": to_currency,
        "from": from_currency,
        "amount": 1
    }
    headers = {"apikey": API_KEY}

    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        result = response.json()
        return result.get("result")
    except Exception:
        return None


def convert_to_rubles(transaction: Dict[str, Any]) -> float:
    """Конвертирует сумму транзакции в рубли."""
    currency_code = transaction['operationAmount']['currency']['code']
    amount = float(transaction['operationAmount']['amount'])

    if currency_code == 'RUB':
        return amount

    rate = get_exchange_rate(currency_code, 'RUB')
    if rate is None:
        return amount

    return amount * rate
