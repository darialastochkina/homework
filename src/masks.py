def get_mask_card_number(card_number: str) -> str:
    first_part = card_number[:6]
    last_part = card_number[-4:]
    masked_part = "** ****"
    masked_number = f"{first_part[:4]} {first_part[4:6]}{masked_part} {last_part}"
    return masked_number


def get_mask_account(account_number: str) -> str:
    last_part = account_number[-4:]
    masked_account = "**" + last_part
    return masked_account
