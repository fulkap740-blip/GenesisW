from aiogram import types
from aiogram.fsm.context import FSMContext
from app.states import RequestForm
from app.keyboards import offer_keyboard, user_menu
from app.db import DB_NAME, get_rate
import sqlite3


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
        user = conn.execute(
            "SELECT wallet FROM users WHERE user_id = ?",
            (call.from_user.id,)
        ).fetchone()

        stats = conn.execute(
            "SELECT COUNT(*), COALESCE(SUM(amount),0) FROM requests WHERE user_id = ?",
            (call.from_user.id,)
        ).fetchone()

    text = (
        f"👤 Профиль\n\n"
        f"ID: {call.from_user.id}\n"
        f"Кошелёк: {user[0] if user else 'не указан'}\n"
        f"Заявок: {stats[0]}\n"
        f"Сумма: {stats[1]:.2f} USDT"
    )

    await call.message.answer(text, reply_markup=user_menu())
    await call.answer()


async def help_cmd(call: types.CallbackQuery):
    await call.message.answer(
        "ℹ️ Инструкция:\n"
        "1. Выбери оффер\n"
        "2. Отправь заявку\n"
        "3. Дождись выплаты",
        reply_markup=user_menu()
    )
    await call.answer()


async def new_request(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer("Ссылка на видео:")
    await state.set_state(RequestForm.video)
    await call.answer()


async def step_video(message: types.Message, state: FSMContext):
    await state.update_data(video=message.text)
    await message.answer("Ссылка на пруф:")
    await state.set_state(RequestForm.proof)


async def step_proof(message: types.Message, state: FSMContext):
    await state.update_data(proof=message.text)
    await message.answer("Количество просмотров:")
    await state.set_state(RequestForm.views)


async def step_views(message: types.Message, state: FSMContext):
    data = await state.get_data()
    views = int(message.text)
    rate = get_rate(data["offer"])
    amount = (views / 1000) * rate

    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("""
        INSERT INTO requests
        (user_id, offer, video_link, proof_link, views, amount, status)
        VALUES (?,?,?,?,?,?,?)
        """, (
            message.from_user.id,
            data["offer"],
            data["video"],
            data["proof"],
            views,
            amount,
            "pending"
        ))
        conn.commit()

    await message.answer(
        f"✅ Заявка отправлена\n"
        f"Сумма: {amount:.2f} USDT\n"
        f"(может быть пересмотрена)",
        reply_markup=user_menu()
    )

    await state.clear()