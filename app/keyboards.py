from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def main_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="👤 Профиль", callback_data="profile")],
        [InlineKeyboardButton(text="➕ Новая заявка", callback_data="new_request")],
        [InlineKeyboardButton(text="🧾 Это все мои заявки на сегодня", callback_data="send_today")],
        [InlineKeyboardButton(text="ℹ️ Help", callback_data="help")]
    ])

def back_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="back")]
    ])

def offers_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="White Bird", callback_data="offer_1")],
        [InlineKeyboardButton(text="Genesis", callback_data="offer_2")]
    ])

def admin_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📂 Заявки за сегодня", callback_data="admin_today")]
    ])