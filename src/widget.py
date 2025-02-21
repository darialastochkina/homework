from src import masks


def mask_account_card(acc: str) -> str:
    parts = acc.split()
    name = parts[0:-1]
    number = parts[-1]

    name_str = ' '.join(name)

    if name_str == "Счет":
        return f"{name_str} {masks.get_mask_account(number)}"
    else:
        return f"{name_str} {masks.get_mask_card_number(number)}"


def get_date(date: str) -> str:
    date_format = f"{date[8:10]}.{date[5:7]}.{date[:4]}"
    return date_format
