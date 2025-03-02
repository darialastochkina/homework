import pytest

from src.widget import get_date, mask_account_card


@pytest.mark.parametrize("input_str, expected", [
    ("Visa Platinum 7000792289606361", "Visa Platinum 7000 79** **** 6361"),
    ("Счет 73654108430135874305", "Счет **4305"),
])
def test_mask_account_card(input_str, expected):
    assert mask_account_card(input_str) == expected


@pytest.mark.parametrize("input_date, expected", [
    ("2024-01-01", "01.01.2024"),
])
def test_get_date(input_date, expected):
    assert get_date(input_date) == expected
