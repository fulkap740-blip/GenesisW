from aiogram import types
from aiogram.fsm.context import FSMContext
from app.keyboards import offers_kb, user_menu
from app.states import RequestForm
from app.db import DB_NAME, get_rate
import sqlite3

async def start(message: types.Message):
    await message.answer("Выбери оффер:", reply_markup=offers_kb())

async def choose_offer(call: types.CallbackQuery, state: FSMContext):
    offer_id = int(call.data.split("_")[1])
    await state.update_data(offer_id=offer_id)
    await call.message.answer("Введи кошелёк USDT TRC20:")
    await call.answer()

async def save_wallet(message: types.Message, state: FSMContext):
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute(
            "INSERT OR REPLACE INTO users (user_id, wallet) VALUES (?,?)",
            (message.from_user.id, message.text)
        )
    await message.answer("Кошелёк сохранён", reply_markup=user_menu())

async def new_request(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer("Ссылка на видео:")
    await state.set_state(RequestForm.video)
    await call.answer()

async def step_video(message: types.Message, state: FSMContext):
    await state.update_data(video=message.text)
    await message.answer("Ссылка на proof:")
    await state.set_state(RequestForm.proof)

async def step_proof(message: types.Message, state: FSMContext):
    await state.update_data(proof=message.text)
    await message.answer("Количество просмотров:")
    await state.set_state(RequestForm.views)

async def step_views(message: types.Message, state: FSMContext):
    data = await state.get_data()
    views = int(message.text)
    rate = get_rate(data["offer_id"])
    amount = round((views / 1000) * rate, 2)

    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("""
        INSERT INTO requests
        (user_id, offer_id, video, proof, views, amount, status)
        VALUES (?,?,?,?,?,?,?)
        """, (
            message.from_user.id,
            data["offer_id"],
            data["video"],
            data["proof"],
            views,
            amount,
            "pending"
        ))

    await message.answer(
        f"Заявка отправлена\n💰 {amount} USDT\n⚠️ Может быть пересмотрено"
    )
    await state.clear()