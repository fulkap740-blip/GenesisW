from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def offer_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🟣 White Bird", callback_data="offer_1")],
        [InlineKeyboardButton(text="🔵 Genesis", callback_data="offer_2")]
    ])

def profile_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="➕ Новая заявка", callback_data="new_request")]
    ])

def admin_offer_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Назначить White Bird", callback_data="admin_offer_1")],
        [InlineKeyboardButton(text="Назначить Genesis", callback_data="admin_offer_2")]
    ])