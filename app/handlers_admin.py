from aiogram.types import Message
from db import DB_NAME
import aiosqlite
from excel import build_excel
from config import OFFERS

async def send_excel(bot, offer_id):
    async with aiosqlite.connect(DB_NAME) as db:
        rows = await db.execute_fetchall(
            "SELECT user_id, offer_id, video, proof, views, amount, status FROM requests WHERE offer_id=?",
            (offer_id,)
        )

    requests = [
        dict(zip(
            ["user_id","offer_id","video","proof","views","amount","status"],
            r
        )) for r in rows
    ]

    file = build_excel(requests)
    await bot.send_document(
        OFFERS[offer_id]["admin_id"],
        document=open(file, "rb")
    )