import asyncio
from aiogram import Bot, Dispatcher, F

from app.config import BOT_TOKEN
from app.db import init_db
from app.states import RequestForm

from app.handlers_user import (
    start,
    profile,
    new_request,
    choose_offer,
    save_wallet,
    step_video,
    step_proof,
    step_views,
    send_today,
    help_cmd,
    back
)

from app.handlers_admin import (
    gen_admin,
    exit_admin,
    admin_today
)

# 1️⃣ создаём бота и диспетчер
bot = Bot(BOT_TOKEN)
dp = Dispatcher()

# 2️⃣ USER handlers
dp.message.register(start, F.text == "/start")
dp.callback_query.register(profile, F.data == "profile")
dp.callback_query.register(new_request, F.data == "new_request")
dp.callback_query.register(choose_offer, F.data.startswith("offer_"))

dp.message.register(save_wallet, F.text.startswith("T"))
dp.message.register(step_video, RequestForm.video)
dp.message.register(step_proof, RequestForm.proof)
dp.message.register(step_views, RequestForm.views)

dp.callback_query.register(send_today, F.data == "send_today")
dp.callback_query.register(help_cmd, F.data == "help")
dp.callback_query.register(back, F.data == "back")

# 3️⃣ ADMIN handlers (СКРЫТЫЕ)
dp.message.register(gen_admin, F.text.startswith("/gen_admin"))
dp.message.register(exit_admin, F.text == "/exit")
dp.callback_query.register(admin_today, F.data == "admin_today")

# 4️⃣ запуск
async def main():
    init_db()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())