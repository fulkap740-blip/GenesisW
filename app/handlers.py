from aiogram import F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from . import database as db
from .states import RequestForm
from .keyboards import offer_kb, profile_kb, admin_offer_kb
from .config import OFFERS, ADMIN_PASSWORD

async def start(msg: Message):
    db.create_user(msg.from_user.id)
    await msg.answer("Выберите оффер:", reply_markup=offer_kb())

async def choose_offer(call: CallbackQuery):
    offer_id = int(call.data.split("_")[1])
    db.update_user_offer(call.from_user.id, offer_id)
    await call.message.answer("Введите USDT TRC20 кошелёк:")
    await call.answer()

async def save_wallet(msg: Message):
    if not msg.text.startswith("T"):
        return await msg.answer("Неверный формат кошелька")
    db.update_wallet(msg.from_user.id, msg.text)
    await msg.answer("Кошелёк сохранён", reply_markup=profile_kb())

async def new_request(call: CallbackQuery, state: FSMContext):
    await state.set_state(RequestForm.video)
    await call.message.answer("Ссылка на видео:")
    await call.answer()

async def step_video(msg: Message, state: FSMContext):
    await state.update_data(video=msg.text)
    await state.set_state(RequestForm.proof)
    await msg.answer("Ссылка на пруф:")

async def step_proof(msg: Message, state: FSMContext):
    await state.update_data(proof=msg.text)
    await state.set_state(RequestForm.views)
    await msg.answer("Количество просмотров:")

async def step_views(msg: Message, state: FSMContext):
    if not msg.text.isdigit():
        return await msg.answer("Введите число")
    views = int(msg.text)
    data = await state.get_data()
    user = db.get_user(msg.from_user.id)
    rate = OFFERS[user[1]]["rate"]
    amount = round((views / 1000) * rate, 2)

    db.add_request((
        msg.from_user.id,
        user[1],
        data["video"],
        data["proof"],
        views,
        amount,
        "⏳ На проверке"
    ))

    await msg.answer(
        f"Заявка принята\n💰 {amount} USDT\n⚠️ Может быть пересмотрено"
    )
    await state.clear()

async def gen_admin(msg: Message):
    await msg.answer("Введите пароль администратора:")

async def admin_auth(msg: Message):
    if msg.text != ADMIN_PASSWORD:
        return
    db.set_admin(msg.from_user.id)
    await msg.answer("Вы админ. Назначьте оффер:", reply_markup=admin_offer_kb())

async def admin_offer(call: CallbackQuery):
    offer_id = int(call.data.split("_")[2])
    db.set_admin_offer(call.from_user.id, offer_id)
    await call.message.answer("Оффер администратора назначен")
    await call.answer()