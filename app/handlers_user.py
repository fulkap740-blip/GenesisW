from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from db import DB_NAME
import aiosqlite
from states import RequestForm
from keyboards import offers_kb, user_menu_kb
from config import OFFERS

async def start(message: Message):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            "INSERT OR IGNORE INTO users (user_id) VALUES (?)",
            (message.from_user.id,)
        )
        await db.commit()
    await message.answer("Выбери оффер:", reply_markup=offers_kb())

async def choose_offer(call: CallbackQuery):
    offer_id = int(call.data.split("_")[1])
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            "UPDATE users SET offer_id=? WHERE user_id=?",
            (offer_id, call.from_user.id)
        )
        await db.commit()
    await call.message.answer("Оффер выбран", reply_markup=user_menu_kb())
    await call.answer()

async def new_request(call: CallbackQuery, state: FSMContext):
    await state.set_state(RequestForm.video)
    await call.message.answer("Ссылка на видео:")
    await call.answer()

async def step_video(message: Message, state: FSMContext):
    await state.update_data(video=message.text)
    await state.set_state(RequestForm.proof)
    await message.answer("Ссылка на пруф:")

async def step_proof(message: Message, state: FSMContext):
    await state.update_data(proof=message.text)
    await state.set_state(RequestForm.views)
    await message.answer("Количество просмотров:")

async def step_views(message: Message, state: FSMContext):
    data = await state.get_data()
    views = int(message.text)

    async with aiosqlite.connect(DB_NAME) as db:
        user = await db.execute_fetchone(
            "SELECT offer_id FROM users WHERE user_id=?",
            (message.from_user.id,)
        )
        offer_id = user[0]
        rate = OFFERS[offer_id]["rate"]
        amount = round((views / 1000) * rate, 2)

        await db.execute("""
        INSERT INTO requests (user_id, offer_id, video, proof, views, amount, status)
        VALUES (?,?,?,?,?,?,?)
        """, (message.from_user.id, offer_id, data["video"], data["proof"], views, amount, "pending"))
        await db.commit()

    await message.answer(
        f"Заявка отправлена\n💰 {amount} USDT\n⚠️ Может быть пересмотрено модерацией"
    )
    await state.clear()