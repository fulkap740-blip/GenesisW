import asyncio
import os
from aiogram import Bot, Dispatcher, F

print("BOT_TOKEN ENV =", os.getenv("BOT_TOKEN"))

from config import BOT_TOKEN
from handlers import *
from states import RequestForm

bot = Bot(BOT_TOKEN)
dp = Dispatcher()

dp.message.register(start, F.text == "/start")
dp.callback_query.register(choose_offer, F.data.startswith("offer_"))
dp.callback_query.register(new_request, F.data == "new_request")

dp.message.register(step_video, RequestForm.video)
dp.message.register(step_proof, RequestForm.proof)
dp.message.register(step_views, RequestForm.views)

dp.message.register(gen_admin, F.text == "/gen_admin")
dp.message.register(admin_auth)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())