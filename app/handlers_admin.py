from aiogram import types
from datetime import date
import sqlite3

from app.config import ADMIN_PASSWORD
from app.keyboards import admin_menu, approve_reject_kb
from app.db import DB_NAME

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
        SELECT id, user_id, offer, video_link, proof_link, views, amount, status
        FROM requests
        WHERE DATE(created) = ?
        ORDER BY created DESC
        """, (today,)).fetchall()

    if not rows:
        await call.message.answer("Заявок нет.")
        await call.answer()
        return

    for r in rows:
        text = (
            f"📝 Заявка #{r[0]}\n\n"
            f"👤 User ID: {r[1]}\n"
            f"📦 Оффер: {r[2]}\n"
            f"🎬 Видео: {r[3]}\n"
            f"📸 Пруф: {r[4]}\n"
            f"👀 Просмотры: {r[5]}\n"
            f"💰 Сумма: {r[6]:.2f} USDT\n"
            f"📌 Статус: {r[7]}"
        )

        await call.message.answer(text, reply_markup=approve_reject_kb(r[0]))

    await call.answer()


async def approve_request(call: types.CallbackQuery):
    if call.from_user.id not in ADMINS:
        return

    request_id = int(call.data.split("_")[1])

    with sqlite3.connect(DB_NAME) as conn:
        conn.execute(
            "UPDATE requests SET status = 'approved' WHERE id = ?",
            (request_id,)
        )
        conn.commit()

    await call.message.edit_text(call.message.text + "\n\n🟢 Одобрено")
    await call.answer("Одобрено")


async def reject_request(call: types.CallbackQuery):
    if call.from_user.id not in ADMINS:
        return

    request_id = int(call.data.split("_")[1])

    with sqlite3.connect(DB_NAME) as conn:
        conn.execute(
            "UPDATE requests SET status = 'rejected' WHERE id = ?",
            (request_id,)
        )
        conn.commit()

    await call.message.edit_text(call.message.text + "\n\n🔴 Отклонено")
    await call.answer("Отклонено")


async def admin_exit(call: types.CallbackQuery):
    ADMINS.discard(call.from_user.id)
    await call.message.answer("Вы вышли из админки")
    await call.answer()
