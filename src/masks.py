import logging
import os


if not os.path.exists('logs'):
    os.makedirs('logs')

logger = logging.getLogger('app.masks')
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler('logs/masks.log', mode='w')
file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_formatter)

logger.addHandler(file_handler)


def get_mask_card_number(card_number: str) -> str:
    """Функция для маскировки номера карты."""
    logger.info("Запуск маскировки номера карты")
    card_number = str(card_number)
    block1 = card_number[:4]
    block2 = card_number[4:6]
    block3 = "**"
    block4 = "****"
    block5 = card_number[-4:]
    mask_card = f"{block1} {block2}{block3} {block4} {block5}"
    logger.info(f"Маскировка пройдена успешно - {mask_card}")
    return mask_card


def get_mask_account(account_number: str) -> str:
    """Функция для маскировки номера счета."""
    logger.info("Запуск маскировки номера счета")
    block6 = account_number[-4:]
    mask_number = f"**{block6}"
    logger.info(f"Маскировка пройдена успешно - {mask_number}")
    return mask_number
