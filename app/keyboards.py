from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def offer_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="White Bird", callback_data="offer_White Bird")],
        [InlineKeyboardButton(text="Genesis", callback_data="offer_Genesis")]
    ])


def user_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="➕ Новая заявка", callback_data="new_request")],
        [InlineKeyboardButton(text="👤 Профиль", callback_data="profile")],
        [InlineKeyboardButton(text="❓ Help", callback_data="help")]
    ])


def admin_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📊 Экспорт заявок", callback_data="admin_export")],
        [InlineKeyboardButton(text="⚙️ Изменить rate", callback_data="admin_rate")],
        [InlineKeyboardButton(text="🚪 Выход", callback_data="admin_exit")]
    ])