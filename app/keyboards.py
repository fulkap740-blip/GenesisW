from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from app.config import OFFERS

def offer_keyboard():
    buttons = [
        [InlineKeyboardButton(text=v["name"], callback_data=f"offer_{k}")]
        for k, v in OFFERS.items()
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def main_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="➕ Новая заявка", callback_data="new_request")]
    ])