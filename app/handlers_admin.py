from aiogram import types
from app.config import ADMIN_PASSWORD, OFFERS
from app.excel import create_excel
import sqlite3
from app.db import DB_NAME

admins = set()

async def gen_admin(message: types.Message):
    await message.answer("Введите пароль:")

async def admin_auth(message: types.Message):
    if message.text == ADMIN_PASSWORD:
        admins.add(message.from_user.id)
        await message.answer("Ты админ. /export")
    else:
        await message.answer("Неверный пароль")

async def export_excel(message: types.Message):
    if message.from_user.id not in admins:
        return

    with sqlite3.connect(DB_NAME) as conn:
        rows = conn.execute("SELECT * FROM requests").fetchall()

    path = create_excel(rows)
    await message.answer_document(types.FSInputFile(path))