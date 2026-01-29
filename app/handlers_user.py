from aiogram import types
from aiogram.fsm.context import FSMContext
from app.keyboards import offer_keyboard, main_menu
from app.states import RequestForm
from app.config import OFFERS
import sqlite3
from app.db import DB_NAME

async def start(message: types.Message):
    await message.answer("Выбери оффер:", reply_markup=offer_keyboard())

async def choose_offer(call: types.CallbackQuery, state: FSMContext):
    offer_id = int(call.data.split("_")[1])
    await state.update_data(offer=OFFERS[offer_id])
    await call.message.answer("Привяжи кошелёк USDT TRC20:")
    await call.answer()

async def save_wallet(message: types.Message, state: FSMContext):
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute(
            "INSERT OR REPLACE INTO users (user_id, wallet) VALUES (?,?)",
            (message.from_user.id, message.text)
        )
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
    amount = views * data["offer"]["rate"]

    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("""
        INSERT INTO requests
        (user_id, offer, video_link, proof_link, views, amount, status)
        VALUES (?,?,?,?,?,?,?)
        """, (
            message.from_user.id,
            data["offer"]["name"],
            data["video"],
            data["proof"],
            views,
            amount,
            "pending"
        ))

    await message.answer(
        f"Заявка отправлена\nСумма: {amount} USDT\n(может быть пересмотрена)"
    )
    await state.clear()