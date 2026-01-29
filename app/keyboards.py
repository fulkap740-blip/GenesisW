from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from app.config import OFFERS


def offer_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=v["name"], callback_data=f"offer_{k}")]
            for k, v in OFFERS.items()
        ]
    )


def main_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="➕ Новая заявка", callback_data="new_request")]
        ]
    )


def admin_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📊 Экспорт заявок (Excel)", callback_data="admin_export")],
            [InlineKeyboardButton(text="🚪 Выйти", callback_data="admin_exit")]
        ]
    )