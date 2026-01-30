from aiogram import types
from aiogram.fsm.context import FSMContext
from app.states import RequestForm
from app.keyboards import offer_keyboard, user_menu
from app.db import DB_NAME, get_rate
import sqlite3


STATUS_MAP = {
    "pending": "🟡 На проверке",
    "approved": "🟢 Одобрено",
    "rejected": "🔴 Отклонено"
}


async def start(message: types.Message):
    await message.answer("Выбери оффер:", reply_markup=offer_keyboard())


async def choose_offer(call: types.CallbackQuery, state: FSMContext):
    offer = call.data.split("_", 1)[1]
    await state.update_data(offer=offer)

    with sqlite3.connect(DB_NAME) as conn:
        row = conn.execute(
            "SELECT wallet FROM users WHERE user_id = ?",
            (call.from_user.id,)
        ).fetchone()

    if row and row[0]:
        await call.message.answer("Оффер выбран.", reply_markup=user_menu())
    else:
        await call.message.answer("Введи кошелёк USDT TRC20:")

    await call.answer()


async def save_wallet(message: types.Message):
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute(
            "INSERT OR REPLACE INTO users (user_id, wallet) VALUES (?, ?)",
            (message.from_user.id, message.text)
        )
        conn.commit()

    await message.answer("Кошелёк сохранён.", reply_markup=user_menu())


async def profile(call: types.CallbackQuery):
    with sqlite3.connect(DB_NAME) as conn:
        wallet = conn.execute(
            "SELECT wallet FROM users WHERE user_id = ?",
            (call.from_user.id,)
        ).fetchone()

        reqs = conn.execute("""
        SELECT offer, amount, status
        FROM requests
        WHERE user_id = ?
        ORDER BY created DESC
        """, (call.from_user.id,)).fetchall()

    text = (
        f"👤 Профиль\n\n"
        f"ID: {call.from_user.id}\n"
        f"Кошелёк: {wallet[0] if wallet else 'не указан'}\n\n"
        f"📋 Заявки:\n"
    )

    if not reqs:
        text += "— заявок нет"
    else:
        for r in reqs:
            text += f"{r[0]} | {r[1]:.2f} USDT | {STATUS_MAP[r[2]]}\n"

    await call.message.answer(text, reply_markup=user_menu())
    await call.answer()


async def help_cmd(call: types.CallbackQuery):
    await call.message.answer(
        "ℹ️ Используй меню ниже для работы с ботом.",
        reply_markup=user_menu()
    )
    await call.answer()
