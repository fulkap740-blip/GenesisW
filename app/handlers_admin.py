from aiogram import types
from app.config import ADMIN_PASSWORD, OFFERS
from app.db import DB_NAME, set_rate
from app.excel import make_excel
import sqlite3

admins = set()

async def gen_admin(message: types.Message):
    await message.answer("Введите пароль:")

async def admin_auth(message: types.Message):
    if message.text == ADMIN_PASSWORD:
        admins.add(message.from_user.id)
        await message.answer("Админ доступ получен")
    else:
        await message.answer("Неверный пароль")

async def export_excel(message: types.Message):
    if message.from_user.id not in admins:
        return

    with sqlite3.connect(DB_NAME) as conn:
        rows = conn.execute("SELECT * FROM requests").fetchall()

    path = make_excel(rows)
    await message.answer_document(types.FSInputFile(path))

async def change_rate(message: types.Message):
    if message.from_user.id not in admins:
        return

    try:
        _, offer_id, rate = message.text.split()
        set_rate(int(offer_id), float(rate))
        await message.answer("Ставка обновлена")
    except:
        await message.answer("Формат: /rate <offer_id> <rate>")