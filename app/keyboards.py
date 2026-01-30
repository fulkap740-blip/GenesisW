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
        [InlineKeyboardButton(text="📊 Заявки на сегодня", callback_data="admin_today")],
        [InlineKeyboardButton(text="🚪 Выход", callback_data="admin_exit")]
    ])


def approve_reject_kb(request_id: int):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Одобрить", callback_data=f"approve_{request_id}"),
            InlineKeyboardButton(text="❌ Отклонить", callback_data=f"reject_{request_id}")
        ]
    ])
