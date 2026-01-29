from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from app.config import OFFERS


def offer_keyboard():
    keyboard = []
    for k, v in OFFERS.items():
        keyboard.append(
            [InlineKeyboardButton(
                text=v["name"],
                callback_data=f"offer_{k}"
            )]
        )
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def main_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text="➕ Новая заявка",
                callback_data="new_request"
            )]
        ]
    )