from aiogram import types
from aiogram.fsm.context import FSMContext
from app.keyboards import offer_keyboard, main_menu
from app.states import RequestForm
from app.config import OFFERS
from app.db import DB_NAME, get_rate
import sqlite3


async def start(message: types.Message):
    await message.answer("Выбери оффер:", reply_markup=offer_keyboard())


async def choose_offer(call: types.CallbackQuery, state: FSMContext):
    offer_id = int(call.data.split("_")[1])
    await state.update_data(offer=OFFERS[offer_id])
    await call.message.answer("Введи кошелёк USDT TRC20:")
    await call.answer()


async def save_wallet(message: types.Message, state: FSMContext):
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute(
            "INSERT OR REPLACE INTO users (user_id, wallet) VALUES (?, ?)",
            (message.from_user.id, message.text)
        )
        conn.commit()

    await message.answer("Кошелёк сохранён", reply_markup=main_menu())


async def new_request(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer("Ссылка на видео:")
    await state.set_state(RequestForm.video)
    await call.answer()


async def step_video(message: types.Message, state: FSMContext):
    await state.update_data(video=message.text)
    await message.answer("Ссылка на пруф (Google Drive):")
    await state.set_state(RequestForm.proof)


async def step_proof(message: types.Message, state: FSMContext):
    await state.update_data(proof=message.text)
    await message.answer("Количество просмотров:")
    await state.set_state(RequestForm.views)


async def step_views(message: types.Message, state: FSMContext):
    data = await state.get_data()
    views = int(message.text)

    offer_name = data["offer"]["name"]
    rate = get_rate(offer_name)
    amount = (views / 1000) * rate

    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("""
        INSERT INTO requests
        (user_id, offer, video_link, proof_link, views, amount, status)
        VALUES (?, ?, ?, ?, ?, ?, 'pending')
        """, (
            message.from_user.id,
            offer_name,
            data["video"],
            data["proof"],
            views,
            amount
        ))
        conn.commit()

    await message.answer(
        f"Заявка отправлена\n"
        f"Просмотры: {views}\n"
        f"Ставка: {rate} USDT\n"
        f"Сумма: {amount:.2f} USDT\n"
        f"(может быть пересмотрена модерацией)"
    )

    await state.clear()