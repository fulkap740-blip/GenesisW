from aiogram import types
from aiogram.fsm.context import FSMContext
from datetime import date
import sqlite3

from app.keyboards import main_menu, offers_kb, back_menu
from app.states import RequestForm
from app.db import DB_NAME, get_rate
from app.config import OFFERS

# /start
async def start(message: types.Message):
    await message.answer("Добро пожаловать", reply_markup=main_menu())

# профиль
async def profile(call: types.CallbackQuery):
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()
        cur.execute("SELECT wallet FROM users WHERE user_id=?", (call.from_user.id,))
        wallet = cur.fetchone()
        cur.execute("SELECT COUNT(*) FROM requests WHERE user_id=?", (call.from_user.id,))
        total = cur.fetchone()[0]

    text = (
        f"👤 Профиль\n\n"
        f"🆔 ID: {call.from_user.id}\n"
        f"💼 Кошелёк: {wallet[0] if wallet else 'не привязан'}\n"
        f"📊 Всего заявок: {total}"
    )

    await call.message.edit_text(text, reply_markup=back_menu())
    await call.answer()

# новая заявка → офферы
async def new_request(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text("Выбери оффер:", reply_markup=offers_kb())
    await call.answer()

# выбор оффера
async def choose_offer(call: types.CallbackQuery, state: FSMContext):
    offer_id = int(call.data.split("_")[1])
    await state.update_data(offer_id=offer_id)
    await call.message.edit_text("Введи кошелёк USDT TRC20:")
    await call.answer()

# сохранение кошелька
async def save_wallet(message: types.Message, state: FSMContext):
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute(
            "INSERT OR REPLACE INTO users (user_id, wallet) VALUES (?,?)",
            (message.from_user.id, message.text)
        )
    await message.answer("Кошелёк сохранён. Ссылка на видео:")
    await state.set_state(RequestForm.video)

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
        (user_id, offer_id, video, proof, views, amount, status, created)
        VALUES (?,?,?,?,?,?,?,?)
        """, (
            message.from_user.id,
            data["offer_id"],
            data["video"],
            data["proof"],
            views,
            amount,
            "pending",
            date.today().isoformat()
        ))

    await message.answer(
        f"Заявка сохранена\n💰 {amount} USDT",
        reply_markup=main_menu()
    )
    await state.clear()

# отправка заявок за сегодня
async def send_today(call: types.CallbackQuery):
    from app.excel import make_excel
    today = date.today().isoformat()

    with sqlite3.connect(DB_NAME) as conn:
        rows = conn.execute("""
        SELECT user_id, offer_id, video, proof, views, amount, status
        FROM requests
        WHERE user_id=? AND created=?
        """, (call.from_user.id, today)).fetchall()

    if not rows:
        await call.answer("Заявок за сегодня нет", show_alert=True)
        return

    path = make_excel(rows)

    offer_id = rows[0][1]
    admin_id = OFFERS[offer_id]["admin_id"]

    await call.bot.send_document(admin_id, types.FSInputFile(path))
    await call.answer("Заявки за сегодня отправлены")

# help
async def help_cmd(call: types.CallbackQuery):
    await call.message.edit_text(
        "ℹ️ Help\n\n"
        "➕ Новая заявка — отправка заявок\n"
        "🧾 Это все мои заявки на сегодня — отправка админу\n"
        "👤 Профиль — ваша статистика",
        reply_markup=back_menu()
    )
    await call.answer()

# назад
async def back(call: types.CallbackQuery):
    await call.message.edit_text("Главное меню", reply_markup=main_menu())
    await call.answer()