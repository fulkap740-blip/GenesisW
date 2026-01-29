from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from app.config import OFFERS

def offers_kb():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=v["name"], callback_data=f"offer_{k}")]
            for k, v in OFFERS.items()
        ]
    )

def user_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="➕ Новая заявка", callback_data="new_request")]
        ]
    )