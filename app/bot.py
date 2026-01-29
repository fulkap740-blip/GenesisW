import asyncio
from aiogram import Bot, Dispatcher, F
from app.config import BOT_TOKEN
from app.db import init_db
from app.handlers_user import *
from app.handlers_admin import *

bot = Bot(BOT_TOKEN)
dp = Dispatcher()

dp.message.register(start, F.text == "/start")
dp.callback_query.register(choose_offer, F.data.startswith("offer_"))
dp.message.register(save_wallet, F.text.startswith("T"))
dp.callback_query.register(new_request, F.data == "new_request")
dp.message.register(step_video, RequestForm.video)
dp.message.register(step_proof, RequestForm.proof)
dp.message.register(step_views, RequestForm.views)

dp.message.register(gen_admin, F.text == "/gen_admin")
dp.message.register(admin_auth)
dp.message.register(export_excel, F.text == "/export")

async def main():
    init_db()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())