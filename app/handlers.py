from aiogram import types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from config import OFFERS, ADMIN_PASSWORD, ADMINS
from keyboards import offers_kb, new_request_kb
from states import RequestForm
from database import users, requests
from openpyxl import Workbook
import datetime

# ---------- USER ----------

async def start(message: Message):
    users.setdefault(message.from_user.id, {
        "wallet": None,
        "offer": None,
        "stats": {"paid": 0, "pending": 0, "cancelled": 0}
    })
    await message.answer(
        "Выбери оффер:",
        reply_markup=offers_kb()
    )

async def choose_offer(call: CallbackQuery):
    offer_id = int(call.data.split("_")[1])
    users[call.from_user.id]["offer"] = offer_id
    await call.message.answer(
        f"Оффер выбран: {OFFERS[offer_id]['name']}",
        reply_markup=new_request_kb()
    )
    await call.answer()

async def new_request(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Пришли ссылку на видео")
    await state.set_state(RequestForm.video)
    await call.answer()

async def step_video(message: Message, state: FSMContext):
    await state.update_data(video=message.text)
    await message.answer("Пришли ссылку на скриншот (Google Drive)")
    await state.set_state(RequestForm.proof)

async def step_proof(message: Message, state: FSMContext):
    await state.update_data(proof=message.text)
    await message.answer("Сколько просмотров?")
    await state.set_state(RequestForm.views)

async def step_views(message: Message, state: FSMContext):
    data = await state.get_data()
    user = users[message.from_user.id]

    req = {
        "user_id": message.from_user.id,
        "offer": user["offer"],
        "video": data["video"],
        "proof": data["proof"],
        "views": int(message.text),
        "status": "pending",
        "date": datetime.datetime.now()
    }

    requests.append(req)
    user["stats"]["pending"] += 1

    await message.answer("Заявка отправлена. Ожидай проверку.")
    await state.clear()

    send_excel_to_admin(req)

# ---------- ADMIN ----------

async def gen_admin(message: Message, state: FSMContext):
    await message.answer("Введи пароль администратора")
    await state.set_state("admin_auth")

async def admin_auth(message: Message, state: FSMContext):
    if message.text == ADMIN_PASSWORD:
        await message.answer("✅ Ты админ")
        await state.clear()
    else:
        await message.answer("❌ Неверный пароль")

# ---------- EXCEL ----------

def send_excel_to_admin(req):
    wb = Workbook()
    ws = wb.active

    ws.append([
        "User ID", "Offer", "Video", "Proof", "Views", "Status", "Date"
    ])

    ws.append([
        req["user_id"],
        req["offer"],
        req["video"],
        req["proof"],
        req["views"],
        req["status"],
        req["date"].strftime("%Y-%m-%d %H:%M")
    ])

    filename = f"/tmp/request_{req['user_id']}.xlsx"
    wb.save(filename)

    # отправка будет через bot в следующем шаге