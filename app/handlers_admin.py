from aiogram import types
from datetime import date
import sqlite3

from app.config import ADMIN_PASSWORD
from app.keyboards import admin_menu
from app.db import DB_NAME
from app.excel import make_excel

admins = set()

async def gen_admin(message: types.Message):
    parts = message.text.split(maxsplit=1)
    if len(parts) != 2 or parts[1] != ADMIN_PASSWORD:
        return
    admins.add(message.from_user.id)
    await message.answer("Админ доступ получен", reply_markup=admin_menu())

async def exit_admin(message: types.Message):
    admins.discard(message.from_user.id)
    await message.answer("Вы вышли из админки")

async def admin_today(call: types.CallbackQuery):
    if call.from_user.id not in admins:
        return

    today = date.today().isoformat()
    with sqlite3.connect(DB_NAME) as conn:
        rows = conn.execute("""
        SELECT user_id, offer_id, video, proof, views, amount, status
        FROM requests WHERE created=?
        """, (today,)).fetchall()

    if not rows:
        await call.answer("Заявок за сегодня нет", show_alert=True)
        return

    path = make_excel(rows)
    await call.message.answer_document(types.FSInputFile(path))
    await call.answer()