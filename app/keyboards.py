from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import OFFERS

def offers_kb():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text=offer["name"],
                callback_data=f"offer_{oid}"
            )] for oid, offer in OFFERS.items()
        ]
    )

def user_menu_kb():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="➕ Новая заявка", callback_data="new_request")],
            [InlineKeyboardButton(text="👤 Профиль", callback_data="profile")]
        ]
    )