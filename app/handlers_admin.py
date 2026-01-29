from aiogram import types
from datetime import date
import sqlite3

from app.config import ADMIN_PASSWORD
from app.keyboards import admin_menu
from app.db import DB_NAME, set_rate
from app.excel import create_excel

ADMINS = set()


async def gen_admin(message: types.Message):
    await message.answer("Введите пароль:")


async def admin_auth(message: types.Message):
    if message.text == ADMIN_PASSWORD:
        ADMINS.add(message.from_user.id)
        await message.answer("Админка", reply_markup=admin_menu())


async def admin_today(call: types.CallbackQuery):
    if call.from_user.id not in ADMINS:
        return

    today = date.today().isoformat()

    with sqlite3.connect(DB_NAME) as conn:
        rows = conn.execute("""
        SELECT
            user_id,
            offer,
            video_link,
            proof_link,
            views,
            amount,
            status,
            created
        FROM requests
        WHERE DATE(created) = ?
        ORDER BY created DESC
        """, (today,)).fetchall()

    if not rows:
        await call.message.answer("За сегодня заявок нет.")
        await call.answer()
        return

    filename = f"requests_{today}.xlsx"
    path = create_excel(rows, filename)

    await call.message.answer_document(types.FSInputFile(path))
    await call.answer()


async def admin_rate(call: types.CallbackQuery):
    await call.message.answer(
        "Формат:\n\n"
        "White Bird 1.7\n"
        "Genesis 2.3"
    )
    await call.answer()


async def admin_exit(call: types.CallbackQuery):
    ADMINS.discard(call.from_user.id)
    await call.message.answer("Вы вышли из админки")
    await call.answer()
