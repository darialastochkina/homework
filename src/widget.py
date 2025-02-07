from src import masks


def mask_account_card(acc: str) -> str:
    """функция счёта"""
    number = ""
    name_card = ""
    for i in acc:
        if i.isdigit():
            number += i
        else:
            name_card += i

        name_card += masks.get_mask_account(number)
    else:
        name_card += masks.get_mask_card_number(number)
    return name_card


def get_date(date: str) -> str:
    date_format = f"{date[8:10]}.{date[5:7]}.{date[:4]}"
    return date_format
