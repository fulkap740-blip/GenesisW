from aiogram import types
from app.config import ADMIN_PASSWORD
from app.keyboards import admin_menu
from app.excel import create_excel
from app.db import DB_NAME
import sqlite3

ADMINS = set()


async def gen_admin(message: types.Message):
    await message.answer("Введите пароль администратора:")


async def admin_auth(message: types.Message):
    if message.text == ADMIN_PASSWORD:
        ADMINS.add(message.from_user.id)
        await message.answer("✅ Вы вошли в админку", reply_markup=admin_menu())
    else:
        # молча игнорируем
        return


async def admin_export(call: types.CallbackQuery):
    if call.from_user.id not in ADMINS:
        return

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
            ORDER BY created DESC
        """).fetchall()

    path = create_excel(rows)
    await call.message.answer_document(types.FSInputFile(path))
    await call.answer()


async def admin_exit(call: types.CallbackQuery):
    ADMINS.discard(call.from_user.id)
    await call.message.answer("🚪 Вы вышли из админки")
    await call.answer()